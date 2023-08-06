"""
Models for Rates module
"""
import datetime
import logging
from datetime import date, timedelta
from hashlib import md5

import networkx as nx
from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from djangophysics.converters.models import BaseConverter, \
    ConverterResult, ConverterResultDetail, \
    ConverterResultError
from djangophysics.core.helpers import service
from djangophysics.currencies.models import Currency

try:
    RATE_SERVICE = settings.RATE_SERVICE
except AttributeError:
    pass

from .services import RatesNotAvailableError


class NoRateFound(Exception):
    """
    Exception when no rate is found
    """
    pass


class BaseRate(models.Model):
    """
    Just an abstract for value and hinting
    """
    value = None

    class Meta:
        """
        Yes, it is abstract
        """
        abstract = True


class RateManager(models.Manager):
    """
    Manager for Rate model
    """

    @staticmethod
    def __sync_rates__(rates: [], base_currency: str):
        """
        Sync rates to the database
        :param rates: array of dict of rates from service
        :param base_currency: base currency to fetch
        """
        output = []
        for rate in rates:
            try:
                _rate, created = Rate.objects.get_or_create(
                    base_currency=base_currency,
                    currency=rate.get('currency'),
                    value_date=rate.get('date'),
                    user=None,
                    key=None
                )
                _rate.value = rate.get('value')
                _rate.save()
            except Rate.MultipleObjectsReturned:
                _rates = Rate.objects.filter(
                    base_currency=base_currency,
                    currency=rate.get('currency'),
                    value_date=rate.get('date'),
                    user=None,
                    key=None
                )
                _rates.update(value=rate.get('value'))
                _rate = _rates.first()
            output.append(_rate)
        return output

    def fetch_rates(self,
                    base_currency: str,
                    currency: str = None,
                    rate_service: str = None,
                    date_obj: date = date.today(),
                    to_obj: date = None) -> []:
        """
        Get rates from a service for a base currency
        and stores them in the database
        If the date is the current date, the rate is not available
        so we take the rate from the day before
        :param rate_service: Service class to fetch from
        :param currency: currency to obtain rate for
        :param base_currency: base currency to get rate from
        :param date_obj: date to fetch rates at
        :param to_obj: end of range
        :return: QuerySet of Rate
        """
        service_name = rate_service or settings.RATE_SERVICE
        try:
            rates = service(
                service_type='rates',
                service_name=service_name
            ).fetch_rates(
                base_currency=base_currency,
                currency=currency,
                date_obj=date_obj,
                to_obj=to_obj)
            if not rates:
                return False
            for d in range((date_obj - (to_obj or date_obj)).days + 1):
                RateServiceFetch.objects.create(
                    service=service_name,
                    value_date=date_obj + timedelta(d),
                    fetch_date=date.today()
                )
        except RatesNotAvailableError as e:
            logging.warning("fetch_rates: Rates not available")
            return False
        return self.__sync_rates__(rates=rates, base_currency=base_currency)

    def rate_at_date(self,
                     currency: str,
                     key: str = None,
                     base_currency: str = settings.BASE_CURRENCY,
                     date_obj: date = date.today()) -> BaseRate:
        """
        Get a rate at a given date
        :param currency: target currency
        :param base_currency: destination currency
        :param key: User key
        :param date_obj: date at which to fetch the rate
        """
        rate = self.find_rate(
            currency=currency,
            key=key,
            base_currency=base_currency,
            date_obj=date_obj)
        if rate and rate.pk:
            return rate
        return Rate()

    @classmethod
    def currency_shortest_path(
            cls, currency: str, base_currency: str, key: str = None,
            date_obj: date = date.today()) -> [str]:
        """
        Return the shortest path between 2 currencies for the given date
        :param currency: source currency code
        :param base_currency: base currency code
        :param key: Key specific to a client
        :param date_obj: Date to obtain the conversion rate for
        :return List of currency codes to go from currency to base currency
        """
        rates = Rate.objects.filter(value_date=date_obj).filter(
            models.Q(user=None) | models.Q(key=key))
        rates_couples = rates.values(
            'currency', 'base_currency', 'value', 'key')
        graph = nx.Graph()
        for k in rates_couples:
            weight = 0.5 if k['base_currency'] == 'EUR' or \
                            k['currency'] == 'EUR' else 1
            weight *= (0.5 if k['key'] else 1)
            graph.add_edge(
                u_of_edge=k['currency'],
                v_of_edge=k['base_currency'], weight=weight)
        try:
            return nx.shortest_path(
                graph, currency, base_currency, weight='weight')
        except (nx.exception.NetworkXNoPath,
                nx.exception.NodeNotFound) as exc:
            raise NoRateFound(
                f"Rate {currency} to {base_currency} on "
                f"key {key} at date {date_obj} does not exist") \
                from exc

    def _find_rate_or_reverse(self,
                              currency: str,
                              rate_service: str = None,
                              key: str = None,
                              base_currency: str = settings.BASE_CURRENCY,
                              date_obj: date = date.today()) -> BaseRate:
        """
        Returns the corresponding rate. 
        If the rate does not exists, it looks for the reverse rate and creates the corresponding rate in the 
        database
        :param currency: source currency code
        :param base_currency: base currency code
        :param key: Key specific to a client
        :param date_obj: Date to obtain the conversion rate for
        :param rate_service: Rate service to use
        """
        rate = self.find_rate(
            currency=currency,
            rate_service=rate_service,
            key=key,
            base_currency=base_currency,
            date_obj=date_obj,
            use_forex=True
        )
        if not rate:
            # No rate has been found, trying the search for the reciprocal conversion rate
            reverse_rate = self.find_rate(
                currency=base_currency,
                rate_service=rate_service,
                key=key,
                base_currency=currency,
                date_obj=date_obj,
                use_forex=True
            )
            if reverse_rate and reverse_rate.value:
                # Reverse rate exists, store the original rate
                rate = Rate.objects.create(
                    key=key,
                    value_date=date_obj,
                    currency=currency,
                    base_currency=base_currency,
                    value=1 / reverse_rate.value
                )
        return rate

    def _query_rate_or_reverse(self,
                               currency: str,
                               key: str = None,
                               base_currency: str = settings.BASE_CURRENCY,
                               date_obj: date = date.today()) -> BaseRate:
        """
        Returns the corresponding rate.
        If the rate does not exists, it looks for the reverse rate and creates the corresponding rate in the
        database
        :param currency: source currency code
        :param base_currency: base currency code
        :param key: Key specific to a client
        :param date_obj: Date to obtain the conversion rate for
        """
        rate_hash = md5(
            f"{currency}-{base_currency}-{date_obj.strftime('%Y-%m-d')}-{key}".encode('latin1')
        ).hexdigest()
        rate = cache.get(rate_hash)
        if rate:
            return rate
        rate = Rate.objects.filter(
            currency=currency,
            base_currency=base_currency,
            value_date=date_obj
        ).filter(
            models.Q(key=key) | models.Q(user__isnull=True)
        ).order_by('-key').first()
        if not rate:
            reverse_rate = Rate.objects.filter(
                currency=base_currency,
                base_currency=currency,
                value_date=date_obj
            ).filter(
                models.Q(key=key) | models.Q(user__isnull=True)
            ).order_by('-key').first()
            if reverse_rate and reverse_rate.value:
                rate = Rate.objects.create(
                    key=key,
                    value_date=date_obj,
                    currency=currency,
                    base_currency=base_currency,
                    value=1 / reverse_rate.value
                )
        cache.set(rate_hash, rate)
        return rate

    def find_rate(self, currency: str,
                  rate_service: str = None,
                  key: str = None,
                  base_currency: str = settings.BASE_CURRENCY,
                  date_obj: date = date.today(),
                  use_forex: bool = False) -> BaseRate:
        """
        Find rate based on Floyd Warshall algorithm
        If the date is the current date, the rate is not available
        so we take the rate from the day before
        :param currency: source currency code
        :param base_currency: base currency code
        :param key: Key specific to a client
        :param date_obj: Date to obtain the conversion rate for
        :param rate_service: Rate service to use
        :param use_forex: use rate service to fill the gaps
        """
        if use_forex:
            # Try fetching value directly from service
            if not self.fetch_rates(
                    base_currency=base_currency,
                    currency=currency,
                    rate_service=rate_service,
                    date_obj=date_obj):
                return Rate()
        try:
            # Find a path between currency and base currency
            rates = self.currency_shortest_path(
                currency=currency,
                base_currency=base_currency,
                key=key,
                date_obj=date_obj
            )
        except NoRateFound:
            # No relation found, try fetching rate
            rate = self._find_rate_or_reverse(
                currency=currency,
                rate_service=rate_service,
                key=key,
                base_currency=base_currency,
                date_obj=date_obj
            )
            return rate
        # Direct connection between rates
        if len(rates) == 2:
            rate = self._query_rate_or_reverse(
                currency=currency,
                key=key,
                base_currency=base_currency,
                date_obj=date_obj
            )
            return rate
        else:
            conv_value = 1
            for i in range(len(rates) - 1):
                from_cur, to_cur = rates[i:i + 2]
                rate = self.find_rate(
                    currency=from_cur,
                    base_currency=to_cur,
                    key=key,
                    date_obj=date_obj,
                    use_forex=False)
                if rate:
                    conv_value *= rate.value
                else:
                    raise NoRateFound(
                        f"rate {from_cur} -> {to_cur} for key {key} "
                        f"does not exist at date {date_obj}")
            rate = Rate.objects.create(
                key=key,
                value_date=date_obj,
                currency=currency,
                base_currency=base_currency,
                value=conv_value
            )
            return rate

    def find_rates(self,
                  rate_service: str = None,
                  key: str = None,
                  base_currency: str = settings.BASE_CURRENCY,
                  date_obj: date = date.today()) -> [BaseRate]:
        """
        Fetch all rates for all currencies provided
         by the rate service to a base currency
        :param base_currency: base currency code
        :param key: Key specific to a client
        :param date_obj: Date to obtain the conversion rate for
        :param rate_service: Rate service to use
        """
        if not RateServiceFetch.objects.filter(
            service=rate_service,
            value_date=date_obj
        ).exists():
            self.fetch_rates(
                base_currency=base_currency,
                rate_service=rate_service,
                date_obj=date_obj,
            )
        return Rate.objects.filter(
            base_currency=base_currency,
            value_date=date_obj
        ).filter(
            models.Q(key=key) | models.Q(user__isnull=True)
        ).order_by('-key')


