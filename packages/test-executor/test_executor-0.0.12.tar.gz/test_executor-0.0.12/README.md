# Test Executor

## Introduction
This module allows you to execute tests in serial and parallel mode.
A test's flow defined by this module is as follows:
* **setup** - general configurations for starting th test
* **pre_test** - this should be defined specifically per test class if needed
* **test** - the test logic itself
* **post_test** - same as for pre_test
* **cleanup** - cleans what is needed after the test's flow is done

Main one can create a general test class that will implement the "setup" and "cleanup" steps, let other test classes 
inherit from it and then implement any specific logic for pre_test and/or post_test if needed.

## Testing Example

### Tests execution
Test execution can be done as follows:
```
# Load the tests needed from a list of paths
loaded_tests = TestLoader.load_tests(test_paths)

# Creating a new test executor with the required concurrency level
test_executor = TestExecutor(concurrency_level=concurrency)

# Starting the execution and getting the results
test_executor.Logger.info("*" * 32 + " Start Execution " + "*" * 32)
results = test_executor.execute(loaded_tests, listener=listener)
test_executor.Logger.info("*" * 32 + " End Execution " + "*" * 32)
```

### Tests implementation
The following is an example for a basic class implementation, as you can also see
a fully configured logger is available during the execution:

```
from test_executor.abstract_test.abstract_test import AbstractTest
class ExampleTest(AbstractTest):
    def setup(self):
        self.logger.info(f"Setup 1")

    def cleanup(self):
        self.logger.info(f"Cleanup 1")

    def test_1(self):
        self.logger.info(f"Test 1")

    def test_2(self):
        self.logger.info(f"Test 2")
```


The logger available is configured separately for each test, so that each
test will have their own logs. Logs will be saved be default under a "logs"
folder in the current working directory. Each execution that contains 1 test 
or more will generate a logs folder in the following format: 
```
{DAY}-{MONTH}-{YEAR}_{HOUR}-{MINUTE}-{SECOND}-{MICROSECONDS}
```
Under this folder each test will create its own test folder in the following
format:
```
{TEST_NUMBER}_{TEST_CLASS_NAME}.{TEST_METHOD_NAME}
```
