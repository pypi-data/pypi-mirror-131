"""
Currencies models
"""
import logging
from datetime import date
from typing import Iterator

from countryinfo import CountryInfo
from django.contrib.auth.models import User
from django.core.cache import caches
from django.db import models

from iso4217 import Currency as Iso4217

from djangophysics.countries.models import Country
from . import CURRENCY_SYMBOLS, DEFAULT_SYMBOL
from .data import CURRENCY_COUNTRIES


class CurrencyNotFoundError(Exception):
    """
    Exception for not found currency
    """
    msg = 'Currency not found'


class Currency:
    """
    Mock for hinting
    """
    pass


class Currency:
    """
    Currency class, wrapper for ISO-4217
    """
    code = None
    name = None
    currency_name = None
    exponent = None
    number = 0
    value = None

    def __init__(self, code: str):
        """
        Initialize an iso4217.Currency instance
        :param code: currency ISO 4217 code
        """
        try:
            i = Iso4217(code.upper())
            for a in ['code', 'name', 'currency_name',
                      'exponent', 'number', 'value']:
                setattr(self, a, getattr(i, a))
        except ValueError:
            raise CurrencyNotFoundError('Invalid currency code')

    @classmethod
    def search(cls, term):
        """
        Search for Contruy by name, alpha_2, alpha_3, or numeric value
        :param term: Search term
        """
        result = []
        for attr in ['code', 'name', 'currency_name', 'number', 'value']:
            result.extend(
                [getattr(c, 'code') for c in Iso4217
                 if term.lower() in str(getattr(c, attr)).lower()]
            )
        # search for symbol
        result.extend([c.code for c in Iso4217
                       if term in cls.get_symbol(c.code)])
        return sorted([Currency(r)
                       for r in set(result)], key=lambda x: x.name)

    @classmethod
    def is_valid(cls, cur: str) -> bool:
        """
        Checks if currency is part of iso4217
        """
        try:
            Currency(cur)
            return True
        except CurrencyNotFoundError:
            return False

    @classmethod
    def all_currencies(cls, ordering: str = 'name') -> Iterator[Currency]:
        """
        Returns a sorted list of currencies
        :param ordering: sort attribute
        """
        descending = False
        if ordering and ordering[0] == '-':
            ordering = ordering[1:]
            descending = True
        if ordering not in ['code', 'name', 'currency_name',
                            'exponent', 'number', 'value']:
            ordering = 'name'
        return sorted([Currency(c.code) for c in Iso4217],
                      key=lambda x: getattr(x, ordering),
                      reverse=descending)

    @property
    def countries(self) -> Iterator[Country]:
        """
        List countries using this currency
        :return: List of Country objects
        """
        a2s = CURRENCY_COUNTRIES.get(self.code, [])
        return [Country(alpha_2) for alpha_2 in a2s]

    @classmethod
    def get_for_country(cls, alpha2: str) -> Iterator[Currency]:
        """
        Return a list of currencies for an alpha2 country code
        :params alpha2: alpha2 code of a country
        """
        try:
            country = Country(alpha2)
            return [Currency(cur.code) for cur in country.currencies()]
        except CurrencyNotFoundError as e:
            logging.error("Error fetching currency")
            logging.error(e)
            return []

    def get_rates(self, user: User = None,
                  key: str = None, base_currency: str = None,
                  start_date: date = None,
                  end_date: date = None) -> Iterator:
        """
        Return a list of rates for this currency
        and an optional base currency between two dates
        :params base_currency: code of the base currency
        :params start_date: rates from that date included
        :params end_date: rates to that date included
        :return: List of rates
        """
        print("Currency get rates")
        from djangophysics.rates.models import Rate
        qs = Rate.objects.filter(currency=self.code)
        if user:
            qs = qs.filter(models.Q(user=user) | models.Q(user=None))
            if key:
                qs = qs.filter(key=key)
        if base_currency:
            qs = qs.filter(base_currency=base_currency)
        if start_date:
            qs = qs.filter(value_date__gte=start_date)
        if end_date:
            qs = qs.filter(value_date__lte=end_date)
        return qs

    @property
    def symbol(self):
        """
        Returns the symbol for this currency based on __init__.CURRENCY_SYMBOLS
        """
        return self.get_symbol(self.code)

    @staticmethod
    def get_symbol(code: str) -> str:
        """
        Get symbol for currency
        :param code: Currency code
        """
        return CURRENCY_SYMBOLS.get(code, DEFAULT_SYMBOL)
