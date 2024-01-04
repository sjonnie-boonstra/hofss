from unittest import TestCase

from ..src.task import Task, Structure
from ..data_structures import Actor, TaskType, Factor


class CreateTaskTest(TestCase):

    def test_minimal_input_initialization(self):
        Task(
            name="test_task",
            factors=[],
            assignee=Actor("test_actor", factors=[]),
            task_type=TaskType.TASK_ONE
        )
        return


class PropertiesTest(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_instance = Task(
            name="test_task",
            factors=[],
            assignee=Actor("test_actor_1", factors=[]),
            task_type=TaskType.TASK_ONE
        )
        return super().setUpClass()

    def test_factors(self):

        # wrong input
        with self.assertRaises(TypeError) as cm:
            self.test_instance.factors = "factor_1 and factor_2"
        self.assertIn("factors should be an iterable and not of type str", str(cm.exception))
        with self.assertRaises(TypeError) as cm:
            self.test_instance.factors = 2
        self.assertIn("factors should be an iterable and not of type str", str(cm.exception))
        with self.assertRaises(TypeError) as cm:
            self.test_instance.factors = [
                Factor(name="factor_1", value=1.5),
                "not a factor",
                Factor(name="factor_3", value=3.5)
            ]
        self.assertIn("item at index '1' is not of type: Factor; received:", str(cm.exception))

        # correct input
        self.test_instance.factors = [
            Factor(name="factor_a", value=1.7),
            Factor(name="factor_b", value=4.7)
        ]
        self.assertEqual(len(self.test_instance.factors), 2)
        self.assertEqual(self.test_instance.factors[0].name, "factor_a")
        self.assertEqual(self.test_instance.factors[0].value, 1.7)
        self.assertEqual(self.test_instance.factors[1].name, "factor_b")
        self.assertEqual(self.test_instance.factors[1].value, 4.7)

        return

    def test_assignee(self):

        # wrong input
        with self.assertRaises(TypeError) as cm:
            self.test_instance.assignee = "wrongly_defined_test_actor"
        self.assertIn("assignee should be of type: Actor; received:", str(cm.exception))

        # correct input
        self.test_instance.assignee = Actor("test_actor_2", factors=[])
        self.assertEqual(self.test_instance.assignee.name, "test_actor_2")
        return

    def test_name(self):

        # wrong input
        with self.assertRaises(TypeError) as cm:
            self.test_instance.name = 2
        self.assertIn("name should be of type: str; received:", str(cm.exception))

        # correct input
        self.test_instance.name = "test_task_renamed"
        self.assertEqual(self.test_instance.name, "test_task_renamed")
        return

    def test_structure(self):

        # wrong input
        with self.assertRaises(TypeError) as cm:
            self.test_instance.structure = "wrongly defined structure"
        self.assertIn("structure should be of type: Structure; received:", str(cm.exception))

        # correct input
        self.test_instance.structure = Structure(name="test_structure")
        self.assertEqual(self.test_instance.structure.name, "test_structure")
        return

    def test_task_type(self):

        # wrong input
        with self.assertRaises(TypeError) as cm:
            self.test_instance.task_type = "wrongly defined task type"
        self.assertIn("task_type should be castable to enum: TaskType; received error:", str(cm.exception))

        # correct input
        self.test_instance.task_type = TaskType.TASK_ONE
        self.test_instance.task_type = "TASK_ONE"
        self.assertEqual(self.test_instance.task_type, TaskType.TASK_ONE)
        return
