import math
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
    distribution_function: callable = None
    "the distribution function of the parameter, expected arguments: mean, standard_deviation, number_of_draws (default=1)"

    def draw(self, n: int) -> np.ndarray:
        """draws n-parameter values for this parameter

        Args:
            n (int): the number of values to draw for this parameter

        Returns:
            np.ndarray[float]: a numpy array of n-values drawn for this parameter
        """
        if self.standard_deviation == 0:
            return self.value
        if self.distribution_function.__name__ == "lognormal":
            mu = math.log(self.value**2 / math.sqrt(self.value**2 + self.standard_deviation**2))
            sigma = math.sqrt(math.log(1 + (self.standard_deviation**2) / (self.value**2)))
            return np.array(self.distribution_function(mu, sigma, int(n)))
        elif self.distribution_function.__name__ == "gamma":
            k = self.value ** 2 / self.standard_deviation ** 2
            theta = self.standard_deviation ** 2 / self.value
            return np.array(self.distribution_function(k, theta, int(n)))
        elif self.distribution_function.__name__ == "exponential":

            return np.array(self.distribution_function(self.value, self.standard_deviation, int(n)))
        else:
            return np.array(self.distribution_function(self.value, self.standard_deviation, int(n)))

    def update_rng(self, rng: np.random.Generator):
        """updates the Random Number Generator (RNG) of the distribution function

        Args:
            rng (np.random.Generator): the random number generator to assign to the distribution function
        """
        function_name = self.distribution_function.__name__
        self.distribution_function = getattr(rng, function_name)
        return
