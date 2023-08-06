"""
Serializers for Calculations module
"""
import json
import uuid
from tokenize import TokenError
from datetime import date

import pint
from rest_framework import serializers
from sympy import sympify, SympifyError

from djangophysics.units.models import UnitSystem
from .models import Expression, CalculationPayload, Operand, \
    CalculationResult, CalculationResultError, CalculationResultDetail
from djangophysics.core.helpers import uuid4_str


class OperandSerializer(serializers.Serializer):
    """
    Serialize an Operand
    """
    name = serializers.CharField(
        label="Name of the operand in the expression",
        help_text="{a} in an expression should have an operand named 'a'")
    value = serializers.FloatField(
        label="Value of the operand as a float")
    unit = serializers.CharField(
        label="Units of the operand as a string")
    uncertainty = serializers.CharField(
        label="Uncertainty value, either absolute, or percentage.",
        required=False,
        help_text="Uncertainty for value, "
                  "if float, it is absolute (10), "
                  "else, it must contain % (12%)")

    def is_valid(self, raise_exception=False) -> bool:
        """
        Check validity of the operand
        """
        if not self.initial_data.get('name'):
            raise serializers.ValidationError("operand Name not set")
        if 'value' not in self.initial_data:
            raise serializers.ValidationError("operand Value not set")
        try:
            float(self.initial_data['value'])
        except ValueError as e:
            raise serializers.ValidationError("invalid operand value") from e
        if 'unit' not in self.initial_data:
            raise serializers.ValidationError("operand Unit not set")
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        """
        Create an Operand object
        :param validated_data: cleaned date
        """
        return Operand(**validated_data)


class ExpressionListSerializer(serializers.ListSerializer):
    """
    Serialize a list of Expressions
    """

    def is_valid(self,
                 unit_system: UnitSystem,
                 dimensions_only=False,
                 raise_exception=False):
        """
        Check validity of expression with a specific UnitSystem
        :param unit_system: UnitSystem instance
        :param dimensions_only: Only check dimensionality, not actual units
        :param raise_exception: raise an exception instead of a list of errors
        """
        super().is_valid(raise_exception=raise_exception)
        for initial_exp in self.initial_data:
            ec = ExpressionSerializer(data=initial_exp)
            ec.is_valid(unit_system=unit_system,
                        dimensions_only=dimensions_only)
            if ec.errors:
                self._errors.append(ec.errors)
        return not bool(self._errors)


