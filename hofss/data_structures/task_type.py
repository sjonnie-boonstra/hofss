from enum import Enum


class TaskType(Enum):
    """Different types of tasks within structural design"""

    TASK_ONE = "description of task 1"

    @classmethod
    def cast(cls, value: any):
        """tries to cast the specified value to an instance of the TaskType enum

        Args:
            value (any): the value to cast to an instance of the TaskType enum

        Raises:
            ValueError: if it is not possible to cast the specified value

        Returns:
            TaskType: the instance cast from the specified value
        """
        for member in cls:
            if isinstance(value, str):
                value = value.lower().strip()
                if member.name.lower() == value:
                    return member
                elif member.value.lower() == value:
                    return member
        raise ValueError(f"unable to cast value: '{value}' to an instance of '{cls.__name__}'")
