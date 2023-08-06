import logging
import os
import pprint
import threading
from typing import List, Dict

from test_executor.abstract_test.abstract_test import AbstractTest
from test_executor.abstract_test.test_result import TestResult
from test_executor.common import DEFAULT_LOGS_FOLDER
from test_executor.logger_factory.logger_factory import LoggerFactory
from test_executor.test_generation.test_runnable import TestRunnable


class TestExecutor(object):
    """
    Class that executes a list of runnables
    """
    _logger: logging.Logger
    _results: List[TestResult]
    _concurrency_level: int
    _logs_folder: str

    __test__ = False

    def __init__(self, logs_folder: str = DEFAULT_LOGS_FOLDER, concurrency_level: int = 1):
        """
        :param logs_folder: path to logs folder
        :param concurrency_level: concurrency level for executing the tests
        """
        self._logs_folder = logs_folder
        self._concurrency_level = concurrency_level
        self._results = []
        self._logger = LoggerFactory.generate_logger(os.path.join(self._logs_folder, "session.log"))

    @property
    def Logger(self) -> logging.Logger:
        return self._logger

    def execute(self, test_runnables: List[TestRunnable], listener=None,
                custom_params: Dict[str, Dict[str, str]] = None) -> List[TestResult]:
        """
        Executes that list of given test runnables.
        If concurrency is not 1, we will execute the tests in batches by their order.

        :param test_runnables: list of runnables
        :param listener: a listener that will be notified on all of the tests results
        :param custom_params: custom parameters for the tests
        """
        if listener:
            TestExecutor._register_listener_to_runnables(test_runnables, listener)

        if custom_params:
            TestExecutor._set_test_params(test_runnables, custom_params)

        test_batches = self._get_test_batches(test_runnables)

        for batch in test_batches:
            batch_threads = []
            for test_runnable in batch:
                test_t = threading.Thread(target=self._run_single_runnable, args=(test_runnable,))
                test_t.start()
                batch_threads.append([test_t, test_runnable])

            while batch_threads:
                for i, batch_part in enumerate(batch_threads):
                    test_t, test_runnable = batch_part
                    test_t.join(timeout=1)
                    if not test_t.is_alive():
                        self._logger.info(f"The test '{test_runnable}' finished its execution")
                        del batch_threads[i]
                    else:
                        self._logger.info(f"The test '{test_runnable}' is still running")

        summary = pprint.pformat(self._results, indent=4, width=120).replace("[", "").replace("]", "").splitlines()
        final_summary = []
        for result in summary:
            result = result.rsplit(",", 1)[0].strip()
            final_summary.append(result)
        final_summary = "\n".join(final_summary)
        self._logger.info(f"Execution Summary:\n{final_summary}")
        return self._results

    def _run_single_runnable(self, test_runnable: TestRunnable):
        result = test_runnable.run(logs_folder=self._logs_folder)
        self._results.append(result)

    def _get_test_batches(self, test_runnables):
        test_batches = []
        num_of_runnables = len(test_runnables)
        for i in range(0, len(test_runnables), self._concurrency_level):
            test_batches.append(test_runnables[i:min(num_of_runnables, i + self._concurrency_level)])
        return test_batches

    @staticmethod
    def _register_listener_to_runnables(test_runnables: List[TestRunnable], listener):
        for test in test_runnables:
            test.register_listener(listener)

    @classmethod
    def _set_test_params(cls, test_runnables, custom_params):
        for test_runnable in test_runnables:
            test_class_name = test_runnable._test_class.__class__.__name__
            test_name = str(test_runnable)
            if test_name in custom_params:
                cls._set_params(test_runnable._test_class, custom_params[test_name])

            if test_class_name in custom_params:
                cls._set_params(test_runnable._test_class, custom_params[test_class_name])

    @classmethod
    def _set_params(cls, test_class: AbstractTest, params: dict):
        for param_name, param_val in params.items():
            test_class.params[param_name] = param_val
