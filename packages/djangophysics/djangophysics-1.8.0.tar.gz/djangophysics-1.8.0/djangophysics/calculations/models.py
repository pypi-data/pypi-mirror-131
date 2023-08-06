"""
Calculations models
"""

import re
import uuid
from datetime import date
from itertools import groupby

import pint.systems
import uncertainties
from django.contrib.auth.models import User
from sympy import sympify, SympifyError

from djangophysics.converters.models import BaseConverter, ConverterLoadError
from djangophysics.units.exceptions import DimensionNotFound, UnitSystemNotFound
from djangophysics.units.models import UnitSystem, Dimension
from .exceptions import ExpressionCalculatorInitError


class Operand:
    """
    Operand in a formula
    """
    name = None
    value = None
    unit = None
    uncertainty = None

    def __init__(self,
                 name: str = None,
                 value: float = 0,
                 unit: str = None,
                 uncertainty: str = None):
        """
        Initialize Operand
        :param name: name of the operand that appears in the formula
        :param value: float magnitude
        :param unit: units
        """
        self.name = name
        self.value = value
        self.unit = unit
        self.uncertainty = uncertainty
        if self.validate():
            self.uvalue = uncertainties.ufloat(value, self.parse_uncertainty())
        else:
            self.uvalue = uncertainties.ufloat(0, 0)

    def validate(self):
        """
        Validate operand
        """
        if not self.name or self.value is None or self.unit is None:
            return False
        try:
            float(self.value)
        except ValueError:
            return False
        try:
            self.parse_uncertainty()
        except (ValueError, AttributeError):
            return False
        return True

    def get_unit(self, unit_system: UnitSystem) -> str:
        """
        Transform unit if unit is a dimension
        """
        # Find dimensions
        exp = r'(?P<dim>\[(?:\w+)*\])'
        replace_dict = {}
        for dimension_name in re.findall(exp, self.unit):
            if dimension_name == '[dimensionless]' or dimension_name == '[]':
                return ''
            try:
                dim = Dimension(unit_system=unit_system, code=dimension_name)
                replace_dict[dimension_name] = str(dim.units.pop())
            except DimensionNotFound:
                pass
        # Replace in formula
        for key, item in replace_dict.items():
            self.unit = self.unit.replace(key, item)
        return self.unit

    def expr(self, unit_system: UnitSystem) -> str:
        """
        return expression of the operand
        """
        return f"({self.value} {self.get_unit(unit_system)})"

    def get_magnitude(self) -> float:
        """
        Get magnitude of the operand
        """
        return self.uvalue.n

    def get_uncertainty(self) -> float:
        """
        Get the value of uncertainty
        """
        return self.uvalue.s

    def parse_uncertainty(self) -> float:
        """
        Transform uncertainty into absolute float value
        """
        if not self.uncertainty:
            return 0
        if self.uncertainty.endswith('%'):
            return self.value * float(self.uncertainty[:-1]) * 0.01
        else:
            return float(self.uncertainty)


class ComputationError(Exception):
    pass


class Dimensionality:
    """
    Dimensionality class. Represents the dimension and the exponent of the
    dimension
    """
    code = None
    multiplicity = None

    def __init__(self, dimension_code: str, multiplicity: float):
        """
        Initialize Dimensionality
        :param dimension_code: Code of the dimension
        :param multiplicity: multiplicity of the dimension
        """
        self.code = dimension_code
        self.multiplicity = multiplicity