class Rate(BaseRate):
    """
    Class Rate
    """
    user = models.ForeignKey(User, related_name='rates',
                             on_delete=models.PROTECT, null=True,
                             db_index=True)
    key = models.CharField("User defined categorization key",
                           max_length=255, default=None,
                           db_index=True, null=True)
    value_date = models.DateField("Date of value", db_index=True)
    value = models.FloatField("Rate conversion factor", default=0)
    currency = models.CharField("Currency to convert from",
                                max_length=3, db_index=True)
    base_currency = models.CharField("Currency to convert to",
                                     max_length=3, db_index=True,
                                     default='EUR')
    objects = RateManager()

    class Meta:
        """
        Meta
        """
        ordering = ['-value_date', ]
        indexes = [
            models.Index(fields=['user', 'key']),
            models.Index(fields=['base_currency', 'value_date']),
            models.Index(fields=['currency', 'value_date']),
            models.Index(fields=['currency', 'base_currency', 'value_date']),
            models.Index(fields=['key', 'currency',
                                 'base_currency', 'value_date']),
        ]
        unique_together = [['key', 'currency', 'base_currency', 'value_date']]

    @classmethod
    def convert(cls, currency: str,
                user: User = None,
                key: str = None,
                base_currency: str = 'EUR',
                date_obj: date = date.today(),
                amount: float = 0) -> ConverterResult:
        """
        Convert rate
        :param user: Django User
        :param key: key for user
        :param base_currency: destination currency
        :param currency: source currency
        :param date_obj: date of the rate
        :param amount: amount to convert
        """
        converter = RateConverter(user=user, key=key,
                                  base_currency=base_currency)
        converter.add_data(
            {
                'currency': currency,
                'amount': amount,
                'date': date_obj
            }
        )
        result = converter.convert()
        return result

    @property
    def currency_obj(self):
        return Currency(self.currency)

    @property
    def base_currency_obj(self):
        return Currency(self.base_currency)


