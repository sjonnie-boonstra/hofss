import numpy as np
import pandas as pd

from .task import Task
from ..data_structures import TaskType


class Check(Task):

    determine_hep = Task.__dict__['determine_hep']

    def __init__(self, task_type: TaskType):
        self.task_type = task_type
        return

    def do_check(self, task_result: pd.Series, rng: np.random.Generator = None) -> pd.Series:

        if rng is None:
            rng = np.random.default_rng()

        error_occurred = bool(task_result["scenario"] is not None)
        error_corrected = False
        check_result = {}
        if error_occurred:
            # hep_data = self.determine_hep(rng=rng)
            # check_hep = hep_data["hep"]
            # error_corrected = bool(check_hep < rng.uniform(0, 1))
            error_corrected = bool(0.72 > rng.uniform(0, 1))
            # for index, value in hep_data.items():
            #     check_result[f"check_{index}"] = value

        check_result["error_occurred"] = error_occurred
        check_result["error_corrected"] = error_corrected

        return pd.Series(check_result)