class Expression:
    """
    Expression with operands
    """
    exp_id = None
    value_date = None
    expression = None
    operands = None
    out_units = None

    def __init__(
            self,
            expression: str,
            operands: [Operand],
            exp_id: str,
            value_date: date = date.today(),
            out_units: str = None):
        """
        Initialize Expression
        :param expression: string expression with placeholders
        :param operands: List of Operand corresponding to placeholders
        """
        self.exp_id = exp_id
        self.value_date = value_date
        self.expression = expression
        self.operands = operands
        self.out_units = out_units

    def _validate_syntax(self, unit_system: UnitSystem) -> (bool, str):
        """
        Syntactic validation of the expression
        :param unit_system: UnitSystem
        """
        if not self.expression:
            return False, "missing expression"
        try:
            sympify(
                self.expression.format(**{
                    v.name: v.value for v in self.operands}))
        except SympifyError:
            return False, "Improper expression"
        return True, ""

    def _validate_dimension(
            self, unit_system: UnitSystem
    ) -> (bool, str):
        """
        Validate dimensionality of an expression
        :param unit_system: UnitSystem to use
        """
        q_ = unit_system.ureg.Quantity
        kwargs = {v.name: q_(v.value, v.get_unit(unit_system=unit_system))
                  for v in self.operands}
        try:
            result = unit_system.ureg.parse_expression(
                self.expression, **kwargs
            )
        except KeyError:
            return False, "Missing operand"
        except pint.errors.DimensionalityError:
            return False, "Incoherent dimensions"
        if self.out_units:
            try:
                result.to(self.out_units)
            except pint.errors.DimensionalityError:
                return False, "Incoherent output dimensions"
        return True, ''

    def validate(self, unit_system: UnitSystem) -> (bool, []):
        """
        Validate syntax and homogeneity
        :param unit_system: UnitSystem
        """
        errors = []
        valid_expression, error = self._validate_syntax(
            unit_system=unit_system
        )
        if not valid_expression:
            errors.append({"syntax": error})
        for var in self.operands:
            if not var.validate():
                errors.append({"operand": "invalid operand"})
        valid_dimension, error = self._validate_dimension(
            unit_system=unit_system
        )
        if not valid_dimension:
            errors.append({"dimension": error})
        if errors:
            return False, errors
        return True, ''

    def dimensionality(self, unit_system: UnitSystem) -> [Dimensionality]:
        """
        Return dimensions list of an expression
        """
        q_ = unit_system.ureg.Quantity
        is_valid, error = self.validate(
            unit_system=unit_system
        )
        if not is_valid:
            return []
        if self.out_units:
            return [{'code': key, 'multiplicity': value} for key, value in q_(
                1, self.out_units
            ).dimensionality.items()]
        else:
            kwargs = {v.name: q_(v.uvalue, v.get_unit(unit_system))
                      for v in self.operands}
            result = unit_system.ureg.parse_expression(
                self.expression, **kwargs
            )
            return [{'code': key, 'multiplicity': value}
                    for key, value in result.dimensionality.items()]

    def evaluate(self, unit_system: UnitSystem) -> pint.Quantity:
        """
        Validate formula
        """
        q_ = unit_system.ureg.Quantity
        is_valid, error = self.validate(unit_system=unit_system)
        if is_valid:
            kwargs = {v.name: q_(v.uvalue, v.unit) for v in self.operands}
            result = unit_system.ureg.parse_expression(
                self.expression, **kwargs
            )
            if self.out_units:
                return result.to(self.out_units)
            else:
                return result
        else:
            raise ComputationError(f"Invalid formula: {error}")


class CalculationPayload:
    """
    Calculation payload: caculate expressions
    """
    data = None
    value_date = None
    unit_system = ''
    user = ''
    key = ''
    batch_id = ''
    eob = False

    def __init__(
            self,
            unit_system: UnitSystem,
            key: str = None,
            data: [] = None,
            value_date: date = date.today(),
            batch_id: str = None,
            eob: bool = False):
        """
        Initialize payload
        """
        self.data = data
        self.value_date = value_date
        self.unit_system = unit_system
        self.key = key
        self.batch_id = batch_id
        self.eob = eob


class CalculationResultDetail:
    """
    Details of an evaluation
    """
    exp_id = None
    value_date = None
    expression = None
    operands = None
    magnitude = None
    uncertainty = None
    unit = None

    def __init__(self, expression: str, operands: [],
                 magnitude: uncertainties.ufloat, unit: str,
                 exp_id: str, value_date: date):
        """
        Initialize detail
        :param expression: Expression in the form of a string
        e.g.: 3*{a} + 2 * {b}
        :param operands: List of Operands
        :param magnitude: result of the calculation
        :param units: dimension of the result
        :param uncertainty: uncertainty of the calculation
        """
        self.exp_id = exp_id
        self.value_date = value_date
        self.expression = expression
        self.operands = operands
        self.magnitude = magnitude.n
        self.uncertainty = magnitude.s
        self.unit = unit


class CalculationResultError:
    """
    Error details of a wrong calculation
    """
    exp_id = None
    value_date = None
    expression = None
    operands = None
    calc_date = None
    errors = None

    def __init__(
            self,
            expression: str,
            operands: [],
            calc_date: date,
            errors: [],
            exp_id: str,
            value_date: date = date.today()
    ):
        """
        Initialize error detail
        :param expression: Expression in the form of a string
        :param operands: List of Operands
        :param date: date of the evaluation
        :param error: Error description
        :param exp_id: Optional expression ID
        :param value_date: Date of value in case of currency conversion
        """
        self.exp_id = exp_id
        self.value_date = value_date
        self.expression = expression
        self.operands = operands
        self.calc_date = calc_date
        self.errors = [{'source': key, 'error': value} for key, value in errors.items()]