@receiver(post_save, sender=Rate)
def create_reverse_rate(sender, instance, created, **kwargs):
    """
    Create the rate object to revert rate when create a rate
    """
    if created and not Rate.objects.filter(
            user=instance.user,
            key=instance.key,
            value_date=instance.value_date,
            currency=instance.base_currency,
            base_currency=instance.currency,
    ).exists() and instance.value != 0:
        Rate.objects.create(
            user=instance.user,
            key=instance.key,
            value_date=instance.value_date,
            currency=instance.base_currency,
            base_currency=instance.currency,
            value=1 / instance.value
        )


class Amount:
    """
    Amount with a currency, a value and a date
    """
    currency = None
    amount = 0
    date_obj = None

    def __init__(self, currency: str, amount: float, date_obj: date):
        """
        Initialize amount
        """
        self.currency = currency
        self.amount = amount
        self.date_obj = date_obj

    def __repr__(self):
        """
        How do I look like
        """
        return f'{self.date_obj}: {self.currency} {self.amount}'


class RateConversionPayload:
    """
    Payload for conversion of amounts
    """
    data = None
    target = ''
    key = ''
    batch_id = ''
    eob = False

    def __init__(self, target, data=None, key=None, batch_id=None, eob=False):
        """
        Representation of the payload
        """
        self.data = data
        self.target = target
        self.key = key
        self.batch_id = batch_id
        self.eob = eob