class ExpressionSerializer(serializers.Serializer):
    """
    Serialize an expression
    """
    unit_system = None
    key = None
    exp_id = serializers.CharField(default=uuid4_str)
    value_date = serializers.DateField(
        label="Date of value for currency conversion",
        required=False
    )
    expression = serializers.CharField(
        label="Mathematical expression to evaluate",
        required=True,
        help_text="Operands must be placed between curly braces."
                  "A recommended expression format "
                  "would be '{a}+{b}*{c}'")
    operands = OperandSerializer(
        label="List of operands",
        many=True,
        required=True)
    out_units = serializers.CharField(
        label="Define output units",
        required=False,
        help_text="Set output units, optional (e.g.: km/hour)")

    class Meta:
        """
        Meta
        """
        list_serializer_class = ExpressionListSerializer

    def operands_obj(self, operands: [dict]):
        return [
            Operand(
                name=v['name'],
                value=v['value'],
                unit=v['unit'])
            for v in operands]

    def expr_args(self, unit_system: UnitSystem, operands: [Operand]):
        """
        Build expression arguments to pass to format or expression validation
        """
        return {v.name: v.expr(unit_system=unit_system)
                for v in operands}

    def is_valid(self, unit_system: UnitSystem,
                 raise_exception=False,
                 dimensions_only=False) -> bool:
        """
        Check if expression is valid
        :param unit_system: UnitSystem instance
        :param dimensions_only: Only test dimensions
        :param raise_exception: raise an exception instead of a list of errors
        """
        super().is_valid(raise_exception=raise_exception)
        operands = self.operands_validation(
            operands=self.initial_data.get('operands')
        )
        expression = self.expression_validation(
            unit_system=unit_system,
            expression=self.initial_data.get('expression'),
            operands=operands
        )
        out_units = self.out_units_validation(
            unit_system=unit_system,
            out_units=self.initial_data.get('out_units')
        )
        if expression:
            if dimensions_only:
                self.dimensions_validation(
                    unit_system=unit_system,
                    expression=expression,
                    operands=operands,
                    out_units=out_units
                )
            else:
                self.units_validation(
                    unit_system=unit_system,
                    expression=expression,
                    operands=operands,
                    out_units=out_units
                )
        if self._errors and raise_exception:
            raise serializers.ValidationError(self._errors)
        return not bool(self._errors)

    def units_validation(self,
                         unit_system: UnitSystem,
                         expression: str,
                         operands: [Operand],
                         out_units: str = None) -> bool:
        """
        Validate units based on the units of the operands
        :param unit_system: Reference unit system with custom units
        :param expression: Mathematical expression as string
        :param operands: list of Operand objects
        :param out_units: optional conversion to specific units
        """
        try:
            units_kwargs = self.expr_args(
                unit_system=unit_system,
                operands=self.operands_obj(operands=operands))
            result = unit_system.ureg.parse_expression(
                expression, **units_kwargs)
        except KeyError:
            self._errors['operands'] = "Missing operands"
            return False
        except pint.errors.UndefinedUnitError:
            self._errors['expression'] = "Invalid units"
            return False
        except pint.errors.DimensionalityError:
            self._errors['expression'] = "Incoherent dimension"
            return False
        except TokenError:
            self._errors['expression'] = "Invalid expression"
            return False
        except ZeroDivisionError:
            self._errors['expression'] = "Division by zero"
            return False
        if out_units:
            try:
                result.to(out_units)
            except pint.errors.DimensionalityError:
                self._errors['out_units'] = "Incoherent output dimension"
                return False
        return True

    def dimensions_validation(self,
                              unit_system: UnitSystem,
                              expression: str,
                              operands: [Operand],
                              out_units: str = None) -> bool:
        """
        Validate units dimensions based on get_unit of the operands
        :param unit_system: Reference unit system with custom units
        :param expression: Mathematical expression as string
        :param operands: list of Operand objects
        :param out_units: optional conversion to specific units
        """
        q_ = unit_system.ureg.Quantity
        units_kwargs = self.expr_args(
            unit_system=unit_system,
            operands=self.operands_obj(operands=operands))
        try:
            result = q_(expression.format(**units_kwargs))
        except KeyError:
            self._errors['operands'] = "Missing operands"
            return False
        except (pint.errors.DimensionalityError,
                pint.errors.UndefinedUnitError) as e:
            self._errors['expression'] = f"Incoherent dimension {str(e)}"
            return False
        except TokenError:
            self._errors['expression'] = "Invalid expression"
            return False
        except ZeroDivisionError:
            self._errors['expression'] = "Division by zero"
            return False
        if out_units:
            try:
                result.to(out_units)
            except (pint.errors.DimensionalityError,
                    pint.errors.UndefinedUnitError) as e:
                self._errors['out_units'] = f"Incoherent output " \
                                            f"dimension {str(e)}"
                return False
        return True

    def expression_validation(
            self,
            unit_system: UnitSystem,
            expression: str, operands: [Operand]):
        """
        Check syntactic validity of expression
        :param unit_system: UnitSystem instance
        :param expression: Mathematical expression as string
        :param operands: list of Operand objects
        """
        if not expression:
            self._errors['expression'] = "Empty expression"
            return None
        # Validate syntax
        value_kwargs = {v['name']: v['value'] for v in operands}
        try:
            sympify(expression.format(**value_kwargs))
        except (SympifyError, KeyError):
            self._errors['expression'] = "Invalid operation"
        return expression

    def out_units_validation(self, unit_system: UnitSystem, out_units: str):
        """
        Check validity of output units
        :param unit_system: Reference unit system with custom units
        :param out_units: optional conversion to specific units
        """
        if not out_units:
            return None
        q_ = unit_system.ureg.Quantity
        try:
            q_(1, out_units)
        except pint.errors.DimensionalityError as e:
            self._errors['out_units'] = f"Incoherent output dimension {str(e)}"
            return None
        except pint.UndefinedUnitError as e:
            self._errors['out_units'] = f"Incoherent output units {str(e)}"
            return None
        return out_units

    def operands_validation(self, operands):
        """
        Validate Operand
        :param operands: Operand
        """
        errors = []
        try:
            for var in operands:
                vs = OperandSerializer(data=var)
                vs.is_valid()
                if vs.errors:
                    errors.append(vs.errors)
            if errors:
                self._errors['operands'] = errors
        except json.JSONDecodeError as e:
            self._errors['operands'] = f"Invalid operands json format: {e}"
        except TypeError:
            self._errors['operands'] = f"Invalid operands input"
        return operands

    def create(self, validated_data):
        """
        Create an Expression
        :param validated_data: cleaned data
        """
        operands = []
        for var in validated_data.get('operands'):
            vs = OperandSerializer(data=var)
            if vs.is_valid():
                operands.append(vs.create(vs.validated_data))
        return Expression(
            exp_id=validated_data.get('exp_id', uuid.uuid4()),
            value_date=validated_data.get('value_date', date.today()),
            expression=validated_data.get('expression'),
            operands=operands,
            out_units=validated_data.get('out_units')
        )

    def update(self, instance, validated_data):
        """
        Update Expression
        :param instance: Expression object
        :param validated_data: cleaned data
        """
        instance.exp_id = validated_data.get('exp_id')
        instance.value_date = validated_data.get('value_date')
        instance.expression = validated_data.get('expression')
        instance.operands = validated_data.get('operands')
        instance.out_units = validated_data.get('out_units')
        return instance


