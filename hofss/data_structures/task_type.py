from dataclasses import dataclass, field
import pandas as pd

from .factor import Factor


@dataclass
class TaskType:
    """Datastructure containing properties of a task type"""

    name: str
    "the name of this task type"
    description: str = ""
    "the description of this task type"
    factors: list[Factor] = field(default_factory=list)
    "the factors that influence a task of this type"
    nhep: float = 1.0
    "the nominal Human Error Probability (HEP) of a task of this type"

    @classmethod
    def parse_from_file(cls, data_file_path: str, hofs: dict[str, Factor]):
        """parses all task types from a data file.

        The data file should be comma separated (.CSV) and have the following header:

            `,GTT,NHEP-EOC,F1,F2,F3,F4,F5,F6,F7,F8,F9,F10,F11,F12,F13,F14`

        Note that the first column is unnamed, this column contains the index,
        which will be the name/identifier of each task type.

        Args:
            data_file_path (str): the path of the file containing the task types

        Returns:
            list[TaskType]: the task types contained in the specified data file
        """
        factor_lookup_table = {factor.name: factor for factor in hofs}
        task_type_data = pd.read_csv(data_file_path, index_col=0)
        task_types = []
        for index, row in task_type_data.iterrows():

            factors = []
            for factor_index in range(1, 15):
                factor_name = f"F{factor_index}"
                if row[factor_name].lower() == "y":
                    factors.append(factor_lookup_table[factor_name])

            task_types.append(cls(name=index, description=row["GTT"], factors=factors, nhep=row["NHEP-EOC"]))
        return task_types