class BulkRate:
    """
    Rate that is applied to a range of dates
    """
    base_currency = settings.BASE_CURRENCY
    currency = settings.BASE_CURRENCY
    value = 0
    key = None
    from_date = None
    to_date = None

    def __init__(
            self,
            base_currency,
            currency,
            value,
            key,
            from_date,
            to_date):
        """
        Initialize
        :param key: key for user
        :param base_currency: destination currency
        :param currency: source currency
        """
        self.base_currency = base_currency
        self.currency = currency
        self.value = value
        self.key = key
        self.from_date = from_date
        self.to_date = to_date

    def to_rates(self, user):
        """
        Create rates in the database
        """
        if not self.to_date:
            self.to_date = date.today()
        rates = []
        for i in range((self.to_date - self.from_date).days + 1):
            rate, created = Rate.objects.get_or_create(
                user=user,
                key=self.key,
                base_currency=self.base_currency,
                currency=self.currency,
                value_date=self.from_date + timedelta(i)
            )
            rate.value = self.value
            rate.save()
            rates.append(rate)
        return rates


class RateConverter(BaseConverter):
    """
    Converter of rates
    """
    base_currency = settings.BASE_CURRENCY
    cached_currencies = {}
    user = None
    key = None

    def __init__(self, user: User, id: str = None, key: str = None,
                 base_currency: str = settings.BASE_CURRENCY):
        """
        Initialize
        :param user: Django User
        :param key: key for user
        :param base_currency: destination currency
        """
        super(RateConverter, self).__init__(id=id)
        self.base_currency = base_currency
        self.user = user
        self.key = key

    def add_data(self, data: [Amount]) -> []:
        """
        Check data and add it to the dataset
        Return list of errors
        """
        errors = super(RateConverter, self).add_data(data)
        self.cache_currencies()
        return errors

    def check_data(self, data: []) -> []:
        """
        Validates that the data contains
        - currency (str)
        - amount (float)
        - date (YYYY-MM-DD)
        """
        from .serializers import RateAmountSerializer
        errors = []
        for line in data:
            serializer = RateAmountSerializer(data=line)
            if serializer.is_valid():
                self.data.append(serializer.create(serializer.validated_data))
            else:
                errors.append(serializer.errors)
        return errors

    def cache_currencies(self):
        """
        Reads currencies in data and fetches rates, put them in memory
        """
        for line in self.data:
            self.cached_currencies[line.date_obj] = \
                self.cached_currencies.get(line.date_obj) or {}
            rate = Rate.objects.rate_at_date(
                key=self.key,
                base_currency=self.base_currency,
                currency=line.currency,
                date_obj=line.date_obj)
            if rate.pk:
                self.cached_currencies[line.date_obj][line.currency] = \
                    rate.value

    def convert(self) -> ConverterResult:
        """
        Converts data to base currency
        """
        result = ConverterResult(id=self.id, target=self.base_currency)
        for amount in self.data:
            rate = self.cached_currencies.get(
                amount.date_obj, {}
            ).get(amount.currency)
            if rate:
                value = float(amount.amount) / rate
                result.increment_sum(value)
                detail = ConverterResultDetail(
                    unit=amount.currency,
                    original_value=amount.amount,
                    date=amount.date_obj,
                    conversion_rate=rate,
                    converted_value=value
                )
                result.detail.append(detail)
            else:
                error = ConverterResultError(
                    unit=amount.currency,
                    original_value=amount.amount,
                    date=amount.date_obj,
                    error=_('Rate could not be found')
                )
                result.errors.append(error)
        self.end_batch(result.end_batch())
        return result


class RateServiceFetch(models.Model):
    service = models.CharField("name of the rate fetch ing service", max_length=255)
    value_date = models.DateField("Date of the value that has been fetched")
    fetch_date = models.DateTimeField("Date of fetching", auto_created=True)


def rate_from(
        self,
        *arg,
        currency: str,
        value_date: date,
        **kwargs):
    """
    Return rate at a given date
    Used for extension of Currency without user context for GraphQL interface
    """
    if type(value_date) == str:
        date_obj = datetime.datetime.strptime(value_date, '%Y-%m-%d').date()
    elif type(value_date) == date:
        date_obj = value_date
    elif type(value_date) == datetime:
        date_obj = value_date.date()
    else:
        raise ValueError('Invalid date format')
    return Rate.objects.find_rate(
        currency=self.code,
        base_currency=currency,
        date_obj=date_obj)


def rate_to(
        self,
        *args,
        currency: str,
        value_date: date,
        **kwargs):
    """
    Return rate at a given date
    Used for extension of Currency without user context for GraphQL interface
    """
    if type(value_date) == str:
        date_obj = datetime.datetime.strptime(value_date, '%Y-%m-%d').date()
    elif type(value_date) == date:
        date_obj = value_date
    elif type(value_date) == datetime:
        date_obj = value_date.date()
    else:
        raise ValueError('Invalid date format')
    return Rate.objects.find_rate(
        base_currency=self.code,
        currency=currency,
        date_obj=date_obj)


# Add rates attribute from Currency class
setattr(Currency, 'rate_from', rate_from)
setattr(Currency, 'rate_to', rate_to)
