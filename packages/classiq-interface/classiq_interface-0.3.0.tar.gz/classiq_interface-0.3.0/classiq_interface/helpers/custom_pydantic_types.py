from typing import TYPE_CHECKING

import pydantic

# General int types
if TYPE_CHECKING:
    pydanticLargerThanOneInteger = int
else:

    class pydanticLargerThanOneInteger(pydantic.ConstrainedInt):
        gt = 1


# Probability float types
if TYPE_CHECKING:
    pydanticProbabilityFloat = float
    pydanticNonOneProbabilityFloat = float
    pydanticNonZeroProbabilityFloat = float
else:

    class pydanticProbabilityFloat(pydantic.ConstrainedFloat):
        ge = 0.0
        le = 1.0

    class pydanticNonOneProbabilityFloat(pydantic.ConstrainedFloat):
        ge = 0.0
        lt = 1.0

    class pydanticNonZeroProbabilityFloat(pydantic.ConstrainedFloat):
        gt = 0.0
        le = 1.0


# CVAR parameter types
if TYPE_CHECKING:
    pydanticAlphaParamCVAR = float
else:

    class pydanticAlphaParamCVAR(pydantic.ConstrainedFloat):
        gt = 0.0
        le = 1.0


# General string types
if TYPE_CHECKING:
    pydanticNonEmptyString = str
else:
    pydanticNonEmptyString = pydantic.constr(min_length=1)

# Name string types
if TYPE_CHECKING:
    pydanticFunctionNameStr = str
else:
    pydanticFunctionNameStr = pydantic.constr(
        strict=True, regex="^([a-z][a-z0-9]*)(_[a-z0-9]+)*$"
    )