class CalculationResultDetailSerializer(serializers.Serializer):
    """
    Serializer for the CalculationResultDetail class
    """
    exp_id = serializers.CharField(label="ID of the expression")
    value_date = serializers.DateField(
        label="Date of value for currency conversion",
        required=False
    )
    expression = serializers.CharField(label="Expression to evaluate")
    operands = OperandSerializer(many=True)
    magnitude = serializers.FloatField(label="Magnitude of result")
    uncertainty = serializers.FloatField(label="Uncertainty of result")
    unit = serializers.CharField(label="Units of result")

    def create(self, validated_data):
        """
        Create a CalculationResultDetail object
        :param validated_data: cleaned data
        """
        return CalculationResultDetail(**validated_data)

    def update(self, instance, validated_data):
        """
        Update a CalculationResultDetail object
        :param instance: CalculationResultDetail object
        :param validated_data: cleaned data
        """
        instance.exp_id = validated_data.get(
            'exp_id', instance.exp_id)
        instance.value_date = validated_data.get(
            'value_date', instance.value_date)
        instance.expression = validated_data.get(
            'expression', instance.expression)
        instance.operands = validated_data.get(
            'operands', instance.operands)
        instance.magnitude = validated_data.get(
            'magnitude', instance.magnitude)
        instance.uncertainty = validated_data.get(
            'uncertainty', instance.operands)
        return instance


class CalculationResultErrorDetailSerializer(serializers.Serializer):
    """
    List of errors in an expression or calculation
    """
    source = serializers.CharField(label="Source of the error")
    error = serializers.CharField(label="Detail of the error")


