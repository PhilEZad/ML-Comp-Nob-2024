import unittest

class AgentTestCase(unittest.TestCase):
    """
    Base class for all agent evaluation tests.
    Subclasses must implement the `run_agent` method to specify how the agent operates.

    Attributes:
        input_data: The input data provided to the agent for evaluation.
        expected_output: The expected final response from the agent.
        expected_steps: The expected sequence of steps the agent should execute.
        expected_arguments: The expected arguments the agent should pass to tools.
        final_response_correct: Indicates whether the agent's final response matches the expected output.
    """
    def __init__(self, methodName: str = "run_test", input_data=None, expected_output=None, 
                 expected_steps=None, expected_arguments=None) -> None:
        super(AgentTestCase, self).__init__(methodName)
        self.input_data = input_data
        self.expected_output = expected_output
        self.expected_steps = expected_steps
        self.expected_arguments = expected_arguments
        self.final_response_correct = False
        self.steps_executed_correct = False

    def run_test(self):
        """
        Executes the test by running the agent and comparing its output, steps, and arguments
        to the expected values. Marks the test as failed if any mismatch occurs.
        """
        # Run the agent and obtain its final response, steps, and arguments
        final_response, steps_executed, arguments_passed = self.run_agent()

        # Validate the final response against the expected output
        try:
            self.assertEqual(final_response, self.expected_output)
            self.final_response_correct = True
        except AssertionError:
            self.final_response_correct = False
            print(f"Final response mismatch for input '{self.input_data}'")

        # Validate the steps executed by the agent
        try:
            self.assertEqual(steps_executed, self.expected_steps)
            self.steps_executed_correct = True
        except AssertionError:
            self.steps_executed_correct = False
            print(f"Steps executed mismatch for input '{self.input_data}'")

        # Validate the arguments passed to tools
        try:
            self.assertEqual(arguments_passed, self.expected_arguments)
        except AssertionError:
            print(f"Arguments passed mismatch for input '{self.input_data}'")

        # Fail the test if any of the validations fail
        if not self.final_response_correct or not self.steps_executed_correct \
           or arguments_passed != self.expected_arguments:
            self.fail("Test failed due to mismatch in response, steps, or arguments.")

    def run_agent(self):
        """
        Method to be implemented by subclasses to define agent execution.
        """
        raise NotImplementedError("Subclasses must implement the run_agent method")


class AgentTestResult(unittest.TextTestResult):
    """
    Custom test result class to track detailed success metrics for agent tests.

    Attributes:
        correct_final_responses: Number of tests where the agent's final response matched the expected output.
        correct_steps_executed: Number of tests where the agent's steps matched the expected sequence.
        total_tests: Total number of tests executed.
    """
    def __init__(self, stream, descriptions, verbosity):
        super(AgentTestResult, self).__init__(stream, descriptions, verbosity)
        self.correct_final_responses = 0
        self.correct_steps_executed = 0
        self.total_tests = 0

    def addSuccess(self, test):
        """
        Overrides the default success handler to update custom success metrics.
        """
        super(AgentTestResult, self).addSuccess(test)
        self.total_tests += 1
        if getattr(test, 'final_response_correct', False):
            self.correct_final_responses += 1
        if getattr(test, 'steps_executed_correct', False):
            self.correct_steps_executed += 1

    def addFailure(self, test, err):
        """
        Overrides the default failure handler to track total tests executed.
        """
        super(AgentTestResult, self).addFailure(test, err)
        self.total_tests += 1

    def addError(self, test, err):
        """
        Overrides the default error handler to track total tests executed.
        """
        super(AgentTestResult, self).addError(test, err)
        self.total_tests += 1
