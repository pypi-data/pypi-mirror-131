"""Generator module, implementing facilities for generating circuits using Classiq platform."""
import asyncio
from typing import List, Type

from classiq_interface.generator import constraints, function_call, result

from classiq import api_wrapper, function_handler, wire
from classiq.exceptions import ClassiqGenerationError
from classiq.function_library import FunctionLibrary

# TODO: Add docstrings for auto generated methods.


class Generator(function_handler.FunctionHandler):
    """Facility to generate circuits, based on the model."""

    def __init__(self, qubit_count: int, max_depth: int, **kwargs) -> None:
        """Init self with qubit count and maximal depth.

        Args:
            qubit_count (): The number of qubits in the generated circuit.
            max_depth (): The maximum depth of the generated circuit.
        """
        super().__init__()
        self._constraints = constraints.QuantumCircuitConstraints(
            qubit_count=qubit_count, max_depth=max_depth, **kwargs
        )

    @property
    def _output_wire_type(self) -> Type[wire.Wire]:
        return wire.Wire

    @property
    def _logic_flow(self) -> List[function_call.FunctionCall]:
        return self._constraints.logic_flow

    def generate(self) -> result.GeneratedCircuit:
        """Generates a circuit, based on the aggregation of requirements in self.

        Returns:
            The results of the generation procedure.
        """
        return asyncio.run(self.generate_async())

    async def generate_async(self) -> result.GeneratedCircuit:
        """Async version of `generate`
        Generates a circuit, based on the aggregation of requirements in self.

        Returns:
            The results of the generation procedure.
        """
        # TODO: There something distorted with regards to the singleton and the configuration. Also, the need to pass
        #       conf here and not in init is weird.
        wrapper = api_wrapper.ApiWrapper()
        generation_result = await wrapper.call_generation_task(self._constraints)

        if generation_result.status != result.GenerationStatus.SUCCESS:
            raise ClassiqGenerationError(
                f"Generation failed: {generation_result.details}"
            )

        return generation_result.details

    @property
    def constraints(self) -> constraints.QuantumCircuitConstraints:
        """Get the constraints aggregated in self.

        Returns:
            The constraints data.
        """
        return self._constraints

    def include_library(self, library: FunctionLibrary) -> None:
        """Includes a user-defined custom function library.

        Args:
            library (FunctionLibrary): The custom function library.
        """
        super().include_library(library=library)
        self._constraints.function_library = library.data
