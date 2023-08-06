from typing import Generic, Optional, TypeVar

import pydantic
from pydantic.generics import GenericModel

RangeType = TypeVar("RangeType", int, float)


class Range(GenericModel, Generic[RangeType]):
    lower_bound: Optional[RangeType] = None
    upper_bound: Optional[RangeType] = None

    @pydantic.validator("upper_bound")
    def validate_bounds_order(cls, upper_bound, values):
        lower_bound = values.get("lower_bound")

        if (
            lower_bound is not None
            and upper_bound is not None
            and lower_bound > upper_bound
        ):
            raise ValueError("lower bound must not be greater than upper bound")

        return upper_bound


NonNegativeIntRange = Range[pydantic.NonNegativeInt]
NonNegativeFloatRange = Range[pydantic.NonNegativeFloat]
