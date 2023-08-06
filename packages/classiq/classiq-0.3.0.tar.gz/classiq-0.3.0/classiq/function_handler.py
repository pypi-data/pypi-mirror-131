import abc
import functools
from typing import Dict, Iterable, List, Optional, Set, Type, Union

from classiq_interface.generator import (
    function_call,
    function_param_list,
    function_params,
)
from classiq_interface.generator.functions import FunctionLibraryData
from classiq_interface.generator.user_defined_function_params import CustomFunction

from classiq.exceptions import ClassiqValueError, ClassiqWiringError
from classiq.function_library import FunctionLibrary
from classiq.quantum_register import QReg as QuantumRegister
from classiq.wire import Wire


class FunctionHandler(abc.ABC):
    def __init__(self) -> None:
        self._generated_wires: Set[Wire] = set()
        self._function_library: Optional[FunctionLibrary] = None

    def _verify_legal_wires(self, wires: Union[Wire, Iterable[Wire]]) -> None:
        if isinstance(wires, Wire):
            wires = [wires]
        if not all(wire in self._generated_wires for wire in wires):
            raise ClassiqWiringError("Wire does not belong to this generator")

    def _update_generated_wires(self, wires: Union[Wire, Iterable[Wire]]) -> None:
        if isinstance(wires, Wire):
            wires = [wires]
        self._generated_wires.update(wires)

    def apply(
        self,
        function_name: str,
        in_wires: Optional[Dict[str, Union[QuantumRegister, Wire]]] = None,
        out_wires: Optional[Dict[str, Union[QuantumRegister, Wire]]] = None,
    ) -> Dict[str, Wire]:
        if self._function_library is None:
            raise ClassiqValueError("Cannot apply function without a function library")

        params = self._function_library.get_function(function_name=function_name)
        return self._function_call_handler(
            function=CustomFunction.__name__,
            params=params,
            in_wires=in_wires,
            out_wires=out_wires,
        )

    def _function_call_handler(
        self,
        function: str,
        params: function_params.FunctionParams,
        in_wires: Optional[Dict[str, Union[QuantumRegister, Wire]]] = None,
        out_wires: Optional[Dict[str, Union[QuantumRegister, Wire]]] = None,
    ) -> Dict[str, Wire]:
        if function != type(params).__name__:
            raise ClassiqValueError(
                "The FunctionParams type does not match function name"
            )

        if isinstance(params, CustomFunction):
            FunctionLibraryData.validate_function_in_library(
                library=self._function_library.data if self._function_library else None,
                function_params=params,
                error_handler=ClassiqValueError,
            )

        call = function_call.FunctionCall(function=function, function_params=params)

        if in_wires:
            self._connect_in_wires(call=call, in_wires=in_wires)

        self._logic_flow.append(call)

        return self._connect_out_wires(
            call=call,
            output_names=params.get_io_names(function_params.IO.Output),
            out_wires=out_wires or {},
        )

    def _connect_in_wires(
        self,
        call: function_call.FunctionCall,
        in_wires: Dict[str, Union[QuantumRegister, Wire]],
    ) -> None:
        self._verify_legal_wires(
            wires=[
                in_wire.wire if isinstance(in_wire, QuantumRegister) else in_wire
                for in_wire in in_wires.values()
            ]
        )

        for input_name, in_wire in in_wires.items():
            if isinstance(in_wire, QuantumRegister):
                in_wire.consume()
                in_wire = in_wire.wire

            in_wire.connect_wire_end(end_call=call, input_name=input_name)

    def _connect_out_wires(
        self,
        call: function_call.FunctionCall,
        output_names: Iterable[str],
        out_wires: Dict[str, Union[QuantumRegister, Wire]],
    ) -> Dict[str, Wire]:
        wire_dict: Dict[str, Wire] = {}

        for name in out_wires.keys():
            if name not in output_names:
                raise ClassiqWiringError(
                    f"output_name ({name}) does not belong to this function call"
                )

        for output_name in output_names:
            if output_name in out_wires:
                out_wire = out_wires[output_name]
                if isinstance(out_wire, QuantumRegister):
                    out_wire = out_wire.wire

                out_wire.connect_wire_start(start_call=call, output_name=output_name)
                wire_dict[output_name] = out_wire
            else:
                wire_dict[output_name] = self._output_wire_type(
                    start_call=call, output_name=output_name
                )

        self._update_generated_wires(wires=wire_dict.values())

        return wire_dict

    def __getattr__(self, item):
        is_builtin_function_name = any(
            item == func.__name__
            for func in function_param_list.get_function_param_list()
        )

        if is_builtin_function_name:
            return functools.partial(self._function_call_handler, function=item)

        is_user_function_name = (
            self._function_library is not None
            and item in self._function_library.data.function_dict
        )

        if is_user_function_name:
            return functools.partial(self.apply, function_name=item)

        return super().__getattr__(item)

    def __dir__(self):
        builtin_func_name = [
            func.__name__ for func in function_param_list.get_function_param_list()
        ]
        user_func_names = (
            list(self._function_library.function_names)
            if self._function_library is not None
            else list()
        )
        return list(super().__dir__()) + builtin_func_name + user_func_names

    def include_library(self, library: FunctionLibrary) -> None:
        """Includes a function library.

        Args:
            library (FunctionLibrary): The function library.
        """
        if self._function_library is not None:
            raise ClassiqValueError("Another function library is already included.")

        self._function_library = library

    @property
    @abc.abstractmethod
    def _logic_flow(self) -> List[function_call.FunctionCall]:
        pass

    @property
    @abc.abstractmethod
    def _output_wire_type(self) -> Type[Wire]:
        pass
