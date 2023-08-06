"""
Units tests
"""
import uuid
from datetime import date, timedelta

import pint
from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from . import ADDITIONAL_BASE_UNITS
from .exceptions import UnitSystemNotFound, UnitDuplicateError, \
    UnitDimensionError, UnitValueError, DimensionDuplicateError, \
    DimensionValueError, DimensionDimensionError, DimensionNotFound
from .models import UnitSystem, UnitConverter, \
    Dimension, DimensionNotFound, CustomUnit, CustomDimension
from .serializers import QuantitySerializer


class DimensionTest(TestCase):
    """
    Test Dimension object
    """

    def setUp(self):
        """
        Setup test environment
        """
        self.key = uuid.uuid4()
        self.admin = User.objects.create(
            username='admin',
            email='admin@local.dev',
            is_superuser=True
        )
        self.user = User.objects.create(
            username='test',
            email='test@local.dev'
        )
        CustomUnit.objects.create(
            user=self.user,
            unit_system='SI',
            code='user_unit',
            name='User Unit',
            relation="1.5 meter",
            symbol="uun",
            alias="uun"
        )
        CustomUnit.objects.create(
            user=self.user,
            unit_system='SI',
            key=self.key,
            code='user_key_unit',
            name='User Key Unit',
            relation="1.5 meter",
            symbol="ukun",
            alias="ukun"
        )

    def test_creation(self):
        """
        Test creation of a dimension
        """
        us = UnitSystem()
        dimension = Dimension(unit_system=us, code='[length]')
        self.assertTrue(isinstance(dimension, Dimension))

    def test_bad_creation(self):
        """
        Test creation with wrong parameters
        """
        us = UnitSystem()
        self.assertRaises(DimensionNotFound, Dimension,
                          unit_system=us, code='length')

    def test_dimension_units(self):
        """
        Test listing dimension units
        """
        us = UnitSystem()
        dimension = Dimension(unit_system=us, code='[length]')
        unit_codes = [unit.code for unit in dimension.units]
        self.assertIn('meter', unit_codes)

    def test_compounded_dimension_units(self):
        """
        Test units list for [compounded] special dimension
        """
        us = UnitSystem()
        dimension = Dimension(unit_system=us, code='[compounded]')
        unit_codes = [unit.code for unit in dimension.units]
        self.assertIn('number_english', unit_codes)

    def test_custom_dimension_superuser_units(self):
        """
        Test units list for [custom] special dimension for superuser
        """
        us = UnitSystem(user=self.admin)
        dimension = Dimension(unit_system=us, code='[custom]')
        self.assertEqual(len(dimension.units), 2)

    def test_custom_dimension_superuser_key_units(self):
        """
        Test units list for [custom] dimension
        with superuser rights with a key
        """
        us = UnitSystem(user=self.admin, key=str(self.key))
        dimension = Dimension(unit_system=us, code='[custom]')
        self.assertEqual(len(dimension.units), 1)

    def test_custom_dimension_user_units(self):
        """
        Test units list for a user
        """
        us = UnitSystem(user=self.user)
        dimension = Dimension(unit_system=us, code='[custom]')
        self.assertEqual(len(dimension.units), 2)

    def test_custom_dimension_user_key_units(self):
        """
        Test units list for a user with a key
        """
        us = UnitSystem(user=self.user, key=str(self.key))
        dimension = Dimension(unit_system=us, code='[custom]')
        self.assertEqual(len(dimension.units), 1)

    def test_custom_dimension_no_user_units(self):
        """
        Test units list if no user
        """
        us = UnitSystem()
        dimension = Dimension(unit_system=us, code='[custom]')
        self.assertEqual(len(dimension.units), 0)

    def test_dimension_name(self):
        """
        Test name transformation
        """
        cd = CustomDimension.objects.create(
            user=self.user,
            key=self.key,
            unit_system='SI',
            code="[myDim]",
            name="My dimension",
            relation="[length]/[luminance]"
        )
        us = UnitSystem(user=self.user, key=str(self.key))
        dims = us.available_dimensions()
        self.assertEqual(dims['[myDim]'].name, 'My dimension')
        self.assertEqual(dims['[length]'].name, _('length'))
        self.assertEqual(dims['[esu_magnetic_dipole]'].name, 'Esu magnetic dipole')


class UnitTest(TestCase):
    """
    Test Unit object
    """

    def test_creation(self):
        """
        Test creation of Unit
        """
        us = UnitSystem()
        unit = us.unit('meter')
        self.assertTrue(isinstance(unit.unit, pint.Unit))

    def test_dimensions(self):
        """
        Test unit dimensions
        """
        us = UnitSystem()
        dimension = Dimension(unit_system=us, code='[length]')
        unit = us.unit('meter')
        self.assertIn(dimension.code, [d.code for d in unit.dimensions])

    def test_readable_dimension(self):
        """
        Test user readable dimension for unit
        """
        us = UnitSystem()
        unit = us.unit(unit_name='meter')
        self.assertEqual(unit.readable_dimension, _('length'))
        unit = us.unit(unit_name='US_international_ohm')
        self.assertEqual(
            unit.readable_dimension,
            f"{_('length')}^2 * {_('mass')} / "
            f"{_('current')}^2 / {_('time')}^3")


