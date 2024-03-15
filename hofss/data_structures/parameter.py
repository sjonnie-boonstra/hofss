from dataclasses import dataclass
import numpy as np


@dataclass
class Parameter:
    """a parameter that describes the structural properties and/or integrity of a structure
    """

    name: str
    "the name of the parameter"
    value: float
    "the (nominal) value of the parameter"
    standard_deviation: float
    "the standard deviation of the parameter"
    distribution_function: callable = np.random.normal
    "the distribution function of the parameter, expected arguments: mean, standard_deviation, number_of_draws (default=1)"

    def draw(self, n: int) -> np.ndarray:
        """draws n-parameter values for this parameter

        Args:
            n (int): the number of values to draw for this parameter

        Returns:
            np.ndarray[float]: a numpy array of n-values drawn for this parameter
        """
        return np.array(self.distribution_function(self.value, self.standard_deviation, int(n)))
