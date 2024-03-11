from dataclasses import dataclass
import random
import pandas as pd
import numpy as np

from .factor_level import FactorLevel


@dataclass
class Factor:
    """a factor that influences the Human Error Probability (HEP) of a task
    """

    name: str
    "name of this factor, used to identify it"
    description: str = None
    "description of this factor"
    p_negative_effect: float = 0
    "chance a negative effect occurs due to this factor"
    p_no_effect: float = 1
    "chance no effect occurs due to this factor"
    p_positive_effect: float = 0
    "chance a positive effect occurs due to this factor"
    m_neg_lower: float = 0
    "lower bound of multiplier in case of negative effect"
    m_neg_5: float = 0
    "5th percentile of multiplier in case of negative effect"
    m_neg_50: float = 0
    "50th percentile of factor in case of negative effect"
    m_neg_95: float = 0
    "95th percentile of multiplier in case of negative effect"
    m_neg_upper: float = 0
    "upper bound of multiplier in case of negative effect"
    m_pos_lower: float = 0
    "lower bound of multiplier in case of positive effect"
    m_pos_5: float = 0
    "5th percentile of multiplier in case of positive effect"
    m_pos_50: float = 0
    "50th percentile of multiplier in case of positive effect"
    m_pos_95: float = 0
    "95th percentile of multiplier in case of positive effect"
    m_pos_upper: float = 0
    "upper bound of multiplier in case of positive effect"

    def draw_negative_effect_multiplier(self, p: float) -> float:
        """draws a multiplier for the negative effect.

        Args:
            p (float): the probability that determines the draw. Should be between [0,1].

        Returns:
            float: the drawn multiplier
        """
        if p < 0 or p > 1:
            raise ValueError(f"p must lie between 0 and 1, received value: {p}")
        p_values = [0, 0.05, 0.5, 0.95, 1]
        multiplier_value = [self.m_neg_lower, self.m_neg_5, self.m_neg_50, self.m_neg_95, self.m_neg_upper]
        return np.interp(p, p_values, multiplier_value)

    def draw_positive_effect_multiplier(self, p: float) -> float:
        """draws a multiplier for the positive effect.

        Args:
            p (float): the probability that determines the draw. Should be between [0,1].

        Returns:
            float: the drawn multiplier
        """

        if p < 0 or p > 1:
            raise ValueError(f"p must lie between 0 and 1, received value: {p}")
        p_values = [0, 0.05, 0.5, 0.95, 1]
        multiplier_value = [self.m_neg_lower, self.m_neg_5, self.m_neg_50, self.m_neg_95, self.m_neg_upper]
        return np.interp(p, p_values, multiplier_value)

    def draw_multiplier(self) -> float:
        """draws a multiplier for this factor.

        First it determines if the effect is positive or negative, then a multiplier is drawn
        from the respective cumulative distribution function that is defined for this factor.

        Returns:
            float: the drawn multiplier.
        """
        effect_draw = random.uniform(0, 1)
        multiplier_draw = random.uniform(0, 1)

        factor_level = None
        if multiplier_draw < 0.05:
            factor_level = FactorLevel.OBVIOUS
        elif multiplier_draw < 0.50:
            factor_level = FactorLevel.NOMINAL
        elif multiplier_draw < 0.95:
            factor_level = FactorLevel.MODERATE
        else:
            factor_level = FactorLevel.HIGH

        effect = 1  # if no effect takes place, the value is 1
        if effect_draw < self.p_negative_effect:
            effect = self.draw_negative_effect_multiplier(multiplier_draw)
        elif effect_draw > (1-self.p_positive_effect):
            effect = self.draw_positive_effect_multiplier(multiplier_draw)

        return effect, factor_level

    @classmethod
    def parse_from_file(cls, data_file_path):
        """parses all factors from a data file.

        The data file should be comma separated (.CSV) and have the following header:

            `,HOFs,Ne,No,Po,Mneg-5th,Mneg-50th,Mneg-95th,Mpos-5th,Mpos-50th,Mpos-95th`

        Note that the first column is unnamed, this column contains the index,
        which will be the name/identifier of each factor.

        Args:
            data_file_path (str): the path of the file containing the factors

        Returns:
            list[Factor]: the factors contained in the specified data file
        """
        factor_data = pd.read_csv(data_file_path, index_col=0, header=0)

        factors = []
        for index, row in factor_data.iterrows():
            factors.append(cls(
                name=index, description=row["HOFs"],
                p_negative_effect=row["Ne"], p_no_effect=row["No"], p_positive_effect=row["Po"],
                m_neg_5=row["Mneg-5th"], m_neg_50=row["Mneg-50th"], m_neg_95=row["Mneg-95th"],
                m_pos_5=row["Mpos-5th"], m_pos_50=row["Mpos-50th"], m_pos_95=row["Mpos-95th"],
                m_neg_lower=row["Mneg-lower"], m_neg_upper=row["Mneg-upper"],
                m_pos_lower=row["Mpos-lower"], m_pos_upper=row["Mpos-upper"]
            ))
        return factors
