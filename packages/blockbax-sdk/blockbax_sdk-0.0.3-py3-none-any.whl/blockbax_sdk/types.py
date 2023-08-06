import datetime
import enum
from numbers import Number
from decimal import Decimal
from typing import Union

import logging
logger = logging.getLogger(__name__)

# Generic types

AnyDate = Union[datetime.datetime, int, str]
AnyNumber = Union[int, float, Number, Decimal]

# Blockbax types

# Measurement data types

class MeasurementDataTypes(str, enum.Enum):
    NUMBER = "number"
    LOCATION = "location"
    TEXT = "text"
    
    @classmethod
    def _missing_(cls, value: str):
        return _check_missing_is_upper_name(cls, value)

# Property data types
class PropertyDataTypes(str, enum.Enum):
    TEXT = "text"
    NUMBER = "number"
    LOCATION = "location"
    MAP_LAYER = "mapLayer"
    IMAGE = "image"
    AREA="area"
    
    @classmethod
    def _missing_(cls, value: str):
        return _check_missing_is_upper_name(cls, value)

# Primary location (Subject Type) types
class PrimaryLocationTypes(str, enum.Enum):
    PROPERTY_TYPE = "PROPERTY_TYPE"
    METRIC = "METRIC"
    
    @classmethod
    def _missing_(cls, value: str):
        return _check_missing_is_upper_name(cls, value)


# Metric types
class MetricTypes(str, enum.Enum):
    INGESTED = "INGESTED"
    SIMULATED = "SIMULATED"
    CALCULATED = "CALCULATED"
    
    @classmethod
    def _missing_(cls, value: str):
        return _check_missing_is_upper_name(cls, value)

# Check if given value is actually its lower counter part

def _check_missing_is_upper_name(cls, value: str):
    known_types = []
    for member in cls:
        known_types.append(member)
        if member.name == str(value).upper():
            return member
    error_unknown_type = f"'{value}' is not a known data type, known data types: {', '.join(known_types)}"
    raise ValueError(error_unknown_type)
