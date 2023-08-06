from enum import Enum
from typing import List, Optional, Union

import pydantic


class UnrollerType(str, Enum):
    THREE_QUBIT_GATES = "three_qubit_gates"


class TranspilationPreferences(pydantic.BaseModel):
    """
    Preferences for running transpiler on the generated quantum circuit.
    """

    is_sub_circuit: bool = pydantic.Field(
        default=False,
        description="Whether the transpiled circuit is part of a bigger circuit. "
        "This enables optimizations with assumptions on the start and end conditions of the circuit.",
    )
    unroller: Optional[Union[UnrollerType, List[str]]] = pydantic.Field(
        default=None,
        description=f"Unroll {UnrollerType.THREE_QUBIT_GATES} or unroll to specific basis gates.",
    )

    @pydantic.validator("unroller")
    def validate_unroller(cls, unroller):
        if isinstance(unroller, list) and not unroller:
            raise ValueError("Empty basis gates is forbidden.")

        return unroller
