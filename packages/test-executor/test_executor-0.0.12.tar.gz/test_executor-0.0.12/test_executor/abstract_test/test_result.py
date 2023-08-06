from enum import Enum

from typing import List


class TestVerdict(Enum):
    """
    Enum for test verdicts
    """
    PASSED = "Passed"
    FAILED = "Failed"
    ABORTED = "Aborted"


class TestResult(object):
    """
    This class is a class data that contains data about a test
    """
    verdict: TestVerdict
    failure_reasons: List[str]

    def __init__(self, test_name: str, test_number: int):
        self.test_name = test_name
        self.verdict = TestVerdict.PASSED
        self.failure_reasons = []
        self.test_log = ""
        self.test_number = test_number

    def __repr__(self):
        return f"Test Name: {self.test_name} - Verdict: {self.verdict} - " \
               f"Failures: {', '.join(self.failure_reasons) if self.failure_reasons else 'None'}"