class UnitAPITest(TestCase):
    """
    Test Unit APIs
    """
    def test_list_request(self):
        """
        Test list of units
        """
        client = APIClient()
        response = client.get(
            '/units/mks/units/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sorted_list_request(self):
        """
        Test list with ordering
        """
        client = APIClient()
        response = client.get(
            '/units/mks/units/',
            data={
                'ordering': 'code'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Currencies are now part of the dimensions
        self.assertEqual(response.json()[0]['code'], 'AUD')

    def test_list_language_request(self):
        """
        Test requireng a translated list
        """
        client = APIClient()
        response = client.get(
            '/units/mks/units/',
            data={
                'language': 'fr'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_bad_language_request(self):
        """
        Test requiring an invalid translation
        """
        client = APIClient()
        response = client.get(
            '/units/mks/units/',
            data={
                'language': 'theta'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_per_dimension_request(self):
        """
        Test list of units grouped by dimension
        """
        client = APIClient()
        response = client.get(
            '/units/mks/units/per_dimension/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bad_list_per_dimension_request(self):
        """
        Test list of units with invalid unit system
        """
        client = APIClient()
        response = client.get(
            '/units/hello/units/per_dimension/'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_with_bad_dimension_request(self):
        """
        Test  units list with invalid dimension filter
        """
        client = APIClient()
        UnitSystem(system_name='mks')
        response = client.get(
            '/units/mks/units/',
            data={
                'dimension': '[hello]'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_with_dimension_request(self):
        """
        Test list filtered by dimension
        """
        client = APIClient()
        us = UnitSystem(system_name='mks')
        response = client.get(
            '/units/mks/units/',
            data={
                'dimension': '[length]'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()),
                         len(Dimension(unit_system=us,
                                       code='[length]').units))

    def test_list_with_domain_request(self):
        """
        Test list filtered by dimension
        """
        client = APIClient()
        response = client.get(
            '/units/SI/units/',
            data={
                'domain': 'mydomain'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_list_with_wrong_domain_request(self):
        """
        Test list filtered by dimension
        """
        client = APIClient()
        response = client.get(
            '/units/SI/units/',
            data={
                'domain': 'mywrongdomain'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

    def test_list_with_compounded_dimension_request(self):
        """
        Test list of [compounded dimension]
        """
        client = APIClient()
        us = UnitSystem(system_name='mks')
        response = client.get(
            '/units/mks/units/',
            data={
                'dimension': '[compounded]'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()),
                         len(Dimension(unit_system=us,
                                       code='[compounded]').units))

    def test_list_with_dimension_2_request(self):
        """
        Test another dimension
        """
        client = APIClient()
        us = UnitSystem(system_name='mks')
        response = client.get(
            '/units/mks/units/',
            data={
                'dimension': '[area]'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()),
                         len(Dimension(unit_system=us,
                                       code='[area]').units))

    def test_retrieve_request(self):
        """
        Test retrieve unit
        """
        client = APIClient()
        response = client.get(
            '/units/mks/units/meter/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_bad_request(self):
        """
        Test retrieve invalid unit
        """
        client = APIClient()
        response = client.get(
            '/units/mks/units/plouf/'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_compatible_request(self):
        """
        Test list compatible units
        """
        client = APIClient()
        response = client.get(
            '/units/mks/units/meter/compatible/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UnitSystemTest(TestCase):
    """
    UnitSystem tests
    """

    def setUp(self):
        """
        Setup test environment
        """
        self.user = User.objects.create(
            username='toto',
            email='toto@example.com'
        )
        self.key = uuid.uuid4()
        self.old_setting = getattr(settings, 'ADDITIONAL_UNITS', {})
        settings.PHYSICS_ADDITIONAL_UNITS = {
            'SI': {
                'my_unit': {
                    'name': 'My Unit',
                    'symbol': 'my²',
                    'relation': '0.0001 meter / meter ** 2'
                },
                'bad_unit': {
                    'name': 'Bad unit',
                    'symbol': 'All hell loose',
                    'relation': 'My tailor is rich'
                }
            }
        }  # value tested against in the TestCase
        self.custom_unit = CustomUnit.objects.create(
            user=self.user,
            key=self.key,
            unit_system='SI',
            code='myUserUnit',
            name='My User Unit',
            relation='12 kg',
            symbol='myuu',
            alias='myuserunit'
        )

    def tearDown(self):
        """
        tear down environment
        """
        settings.PHYSICS_ADDITIONAL_UNITS = self.old_setting

    def test_available_systems(self):
        """
        Test list of available unit systems
        """
        us = UnitSystem()
        available_systems = us.available_systems()
        self.assertEqual(
            available_systems,
            ['Planck', 'SI', 'US', 'atomic', 'cgs', 'imperial', 'mks'])

    def test_user_key_system(self):
        user_us = UnitSystem(system_name='SI', user=self.user, key=self.key)
        self.assertIsNotNone(user_us.unit('myUserUnit'))
        us = UnitSystem(system_name='SI')
        self.assertIsNone(us.unit('myUserUnit'))

    def test_value_date_system(self):
        today_us = UnitSystem(system_name='SI')
        last_week_us = UnitSystem(system_name='SI', value_date=date.today() - timedelta(7))
        self.assertNotEqual(
            today_us.ureg.Quantity(1, 'USD').to('EUR'),
            last_week_us.ureg.Quantity(1, 'USD').to('EUR'),
        )

    def test_available_units(self):
        """
        Test list of avaible units
        """
        us = UnitSystem(system_name='imperial')
        available_units = us.available_unit_names()
        self.assertIn('UK_hundredweight', available_units)

    def test_available_base_units(self):
        """
        Test list of availbale base units
        """
        us = UnitSystem(system_name='SI')
        available_units = us.available_unit_names()
        self.assertIn('kilogram', available_units)

    def test_available_additional_units(self):
        """
        Test list of available additional units
        """
        us = UnitSystem(system_name='SI')
        available_units = us.available_unit_names()
        self.assertIn('my_unit', available_units)

    def test_test_additional_base_units(self):
        """
        test add base units test
        """
        us = UnitSystem(system_name='SI')
        available_units = us._test_additional_units(ADDITIONAL_BASE_UNITS)
        self.assertTrue(available_units)

    def test_test_additional_units(self):
        """
        Test additionnal units addition test
        """
        us = UnitSystem(system_name='SI')
        available_units = us._test_additional_units(
            settings.PHYSICS_ADDITIONAL_UNITS)
        self.assertFalse(available_units)

    def test_available_units_different(self):
        """
        Test avaible available unitsfor another unit system
        """
        us = UnitSystem(system_name='mks')
        available_units = us.available_unit_names()
        self.assertIn('meter', available_units)
        self.assertNotIn('UK_hundredweight', available_units)
        imperial = UnitSystem(system_name='imperial')
        imperial_available_units = imperial.available_unit_names()
        self.assertIn('UK_hundredweight', imperial_available_units)

    def test_units_per_dimensionality(self):
        """
        Test listing units per dimensionality
        """
        us = UnitSystem(system_name='mks')
        upd = us.units_per_dimensionality()
        self.assertIn(_('length'), upd)

    def test_dimensionalities(self):
        """
        Test dimensionalities of a unit system
        """
        us = UnitSystem(system_name='mks')
        dims = us.dimensionalities
        self.assertIn(_('length'), dims)


class UnitSystemAPITest(TestCase):
    """
    UnitSystem API tests
    """

    def setUp(self):
        """
        Setup test environment
        """
        self.old_setting = getattr(settings, 'ADDITIONAL_UNITS', {})
        settings.PHYSICS_ADDITIONAL_UNITS = {
            'SI': {
                'my_unit': {
                    'name': 'My Unit',
                    'symbol': 'my²',
                    'relation': '0.0001 meter / meter ** 2'
                },
                'bad_unit': {
                    'name': 'Bad unit',
                    'symbol': 'All hell loose',
                    'relation': 'My tailor is rich'
                }
            }
        }  # value tested against in the TestCase

    def test_list_request(self):
        """
        Test unit system list API
        """
        client = APIClient()
        response = client.get(
            '/units/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('SI', [us['system_name'] for us in response.json()])

    def test_retrieve_request(self):
        """
        Test retrieve unit system API
        """
        client = APIClient()
        response = client.get(
            '/units/SI/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("system_name"), "SI")

    def test_list_dimensions_request(self):
        """
        Test dimensions list request
        """
        client = APIClient()
        response = client.get(
            '/units/SI/dimensions/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("[length]", [r['code'] for r in response.json()])

    def test_list_sorted_dimensions_request(self):
        """
        Test sorted dimensions request
        """
        client = APIClient()
        response = client.get(
            '/units/SI/dimensions/',
            data={
                'ordering': '-code'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("[length]", [r['code'] for r in response.json()])
        self.assertEqual(response.json()[0]['code'], '[wavenumber]')

    def test_retrieve_request_not_found(self):
        """
        Test invalid retrieve request
        """
        client = APIClient()
        response = client.get(
            '/units/sO/'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UnitConverterTest(TestCase):
    """
    Test UnitConverter object
    """
    base_system = 'SI'
    base_unit = 'meter'

    def setUp(self) -> None:
        """
        Setup environment
        """
        self.converter = UnitConverter(base_system='SI', base_unit='meter')
        self.quantities = [
            {
                'system': 'SI',
                'unit': 'furlong',
                'value': 1,
                'date_obj': '2020-07-22'
            },
            {
                'system': 'SI',
                'unit': 'yard',
                'value': 1,
                'date_obj': '2020-07-22'
            },
        ]
        self.trash_quantities = [
            {
                'system': 'si',
                'unit': 'trop',
                'value': 100,
                'date_obj': '01/01/2020'
            },
            {
                'system': 'SI',
                'unit': 'trop',
                'value': 2,
                'date_obj': '2020-07-23'
            },
            {
                'system': 'SI',
                'unit': 'meter',
                'value': 'tete',
                'date_obj': '2020-07-23'
            },
            {
                'system': 'SI',
                'unit': 'meter',
                'value': 0,
                'date_obj': '01/01/2021'
            },
        ]

    def test_created(self):
        """
        Test converter  creation
        """
        self.assertEqual(self.converter.status,
                         self.converter.INITIATED_STATUS)

    def test_add_data(self):
        """
        Test adding data to a converter
        """
        errors = self.converter.add_data(self.quantities)
        self.assertEqual(errors, [])
        self.assertEqual(self.converter.status,
                         self.converter.INSERTING_STATUS)
        self.assertIsNotNone(cache.get(self.converter.id))

    def test_trash_quantities(self):
        """
        Test adding trash to a converter
        """
        converter = UnitConverter(base_system='SI', base_unit='meter')
        errors = converter.add_data(self.trash_quantities)
        self.assertEqual(len(errors), 3)
        self.assertIn("system", errors[0])
        self.assertIn("value", errors[1])
        self.assertIn("date_obj", errors[2])

    def test_add_empty_data(self):
        """
        Test adding empty values to a converter
        """
        converter = UnitConverter(base_system='SI', base_unit='meter')
        errors = converter.add_data(data=None)
        self.assertEqual(len(errors), 1)

    def test_convert(self):
        """
        Test conversion
        """
        result = self.converter.convert()
        self.assertEqual(result.id, self.converter.id)
        self.assertEqual(result.target, 'meter')
        self.assertEqual(self.converter.status, self.converter.FINISHED)
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.detail), len(self.converter.data))
        converted_sum = sum([d.converted_value for d in result.detail])
        self.assertEqual(result.sum, converted_sum)


class UnitConverterAPITest(TestCase):
    """
    Test UnitConverter API object
    """
    base_system = 'SI'
    base_unit = 'meter'

    def setUp(self) -> None:
        """
        Setup environment
        """
        self.converter = UnitConverter(base_system='SI', base_unit='meter')
        self.quantities = [
            {
                'system': 'SI',
                'unit': 'furlong',
                'value': 1,
                'date_obj': '2020-07-22'
            },
            {
                'system': 'SI',
                'unit': 'yard',
                'value': 1,
                'date_obj': '2020-07-22'
            },
        ]
        self.trash_quantities = [
            {
                'system': 'si',
                'unit': 'trop',
                'value': 100,
                'date_obj': '01/01/2020'
            },
            {
                'system': 'SI',
                'unit': 'trop',
                'value': 2,
                'date_obj': '2020-07-23'
            },
            {
                'system': 'SI',
                'unit': 'meter',
                'value': 'tete',
                'date_obj': '2020-07-23'
            },
            {
                'system': 'SI',
                'unit': 'meter',
                'value': 0,
                'date_obj': '01/01/2021'
            },
        ]

    def test_convert_request(self):
        """
        Test conversion API
        """
        quantities = QuantitySerializer(self.quantities, many=True)
        client = APIClient()
        response = client.post(
            '/units/convert/',
            data={
                'data': quantities.data,
                'base_system': 'SI',
                'base_unit': 'meter'
            },
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('sum', response.json())
        self.assertEqual(len(response.json().get('detail')),
                         len(self.quantities))

    def test_convert_batch_request(self):
        """
        Test batch conversion
        """
        batch_id = uuid.uuid4()
        client = APIClient()
        quantities = QuantitySerializer(self.quantities, many=True)
        response = client.post(
            '/units/convert/',
            data={
                'data': quantities.data,
                'base_system': 'SI',
                'base_unit': 'meter',
                'batch_id': batch_id,
            },
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', response.json())
        self.assertEqual(response.json().get('status'),
                         UnitConverter.INSERTING_STATUS)
        self.assertEqual(response.json().get('id'), str(batch_id))
        response = client.post(
            '/units/convert/',
            data={
                'data': quantities.data,
                'batch_id': batch_id,
                'base_system': 'SI',
                'base_unit': 'meter',
                'eob': True
            },
            format='json')
        self.assertEqual(response.json().get('status'),
                         UnitConverter.FINISHED)
        self.assertEqual(len(response.json().get('detail')),
                         2 * len(self.quantities))

    def test_watch_request(self):
        """
        Test observation of a batch
        """
        batch_id = uuid.uuid4()
        client = APIClient()
        quantities = QuantitySerializer(self.quantities, many=True)
        response = client.post(
            '/units/convert/',
            data={
                'data': quantities.data,
                'base_system': 'SI',
                'base_unit': 'meter',
                'batch_id': batch_id,
            },
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', response.json())
        self.assertEqual(response.json().get('status'),
                         UnitConverter.INSERTING_STATUS)
        self.assertEqual(response.json().get('id'), str(batch_id))
        response = client.get(
            f'/watch/{str(batch_id)}/',
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('status'),
                         UnitConverter.INSERTING_STATUS)
        self.assertEqual(response.json().get('id'), str(batch_id))


class CustomDimensionTest(TestCase):
    """
    CustomDimension tests
    """

    def setUp(self) -> None:
        """
        Setup environment
        """
        self.user, created = User.objects.get_or_create(
            username='test',
            email='test@ipd.com'
        )
        self.user.set_password('test')
        self.user.save()
        Token.objects.create(user=self.user)
        self.key = uuid.uuid4()

    def test_creation(self):
        """
        Test creation of a CustomDimension
        """
        cd = CustomDimension.objects.create(
            user=self.user,
            key=self.key,
            unit_system='SI',
            code='[my_dimension]',
            name='My Dimension',
            relation="[time] * [length]")
        self.assertEqual(cd.user, self.user)
        self.assertEqual(cd.key, self.key)
        self.assertEqual(cd.unit_system, 'SI')
        self.assertEqual(cd.code, '[my_dimension]')
        self.assertEqual(cd.name, 'My Dimension')
        self.assertEqual(cd.relation, '[time] * [length]')
        self.assertEqual(
            CustomDimension.objects.filter(
                user=self.user, key=self.key,
                unit_system='SI', code='[my_dimension]').count(),
            1)
        us = UnitSystem(system_name='SI', user=self.user, key=self.key)
        self.assertIn('[my_dimension]', us.available_dimension_names())
        self.assertIn('[my_dimension]', us.available_dimensions().keys())

    def test_unit_assignment(self):
        """
        Test units associated with the custom dimension
        """
        cd = CustomDimension.objects.create(
            user=self.user,
            key=self.key,
            unit_system='SI',
            code='[my_dimension]',
            name='My Dimension',
            relation="[time] * [length]")
        cu = CustomUnit.objects.create(
            user=self.user,
            key=self.key,
            unit_system='SI',
            code='my_unit',
            name='My Unit',
            relation="1.5 hour * meter",
            symbol="myu",
            alias="myu")
        us = UnitSystem(system_name='SI', user=self.user, key=self.key)
        dim = Dimension(unit_system=us, code='[my_dimension]')
        self.assertIn('my_unit', [u.code for u in dim.units])

    def test_creation_with_dash(self):
        """
        Test creation of a CustomDimension with - in code
        """
        cd = CustomDimension.objects.create(
            user=self.user,
            key=self.key,
            unit_system='SI',
            code='[my-dimension]',
            name='My Dimension',
            relation="[time] * [length]"
        )
        self.assertEqual(cd.user, self.user)
        self.assertEqual(cd.key, self.key)
        self.assertEqual(cd.unit_system, 'SI')
        self.assertEqual(cd.code, '[my_dimension]')
        self.assertEqual(cd.name, 'My Dimension')
        self.assertEqual(cd.relation, '[time] * [length]')
        self.assertEqual(
            CustomDimension.objects.filter(
                user=self.user, key=self.key,
                unit_system='SI', code='[my_dimension]').count(),
            1)

    def test_creation_with_wrong_dimension(self):
        """
        Test creation of a CustomUnit with - in code, symbol and alias
        """
        self.assertRaises(
            DimensionDimensionError,
            CustomDimension.objects.create,
            user=self.user,
            key=self.key,
            unit_system='SI',
            code='[my_dimension]',
            name='My Dimension',
            relation="[time] * [space]"
        )

    def test_invalid_creation_params(self):
        """
        Test invalid creation params
        """
        self.assertRaises(
            UnitSystemNotFound,
            CustomDimension.objects.create,
            user=self.user,
            key=self.key,
            unit_system='SO',
            code='[my_dimension]',
            name='My Dimension',
            relation="[time] * [length]"
        )

    def test_duplicate_dimension_params(self):
        """
        Test duplicated unit
        """
        self.assertRaises(
            DimensionDuplicateError,
            CustomDimension.objects.create,
            user=self.user,
            key=self.key,
            unit_system='SI',
            code='[length]',
            name='My Dimension',
            relation="[length]"
        )

    def test_duplicate_dimension_relation_params(self):
        """
        Test duplicated unit
        """
        self.assertRaises(
            DimensionDuplicateError,
            CustomDimension.objects.create,
            user=self.user,
            key=self.key,
            unit_system='SI',
            code='[mojo]',
            name='My Dimension',
            relation="[length]"
        )


class CustomDimensionAPITest(TestCase):
    """
    CustomUnit API tests
    """

    def setUp(self) -> None:
        """
        Setup environment
        """
        self.user, created = User.objects.get_or_create(
            username='test',
            email='test@ipd.com'
        )
        self.user.set_password('test')
        self.user.save()
        Token.objects.create(user=self.user)
        self.key = uuid.uuid4()

    def test_list_request(self):
        """
        Test list of custom dimensions
        """
        client = APIClient()
        response = client.get(
            '/units/SI/dimensions/custom/',
            format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_connected_list_request(self):
        """
        Test list of custom dimensions with connected user
        """
        client = APIClient()
        token = Token.objects.get(user__username=self.user.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        post_response = client.post(
            '/units/SI/dimensions/custom/',
            data={
                'code': '[my_dimension]',
                'name': 'My Dimension',
                'relation': "[energy] / [time]"
            }
        )
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertIn('code', post_response.json())
        response = client.get(
            '/units/SI/dimensions/custom/',
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if 'results' in response.json():
            # Paginated results
            self.assertEqual(len(response.json()['results']), 1)
            self.assertEqual(response.json()['results'][0]['code'],
                             '[my_dimension]')
        else:
            # Non paginated results
            self.assertEqual(len(response.json()), 1)
            self.assertEqual(response.json()[0]['code'], '[my_dimension]')

    def test_connected_duplicate_post(self):
        """
        Test list of custom dimensions with connected user
        """
        client = APIClient()
        token = Token.objects.get(user__username=self.user.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        post_response = client.post(
            '/units/SI/dimensions/custom/',
            data={
                'code': '[my_dimension]',
                'name': 'My Dimension',
                'relation': "[energy] / [time]"
            }
        )
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertIn('code', post_response.json())
        post_response = client.post(
            '/units/SI/dimensions/custom/',
            data={
                'code': '[my_dimension]',
                'name': 'My Dimension',
                'relation': "[energy] / [time]"
            }
        )
        self.assertEqual(post_response.status_code, status.HTTP_409_CONFLICT)

    def test_connected_unit_system_request(self):
        """
        Test list of custom dimensions with connected user
        """
        client = APIClient()
        token = Token.objects.get(user__username=self.user.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        post_response = client.post(
            '/units/SI/dimensions/custom/',
            data={
                'code': '[my_dimension]',
                'name': 'My Dimension',
                'relation': "[energy] / [time]"
            }
        )
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertIn('code', post_response.json())
        response = client.get(
            '/units/SI/dimensions/custom/',
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if 'results' in response.json():
            # Paginated results
            self.assertEqual(len(response.json()['results']), 1)
            self.assertEqual(response.json()['results'][0]['code'],
                             '[my_dimension]')
        else:
            # Non paginated results
            self.assertEqual(len(response.json()), 1)
            self.assertEqual(response.json()[0]['code'], '[my_dimension]')
        response = client.get(
            '/units/mks/dimensions/custom/',
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if 'results' in response.json():
            # Paginated results
            self.assertEqual(len(response.json()['results']), 0)
        else:
            # Non paginated results
            self.assertEqual(len(response.json()), 0)

    def test_connected_list_key_request(self):
        """
        Test list of custom dimensions with connected user and a key
        """
        client = APIClient()
        token = Token.objects.get(user__username=self.user.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        post_response = client.post(
            '/units/SI/dimensions/custom/',
            data={
                'key': self.key,
                'code': '[my_dimension]',
                'name': 'My Dimension',
                'relation': "[energy] / [time]"
            }
        )
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertIn('code', post_response.json())
        response = client.get(
            '/units/SI/dimensions/custom/',
            data={'key': self.key},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if 'results' in response.json():
            # Paginated results
            self.assertEqual(len(response.json()['results']), 1)
            self.assertEqual(response.json()['results'][0]['code'],
                             '[my_dimension]')
        else:
            # Non paginated results
            self.assertEqual(len(response.json()), 1)
            self.assertEqual(response.json()[0]['code'], '[my_dimension]')

    def test_connected_dimension_list_request(self):
        """
        Test list of dimensions with custom dimension and connected user
        """
        CustomDimension.objects.create(
            user=self.user,
            key=self.key,
            unit_system='SI',
            code='[ny_dimension]',
            name='Ny Dimension',
            relation="[energy] / [mass] * [time]")
        client = APIClient()
        token = Token.objects.get(user__username=self.user.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(
            '/units/SI/dimensions/',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if 'results' in response.json():
            self.assertIn('[ny_dimension]', [u['code']
                                      for u in response.json()['results']])
        else:
            self.assertIn('[ny_dimension]',
                          [u['code'] for u in response.json()])

    def test_connected_dimension_list_2_request(self):
        """
        Another test of a list of dimensions with a custom dimension
        """
        new_key = uuid.uuid4()
        CustomDimension.objects.create(
            user=self.user,
            key=self.key,
            unit_system='SI',
            code='[ny_dimension]',
            name='Ny Dimension',
            relation="[energy] * [conductance] / [time]")
        CustomDimension.objects.create(
            user=self.user,
            key=new_key,
            unit_system='SI',
            code='[py_dimension]',
            name='Py Dimension',
            relation="[energy] * [conductance] / [length]")
        client = APIClient()
        token = Token.objects.get(user__username=self.user.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(
            '/units/SI/dimensions/',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if 'results' in response.json():
            self.assertIn('[ny_dimension]', [u['code']
                                      for u in response.json()['results']])
            self.assertIn('[py_dimension]', [u['code']
                                      for u in response.json()['results']])
        else:
            self.assertIn('[ny_dimension]', [u['code'] for u in response.json()])
            self.assertIn('[py_dimension]', [u['code'] for u in response.json()])

    def test_connected_dimension_list_new_key_request(self):
        """
        Test key isolation
        """
        new_key = uuid.uuid4()
        CustomDimension.objects.create(
            user=self.user,
            key=self.key,
            unit_system='SI',
            code='[ny_dimension]',
            name='Ny Unit',
            relation="[time] * [temperature] * [length]")
        CustomDimension.objects.create(
            user=self.user,
            key=new_key,
            unit_system='SI',
            code='[py_dimension]',
            name='Py Dimension',
            relation="[volume] / [area]")
        client = APIClient()
        token = Token.objects.get(user__username=self.user.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(
            '/units/SI/dimensions/custom/',
            data={
                'key': new_key
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if 'results' in response.json():
            self.assertNotIn('[ny_dimension]', [u['code']
                                             for u in response.json()['results']])
            self.assertIn('[py_dimension]', [u['code']
                                             for u in response.json()['results']])
        else:
            self.assertNotIn('[ny_dimension]', [u['code'] for u in response.json()])
            self.assertIn('[py_dimension]', [u['code'] for u in response.json()])



    def test_connected_dimension_list_self_key_request(self):
        """
        Another isolation test
        """
        new_key = uuid.uuid4()
        CustomDimension.objects.create(
            user=self.user,
            key=self.key,
            unit_system='SI',
            code='[ny_dimension]',
            name='Ny Dimension',
            relation="[time] * [length]")
        CustomDimension.objects.create(
            user=self.user,
            key=new_key,
            unit_system='SI',
            code='[py_dimension]',
            name='Py Dimension',
            relation="[conductance] * [resistance]")
        client = APIClient()
        token = Token.objects.get(user__username=self.user.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(
            '/units/SI/dimensions/custom/',
            data={
                'key': self.key
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if 'results' in response.json():
            self.assertIn('[ny_dimension]', [u['code']
                                                for u in response.json()['results']])
            self.assertNotIn('[py_dimension]', [u['code']
                                             for u in response.json()['results']])
        else:
            self.assertIn('[ny_dimension]', [u['code'] for u in response.json()])
            self.assertNotIn('[py_dimension]', [u['code'] for u in response.json()])


class CustomUnitTest(TestCase):
    """
    CustomUnit tests
    """

    def setUp(self) -> None:
        """
        Setup environment
        """
        self.user, created = User.objects.get_or_create(
            username='test',
            email='test@ipd.com'
        )
        self.user.set_password('test')
        self.user.save()
        Token.objects.create(user=self.user)
        self.key = uuid.uuid4()

    def test_creation(self):
        """
        Test creation of a CustomUnit
        """
        cu = CustomUnit.objects.create(
            user=self.user,
            key=self.key,
            unit_system='SI',
            code='my_unit',
            name='My Unit',
            relation="1.5 meter",
            symbol="myu",
            alias="myu")
        self.assertEqual(cu.user, self.user)
        self.assertEqual(cu.key, self.key)
        self.assertEqual(cu.unit_system, 'SI')
        self.assertEqual(cu.code, 'my_unit')
        self.assertEqual(cu.name, 'My Unit')
        self.assertEqual(cu.relation, '1.5 meter')
        self.assertEqual(cu.symbol, 'myu')
        self.assertEqual(cu.alias, 'myu')
        self.assertEqual(
            CustomUnit.objects.filter(
                user=self.user, key=self.key,
                unit_system='SI', code='my_unit').count(),
            1)

    def test_creation_with_dash(self):
        """
        Test creation of a CustomUnit with - in code, symbol and alias
        """
        cu = CustomUnit.objects.create(
            user=self.user,
            key=self.key,
            unit_system='SI',
            code='my-unit',
            name='My Unit',
            relation="1.5 meter",
            symbol="m-yu",
            alias="m-yu")
        self.assertEqual(cu.user, self.user)
        self.assertEqual(cu.key, self.key)
        self.assertEqual(cu.unit_system, 'SI')
        self.assertEqual(cu.code, 'my_unit')
        self.assertEqual(cu.name, 'My Unit')
        self.assertEqual(cu.relation, '1.5 meter')
        self.assertEqual(cu.symbol, 'm_yu')
        self.assertEqual(cu.alias, 'm_yu')
        self.assertEqual(
            CustomUnit.objects.filter(
                user=self.user, key=self.key,
                unit_system='SI', code='my_unit').count(),
            1)

    def test_invalid_creation_params(self):
        """
        Test invalid creation params
        """
        self.assertRaises(
            UnitSystemNotFound,
            CustomUnit.objects.create,
            user=self.user,
            key=self.key,
            unit_system='SO',
            code='my_unit',
            name='My Unit',
            relation="1.5 meter",
            symbol="myu",
            alias="myu"
        )

    def test_duplicate_unit_params(self):
        """
        Test duplicated unit
        """
        self.assertRaises(
            UnitDuplicateError,
            CustomUnit.objects.create,
            user=self.user,
            key=self.key,
            unit_system='SI',
            code='meter',
            name='My Unit',
            relation="1.5 meter",
            symbol="myu",
            alias="myu"
        )

    def test_inception_unit_params(self):
        """
        Test duplicated unit
        """
        self.assertRaises(
            UnitValueError,
            CustomUnit.objects.create,
            user=self.user,
            key=self.key,
            unit_system='SI',
            code='inception',
            name='My Inception',
            relation="1.5 inception",
            symbol="inc",
            alias="inc"
        )

    def test_wrong_dimensionality_unit_params(self):
        """
        Test unit creation with wrong dimensionality
        """
        self.assertRaises(
            UnitDimensionError,
            CustomUnit.objects.create,
            user=self.user,
            key=self.key,
            unit_system='SI',
            code='my_unit',
            name='My Unit',
            relation="1.5 brouzouf",
            symbol="myu",
            alias="myu"
        )


class CustomUnitAPITest(TestCase):
    """
    CustomUnit API tests
    """

    def setUp(self) -> None:
        """
        Setup environment
        """
        self.user, created = User.objects.get_or_create(
            username='test',
            email='test@ipd.com'
        )
        self.user.set_password('test')
        self.user.save()
        Token.objects.create(user=self.user)
        self.key = uuid.uuid4()

    def test_list_request(self):
        """
        Test list of custom units
        """
        client = APIClient()
        response = client.get(
            '/units/SI/custom/',
            format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_connected_list_request(self):
        """
        Test list of custom units with connected user
        """
        client = APIClient()
        token = Token.objects.get(user__username=self.user.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        post_response = client.post(
            '/units/SI/custom/',
            data={
                'code': 'my_unit',
                'name': 'My Unit',
                'relation': "1.5 meter",
                'symbol': "myu"
            }
        )
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertIn('code', post_response.json())
        response = client.get(
            '/units/SI/custom/',
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if 'results' in response.json():
            # Paginated results
            self.assertEqual(len(response.json()['results']), 1)
            self.assertEqual(response.json()['results'][0]['code'], 'my_unit')
        else:
            # Non paginated results
            self.assertEqual(len(response.json()), 1)
            self.assertEqual(response.json()[0]['code'], 'my_unit')

    def test_connected_duplicate_post(self):
        """
        Test list of custom units with connected user
        """
        client = APIClient()
        token = Token.objects.get(user__username=self.user.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        post_response = client.post(
            '/units/SI/custom/',
            data={
                'code': 'my_unit',
                'name': 'My Unit',
                'relation': "1.5 meter",
                'symbol': "myu"
            }
        )
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertIn('code', post_response.json())
        post_response = client.post(
            '/units/SI/custom/',
            data={
                'code': 'my_unit',
                'name': 'My Unit',
                'relation': "1.5 meter",
                'symbol': "myu"
            }
        )
        self.assertEqual(post_response.status_code, status.HTTP_409_CONFLICT)

    def test_connected_unit_system_request(self):
        """
        Test list of custom units with connected user
        """
        client = APIClient()
        token = Token.objects.get(user__username=self.user.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        post_response = client.post(
            '/units/SI/custom/',
            data={
                'code': 'my_unit',
                'name': 'My Unit',
                'relation': "1.5 meter",
                'symbol': "myu"
            }
        )
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertIn('code', post_response.json())
        response = client.get(
            '/units/SI/custom/',
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if 'results' in response.json():
            # Paginated results
            self.assertEqual(len(response.json()['results']), 1)
            self.assertEqual(response.json()['results'][0]['code'], 'my_unit')
        else:
            # Non paginated results
            self.assertEqual(len(response.json()), 1)
            self.assertEqual(response.json()[0]['code'], 'my_unit')
        response = client.get(
            '/units/mks/custom/',
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if 'results' in response.json():
            # Paginated results
            self.assertEqual(len(response.json()['results']), 0)
        else:
            # Non paginated results
            self.assertEqual(len(response.json()), 0)

    def test_connected_list_key_request(self):
        """
        Test list of custom units with connected user and a key
        """
        client = APIClient()
        token = Token.objects.get(user__username=self.user.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        post_response = client.post(
            '/units/SI/custom/',
            data={
                'key': self.key,
                'code': 'my_unit',
                'name': 'My Unit',
                'relation': "1.5 meter",
                'symbol': "myu",
                'alias': "myu"
            }
        )
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertIn('code', post_response.json())
        response = client.get(
            '/units/SI/custom/',
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if 'results' in response.json():
            # Paginated results
            self.assertEqual(len(response.json()['results']), 1)
            self.assertEqual(response.json()['results'][0]['code'], 'my_unit')
        else:
            # Non paginated results
            self.assertEqual(len(response.json()), 1)
            self.assertEqual(response.json()[0]['code'], 'my_unit')

    def test_connected_unit_creation_with_dimension(self):
        """
        Test creation of a unit with correct dimension
        """
        client = APIClient()
        token = Token.objects.get(user__username=self.user.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        post_response = client.post(
            '/units/SI/custom/',
            data={
                'key': self.key,
                'code': 'my_unit',
                'name': 'My Unit',
                'relation': "1.5 meter",
                'symbol': "myu",
                'alias': "myu",
                'dimension': '[length]'
            }
        )
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertIn('code', post_response.json())
        response = client.get(
            '/units/SI/custom/',
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if 'results' in response.json():
            # Paginated results
            self.assertEqual(len(response.json()['results']), 1)
            self.assertEqual(response.json()['results'][0]['code'], 'my_unit')
        else:
            # Non paginated results
            self.assertEqual(len(response.json()), 1)
            self.assertEqual(response.json()[0]['code'], 'my_unit')

    def test_connected_unit_creation_with_wrong_dimension(self):
        """
        Test creation of a unnit with an incompatible dimension
        """
        client = APIClient()
        token = Token.objects.get(user__username=self.user.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        post_response = client.post(
            '/units/SI/custom/',
            data={
                'key': self.key,
                'code': 'my_unit',
                'name': 'My Unit',
                'relation': "1.5 meter",
                'symbol': "myu",
                'alias': "myu",
                'dimension': '[time]'
            }
        )
        self.assertEqual(post_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_connected_unit_creation_with_new_dimension(self):
        """
        Test creation of a unit and association with a new dimension
        """
        client = APIClient()
        token = Token.objects.get(user__username=self.user.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        post_response = client.post(
            '/units/SI/custom/',
            data={
                'key': self.key,
                'code': 'my_unit',
                'name': 'My Unit',
                'relation': "1.5 meter * hour / kelvin",
                'symbol': "myu",
                'alias': "myu",
                'dimension': '[new_dim]'
            }
        )
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        us = UnitSystem(system_name='SI', user=self.user, key=self.key)
        response = client.get(
            '/units/SI/units/',
            data={
                'key': self.key,
                'dimension': '[new_dim]'
            }
        )
        self.assertEqual(response.json()[0]['code'], 'my_unit')


    def test_connected_unit_list_request(self):
        """
        Test list of units with custom unit and connected user
        """
        CustomUnit.objects.create(
            user=self.user,
            key=self.key,
            unit_system='SI',
            code='ny_unit',
            name='Ny Unit',
            relation="1.5 meter",
            symbol="nyu",
            alias="nnyu")
        client = APIClient()
        token = Token.objects.get(user__username=self.user.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(
            '/units/SI/units/',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if 'results' in response.json():
            self.assertIn('ny_unit', [u['code']
                                      for u in response.json()['results']])
        else:
            self.assertIn('ny_unit', [u['code'] for u in response.json()])

    def test_connected_unit_list_2_request(self):
        """
        Another test of a list of units with a custom unit
        """
        new_key = uuid.uuid4()
        CustomUnit.objects.create(
            user=self.user,
            key=self.key,
            unit_system='SI',
            code='ny_unit',
            name='Ny Unit',
            relation="1.5 meter",
            symbol="nyu",
            alias="nnyu")
        CustomUnit.objects.create(
            user=self.user,
            key=new_key,
            unit_system='SI',
            code='py_unit',
            name='Py Unit',
            relation="1.5 meter",
            symbol="pyu",
            alias="pnyu")
        client = APIClient()
        token = Token.objects.get(user__username=self.user.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(
            '/units/SI/units/',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if 'results' in response.json():
            self.assertIn('ny_unit', [u['code']
                                      for u in response.json()['results']])
            self.assertIn('py_unit', [u['code']
                                      for u in response.json()['results']])
        else:
            self.assertIn('ny_unit', [u['code'] for u in response.json()])
            self.assertIn('py_unit', [u['code'] for u in response.json()])

    def test_connected_unit_list_new_key_request(self):
        """
        Test key isolation
        """
        new_key = uuid.uuid4()
        CustomUnit.objects.create(
            user=self.user,
            key=self.key,
            unit_system='SI',
            code='ny_unit',
            name='Ny Unit',
            relation="1.5 meter",
            symbol="nyu",
            alias="nnyu")
        CustomUnit.objects.create(
            user=self.user,
            key=new_key,
            unit_system='SI',
            code='py_unit',
            name='Py Unit',
            relation="1.5 meter",
            symbol="pyu",
            alias="pnyu")
        client = APIClient()
        token = Token.objects.get(user__username=self.user.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(
            '/units/SI/units/',
            data={
                'key': new_key
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if 'results' in response.json():
            self.assertNotIn('ny_unit', [u['code']
                                         for u in response.json()['result']])
            self.assertIn('py_unit', [u['code']
                                      for u in response.json()['result']])
        else:
            self.assertNotIn('ny_unit', [u['code'] for u in response.json()])
            self.assertIn('py_unit', [u['code'] for u in response.json()])

    def test_connected_unit_list_self_key_request(self):
        """
        Another isolation test
        """
        new_key = uuid.uuid4()
        CustomUnit.objects.create(
            user=self.user,
            key=self.key,
            unit_system='SI',
            code='ny_unit',
            name='Ny Unit',
            relation="1.5 meter",
            symbol="nyu",
            alias="nnyu")
        CustomUnit.objects.create(
            user=self.user,
            key=new_key,
            unit_system='SI',
            code='py_unit',
            name='Py Unit',
            relation="1.5 meter",
            symbol="pyu",
            alias="pnyu")
        client = APIClient()
        token = Token.objects.get(user__username=self.user.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(
            '/units/SI/units/',
            data={
                'key': self.key
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if 'results' in response.json():
            self.assertIn('ny_unit', [u['code']
                                      for u in response.json()['result']])
            self.assertNotIn('py_unit', [u['code']
                                         for u in response.json()['result']])
        else:
            self.assertIn('ny_unit', [u['code'] for u in response.json()])
            self.assertNotIn('py_unit', [u['code'] for u in response.json()])
