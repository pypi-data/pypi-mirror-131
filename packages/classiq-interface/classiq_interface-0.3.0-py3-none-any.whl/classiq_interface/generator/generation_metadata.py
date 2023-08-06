from typing import List, Optional, Union

import pydantic

from classiq_interface.generator import finance, grover_operator
from classiq_interface.hybrid import encoding_type, problem_input


class FinanceModelMetadata(pydantic.BaseModel):
    num_model_qubits: int
    distribution_range: List[float]


class HybridMetadata(pydantic.BaseModel):
    problem: problem_input.ProblemInput
    encoding_type: encoding_type.EncodingType
    num_auxiliary: Optional[pydantic.NonNegativeInt] = 0
    permutation: List[int]
    is_qaoa: bool = False


class FinanceMetadata(pydantic.BaseModel):
    finance_attribute: Optional[Union[finance.Finance, FinanceModelMetadata]]


class GroverMetadata(pydantic.BaseModel):
    grover_attribute: Optional[grover_operator.GroverOperator]


class FunctionMetadata(pydantic.BaseModel):
    name: str
    parent: Optional[str]
    children: List[str]


class GenerationMetadata(pydantic.BaseModel):
    hybrid: Optional[HybridMetadata]
    finance: Optional[FinanceMetadata]
    grover: Optional[GroverMetadata]
