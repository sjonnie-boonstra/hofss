from typing import Iterable
import time
import random

from ..data_structures import Parameter, Scenario
from .failure_mode import FailureMode


class Structure:

    def __init__(self, name: str, parameters: list[Parameter], failure_modes: list[FailureMode]) -> None:
        self.name = name
        self.parameters = parameters
        self.failure_modes = failure_modes
        return

    @property
    def name(self) -> str:
        """name of this structure"""
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise TypeError(f"name should be of type: str; received: {type(value).__name__}")
        self._name = value
        return

    @property
    def parameters(self) -> list[Parameter]:
        """the parameters that define the structural properties and integrity of this structure"""
        return self._parameters

    @parameters.setter
    def parameters(self, values: list[Parameter]):
        if not isinstance(values, Iterable) or isinstance(values, str):
            raise TypeError(f"parameters should be an iterable and not of type str")
        for i, value in enumerate(values):
            if not isinstance(value, Parameter):
                raise TypeError(f"item at index '{i}' is not of type: Parameter; received: {type(value).__name__}")
        self._parameters = list(values)
        return

    @property
    def failure_modes(self) -> list[FailureMode]:
        """the failure modes that affect this structure"""
        return self._failure_modes

    @failure_modes.setter
    def failure_modes(self, values: list[FailureMode]):
        if not isinstance(values, Iterable) or isinstance(values, str):
            raise TypeError(f"failure_modes should be an iterable and not of type str")
        for i, value in enumerate(values):
            if not isinstance(value, FailureMode):
                raise TypeError(f"item at index '{i}' is not of type: FailureMode; received: {type(value).__name__}")
        self._failure_modes = list(values)
        return

    def update_parameters(self, scenario: Scenario) -> None:
        """updates the parameters according to the provided scnario

        Args:
            scenario (Scenario): the scenario that happened after a human error has occured
        """
        if scenario is None:
            return

        # use the scenario to update this structure's prameters

        return

    def draw_parameter_values(self, seed: int) -> dict[str, float]:
        """draws parameter values for this structures from this structure's
        parameter definitionsusing the provided Random Number Generator seed

        Args:
            seed (int): the seed to use to draw a random number from the parameter distributions

        Returns:
            dict[str, float]: a dictionary with the parameter values by their respective names
        """
        random.seed(seed)
        parameter_values = {}
        for parameter in self.parameters:
            parameter_value = None  # draw number from the parameter distribution here
            parameter_values[parameter.name] = parameter_value
        return parameter_values

    def calculate_failure_probabilities(
        self, number_of_iterations: int = 1e6, monte_carlo_seed: int = None
    ) -> dict[str, float]:
        """calculates the failure probabilities for each failure mode through a Monte Carlo simulation

        Args:
            number_of_iterations (int, optional): the number of iterations in the
            Monte Carlo simulation. Defaults to 1e6.
            monte_carlo_seed (int, optional): the seed that is used to create the randomness
            in the Monte Carlos simulation. Defaults to None.

        Returns:
            dict[str, float]: a dictionary with the failure probability per failure mode
        """

        # create the randomness in the Monte Carlo simulation
        if monte_carlo_seed is not None:
            monte_carlo_seed = time.time()
        random.seed(monte_carlo_seed)

        # create a list of seeds to draw parameter values
        draw_seeds = [random.randint(1, 1e10) for _ in range(number_of_iterations)]
        random.shuffle(draw_seeds)

        # compute the failure criterions by drawing parameters and using
        # them to calculate this criterion for each failure mode
        failure_simulations = []
        for draw_seed in draw_seeds:
            failure_criterions = []
            for failure_mode in self.failure_modes:
                parameter_values = self.draw_parameter_values(draw_seed)
                failure_criterions.append(failure_mode.calculate_failure_criterion(**parameter_values))
            failure_simulations.append(failure_criterions)

        # calculate the failure probabilities for each failure mode
        failure_probabilities = {}
        for failure_mode in self.failure_modes:
            # calculate the probability of this failure mode
            pass
        # calculate the total failure probability considering all failure modes
        return failure_probabilities
