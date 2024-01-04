from ..data_structures import Actor, Scenario, Parameter, Organization, TaskType


class Task:

    def greet(self, name: str = None) -> str:
        if name is None:
            name = "world"
        return f"Hello {name}!"

    pass
