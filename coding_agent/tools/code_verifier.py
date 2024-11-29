import os
import subprocess
from typing import Tuple
from autogen import ConversableAgent

from coding_agent.config import LLM_CONFIG


def create_test_agent():
    """
    Create and configure the testing agent.
    """
    return ConversableAgent(
        name="Test Generation Agent",
        system_message=(
            "You are a testing expert. Your task is to generate a test suite for a given Python function. "
            "Ensure that the tests are comprehensive and cover edge cases."
        ),
        is_termination_msg=lambda msg: "FINISH" in msg.get("content", ""),
        llm_config=LLM_CONFIG,
    )


def generate_test_code(agent, source_code: str) -> str:
    """
    Use the test generation agent to create a test suite for the provided Python function.
    """
    messages = [
        {
            "role": "user",
            "content": (
                f"Generate a unittest for the following Python function source code:\n\n{source_code}\n\n"
                'Return the test code and end with "FINISH". Only include the code—no code blocks or extra text.'
            ),
        }
    ]
    reply = agent.generate_reply(messages=messages)

    if not reply:
        raise ValueError("No reply received from the agent.")

    reply_content = reply.get("content", "").replace("\nFINISH", "").strip()
    if not reply_content:
        raise ValueError("Agent's reply contained no valid content.")

    return reply_content


def save_to_file(file_path: str, content: str):
    """
    Save the given content to a specified file, ensuring the directory exists.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as file:
        file.write(content)


def execute_test_file(test_file: str) -> Tuple[bool, str]:
    """
    Execute the test file and return the result.
    """
    try:
        result = subprocess.run(["python", test_file], check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stdout + "\n" + e.stderr


def verify_function(source_code: str, code_filename: str) -> Tuple[bool, str]:
    """
    Verify the correctness of a Python function by generating and executing a test suite.

    :param source_code: The source code of the function to test.
    :param code_filename: The filename of the source code file.
    :return: A tuple (bool, str) where the first element indicates if tests passed, and the second is the output.
    """
    coding_directory = os.path.dirname(code_filename)

    # Read function code from the source file
    with open(code_filename, "r") as code_file:
        source_code = code_file.read()

    # Create the test generation agent
    test_agent = create_test_agent()

    # Generate the test suite code
    test_code = generate_test_code(test_agent, source_code)

    print("Generated Test Code:", test_code)

    # Save the test suite to a file
    test_filename = code_filename.replace(".py", "_test.py")
    save_to_file(test_filename, test_code)

    # Execute the test suite and capture the results
    return execute_test_file(test_filename)