class CalculationResult:
    """
    Result of a batch of evaluations
    """
    id = None
    detail = []
    status = None
    errors = []

    def __init__(self,
                 id: str = None,
                 detail: [CalculationResultDetail] = None,
                 status: str = BaseConverter.INITIATED_STATUS,
                 errors: [CalculationResultError] = None):
        """
        Initialize result
        :param id: ID of the batch
        :param detail: List of CalculationResultDetail
        :param status: status of the batch
        :param errors: List of CalculationResultErrors
        """
        self.id = id
        self.detail = detail or []
        self.status = status
        self.errors = errors or []

    def end_batch(self):
        """
        Puts a finall status on the batch
        """
        if self.errors:
            self.status = BaseConverter.WITH_ERRORS
        else:
            self.status = BaseConverter.FINISHED
        return self.status


class ExpressionCalculator(BaseConverter):
    """
    Conversion between units
    """
    unit_system = None

    def __init__(
            self,
            unit_system: str,
            user: User = None,
            key: str = '',
            id: str = None):
        """
        Initiate ExpressionCalculator
        :param unit_system: unit system name
        :param user: User
        :param key: key of user
        :param id: ID of the batch
        """
        try:
            super().__init__(id=id)
            self.unit_system = unit_system
            self.user = user
            self.key = key
            self.system = UnitSystem(
                system_name=unit_system,
                user=self.user,
                key=self.key,
            )
        except UnitSystemNotFound as e:
            raise ExpressionCalculatorInitError from e

    def add_data(self, data: []) -> []:
        """
        Check data and add it to the dataset
        Return list of errors
        """
        errors = super().add_data(data)
        return errors

    def check_data(self, data):
        """
        Validates that the data contains
        - system (str)
        - unit (str)
        - value (float)
        - date (YYYY-MM-DD)
        """
        from .serializers import ExpressionSerializer
        errors = []
        for line in data:
            serializer = ExpressionSerializer(data=line)
            if serializer.is_valid(unit_system=self.system):
                self.data.append(serializer.create(serializer.validated_data))
            else:
                cre = CalculationResultError(
                    exp_id=line.get('exp_id', ''),
                    expression=line.get('exp', ''),
                    operands=line.get('operands'),
                    calc_date=date.today(),
                    errors=serializer.errors
                )
                errors.append(cre)
        return errors

    @classmethod
    def load(
            cls,
            id: str,
            user: User = None,
            key: str = None,
    ) -> BaseConverter:
        """
        Load converter from batch
        :param id: ID of the batch
        :param user: Users object
        :param key: User defined category
        """
        try:
            uc = super().load(id)
            uc.system = UnitSystem(
                system_name=uc.unit_system,
                user=user,
                key=key,
            )
            return uc
        except (UnitSystemNotFound, KeyError) as e:
            raise ConverterLoadError from e

    def save(self):
        """
        Save converter to caching system
        """
        system = self.system
        self.system = None
        super(ExpressionCalculator, self).save()
        self.system = system

    def convert(self) -> CalculationResult:
        """
        Converts data to base unit in base system
        """
        result = CalculationResult(id=self.id)
        for value_date, expressions in groupby(
                self.data,
                key=lambda x: x.value_date
        ):
            self.system.update_value_date(value_date)
            for expression in expressions:
                valid, exp_errors = expression.validate(unit_system=self.system)
                if not valid:
                    error = CalculationResultError(
                        exp_id=expression.exp_id,
                        value_date=expression.value_date,
                        expression=expression.expression,
                        operands=expression.operands,
                        calc_date=date.today(),
                        errors=exp_errors
                    )
                    result.errors.append(error)
                    continue
                try:
                    self.system.update_value_date(expression.value_date)
                    out = expression.evaluate(unit_system=self.system)
                except ComputationError as e:
                    error = CalculationResultError(
                        exp_id=expression.exp_id,
                        value_date=expression.value_date,
                        expression=expression.expression,
                        operands=expression.operands,
                        calc_date=date.today(),
                        errors={'source': 'computation', 'error': str(e)}
                    )
                    result.errors.append(error)
                    continue
                detail = CalculationResultDetail(
                    exp_id=expression.exp_id,
                    value_date=expression.value_date,
                    expression=expression.expression,
                    operands=expression.operands,
                    magnitude=out.magnitude,
                    unit=out.units
                )
                result.detail.append(detail)
        self.end_batch(result.end_batch())
        return result
