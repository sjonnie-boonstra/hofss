from dataclasses import dataclass, field
import pandas as pd

from .factor import Factor

@dataclass
class TaskType:
    """Datastructure containing properties of a task type"""
    name: str
    description: str = ""
    factors: list[Factor] = field(default_factory=list)
    nhep: float = 1.0

    @classmethod
    def parse_from_file(cls, data_file_path: str, hofs: dict[str, Factor]):
        factor_lookup_table = {factor.name: factor for factor in hofs}
        task_type_data = pd.read_csv(data_file_path, index_col=0)
        task_types = []
        for index, row in task_type_data.iterrows():

            factors = []
            for factor_index in range(1,15):
                factor_name = f"F{factor_index}"
                if row[factor_name].lower() == "y":
                    factors.append(factor_lookup_table[factor_name])

            task_types.append(cls(name=index,description=row["GTT"],factors=factors,nhep=row["NHEP-EOC"]))
        return task_types
    