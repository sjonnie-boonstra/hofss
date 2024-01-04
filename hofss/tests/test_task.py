from unittest import TestCase

from ..src.task import Task


class GreetTest(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_instance = Task()
        return super().setUpClass()

    def test_no_value(self):
        self.assertEqual(self.test_instance.greet(), "Hello world!")
        return

    def test_with_value(self):
        self.assertEqual(self.test_instance.greet("there"), "Hello there!")
        return
