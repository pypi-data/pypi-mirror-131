import inspect
import pkgutil
from typing import List

from test_executor.abstract_test.abstract_test import AbstractTest
from test_executor.test_generation.test_runnable import TestRunnable


class TestLoader(object):
    """
    This class loads tests from a given paths and generates runnables out of them
    """
    __test__ = False

    def __init__(self):
        self.number_of_test = 0

    def load_tests(self, tests_paths: List[str], tests_filter: str = "test_") -> List[TestRunnable]:
        """
        From a given list of paths to tests, a list of test runnables is returned

        :param tests_paths: paths to tests
        :param tests_filter: filter for choosing a test by its test function name
        :return: list of test runnables
        """
        tests = []
        for tests_path in tests_paths:
            tests += self._load_tests(tests_path, tests_filter)

        return tests

    def _load_tests(self, tests_path: str, tests_filter: str):
        tests = []

        for loader, sub_module, is_pkg in pkgutil.walk_packages([tests_path]):
            loaded = loader.find_module(sub_module).load_module(sub_module)
            cls_members = inspect.getmembers(loaded, inspect.isclass)
            for cls_mem in cls_members:
                if issubclass(cls_mem[1], AbstractTest) and cls_mem[1].__name__ != AbstractTest.__name__:
                    test_class = cls_mem[1]()
                    test_functions = [function_name for function_name, _ in inspect.getmembers(test_class,
                                                                                               inspect.ismethod)
                                      if function_name.startswith(tests_filter) and
                                      function_name not in AbstractTest.abstract_test_methods]
                    for function_name in test_functions:
                        class_instance = cls_mem[1]()
                        runnable = TestRunnable(test_function=getattr(class_instance, function_name),
                                                test_class=class_instance,
                                                test_number=self.number_of_test)
                        tests.append(runnable)
                        self.number_of_test += 1

        return tests
