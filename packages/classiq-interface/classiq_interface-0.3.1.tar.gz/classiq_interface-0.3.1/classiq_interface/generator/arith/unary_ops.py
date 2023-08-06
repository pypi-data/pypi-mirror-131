from enum import Enum
from typing import Dict, Optional

import pydantic

from classiq_interface.generator.arith.arithmetic import (
    DEFAULT_ARG_NAME,
    DEFAULT_OUT_NAME,
)
from classiq_interface.generator.arith.register_user_input import RegisterUserInput
from classiq_interface.generator.function_params import FunctionParams


class UnaryOpParams(FunctionParams):
    arg: RegisterUserInput
    output_size: Optional[pydantic.PositiveInt]
    output_name: Optional[str]
    inplace: bool = False

    def create_io_enums(self):
        output_name = self.output_name if self.output_name else DEFAULT_OUT_NAME
        arg_name = self.arg.name if self.arg.name else DEFAULT_ARG_NAME

        output_name_dict: Dict[str, str] = {output_name: output_name}
        input_name_dict = {arg_name: arg_name}
        if not self.inplace:
            output_name_dict.update(input_name_dict)

        self._output_enum = Enum("BinaryOpOutputs", output_name_dict)
        self._input_enum = Enum("UnaryOpInputs", input_name_dict)

    class Config:
        arbitrary_types_allowed = True


class BitwiseInvert(UnaryOpParams):
    pass


class Negation(UnaryOpParams):
    pass