class CalculationResultErrorSerializer(serializers.Serializer):
    """
    Serializer for the CalculationResultError class
    """
    exp_id =  serializers.CharField(label="ID of the expression")
    value_date = serializers.DateField(
        label="Date of value for currency conversion",
        required=False
    )
    expression = serializers.CharField(label="Expression to evaluate")
    operands = OperandSerializer(many=True)
    calc_date = serializers.DateField(label="Date of calculation")
    errors = CalculationResultErrorDetailSerializer(
        label="Error during calculation",
        many=True)

    def create(self, validated_data):
        """
        Create a CalculationResultError object
        :param validated_data: cleaned data
        """
        return CalculationResultError(**validated_data)

    def update(self, instance, validated_data):
        """
        Update a CalculationResultError object
        :param instance: CalculationResultError object
        :param validated_data: cleaned data
        """
        instance.exp_id = validated_data.get(
            'exp_id', instance.exp_id)
        instance.expression = validated_data.get(
            'expression', instance.expression)
        instance.operands = validated_data.get(
            'operands', instance.operands)
        instance.calc_date = validated_data.get(
            'calc_date', instance.calc_date)
        instance.errors = validated_data.get(
            'errors', instance.errors)
        return instance


class CalculationResultSerializer(serializers.Serializer):
    id = serializers.UUIDField(label="ID of the batch")
    detail = CalculationResultDetailSerializer(
        label="Details of the calculation", many=True)
    status = serializers.CharField(
        label="Status of the calculation")
    errors = CalculationResultErrorSerializer(
        label="Errors during calculation", many=True)

    def create(self, validated_data):
        """
        Create a CalculationResult object
        :param validated_data: cleaned data
        """
        return CalculationResult(**validated_data)

    def update(self, instance, validated_data):
        """
        Update a CalculationResult object
        :param instance: CalculationResult object
        :param validated_data: cleaned data
        """
        instance.id = validated_data.get('id', instance.id)
        instance.value_date = validated_data.get('value_date', instance.value_date)
        instance.detail = validated_data.get('detail', instance.detail)
        instance.status = validated_data.get('status', instance.status)
        instance.errors = validated_data.get('errors', instance.errors)
        return instance


class CalculationPayloadSerializer(serializers.Serializer):
    """
    Serializer for CalculationPayload
    """
    unit_system = serializers.CharField(
        label="Unit system to evaluate in",
        required=True)
    data = ExpressionSerializer(
        label="Payload of expressions",
        many=True, required=False)
    batch_id = serializers.CharField(
        label="User defined ID of the batch of evaluations",
        required=False)
    key = serializers.CharField(
        label="User defined categorization key",
        required=False)
    eob = serializers.BooleanField(
        label="End of batch ? triggers the evaluation",
        default=False)

    def is_valid(self, raise_exception=False) -> bool:
        """
        Check validity of the payload
        """
        if not self.initial_data.get('data') and \
                (not self.initial_data.get('batch_id')
                 or (self.initial_data.get('batch_id')
                     and not self.initial_data.get('eob'))):
            raise serializers.ValidationError(
                'data has to be provided if batch_id is not provided '
                'or batch_id is provided and eob is False'
            )
        return super().is_valid(raise_exception=raise_exception)

    @staticmethod
    def validate_unit_system(value: str):
        """
        Validate unit system
        :param value: unit system name
        """
        from djangophysics.units.models import UnitSystem
        if not UnitSystem.is_valid(value):
            raise serializers.ValidationError('Invalid unit system')
        return value

    def create(self, validated_data: {}):
        """
        Create CalculationPayload from cleaned data
        :param validated_data: cleaned data
        """
        return CalculationPayload(**validated_data)

    def update(self, instance, validated_data: {}):
        """
        Update a CalculationPayload from cleaned data
        :param instance: CalculationPayload object
        :param validated_data: cleaned data
        """
        self.data = validated_data.get('data', instance.data)
        self.value_date = validated_data.get('value_date', instance.value_date)
        self.unit_system = validated_data.get(
            'unit_system', instance.unit_system)
        self.batch_id = validated_data.get('batch_id', instance.batch_id)
        self.key = validated_data.get('key', instance.key)
        self.eob = validated_data.get('eob', instance.eob)
        return instance


class DimensionalitySerializer(serializers.Serializer):
    """
    Serializer for dimensionality
    return a dimension with associated power
    """
    code = serializers.CharField(label="code of the dimension")
    multiplicity = serializers.FloatField(
        label="multiplicy of the dimension"
    )
