import os
import uuid
from datetime import datetime
from typing import Tuple, Any
from flaml.autogen import AssistantAgent
from coding_agent.config import LLM_CONFIG


def generate_unique_filename(base_name: str, extension: str, directory: str) -> str:
    """
    Generate a unique filename with a timestamp and UUID.

    :param base_name: The base name for the file.
    :param extension: The file extension (e.g., '.py').
    :param directory: The directory where the file will be saved.
    :return: A unique filename with the specified directory.
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = uuid.uuid4()
    filename = f"{base_name}_{timestamp}_{unique_id}{extension}"
    return os.path.join(directory, filename)


def initialize_code_agent() -> AssistantAgent:
    """
    Initialize and configure the code-writing assistant agent.

    :return: A configured instance of AssistantAgent.
    """
    return AssistantAgent(
        name="Code Writing Agent",
        system_message=(
            "You are an expert Python developer. Your task is to generate a Python function "
            "based on the given description. Ensure the code is clean, well-commented, and correct. "
            "Do not include code blocks or any text outside the code itself."
        ),
        is_termination_msg=lambda msg: "FINISH" in msg.get("content", ""),
        llm_config=LLM_CONFIG,
        human_input_mode="NEVER",
    )


def generate_code(prompt: str, agent: AssistantAgent) -> str:
    """
    Use the assistant agent to generate Python code based on the given prompt.

    :param prompt: The task description for generating the code.
    :param agent: The assistant agent used to generate the code.
    :return: The generated Python code as a string.
    """
    messages = [
        {
            "role": "user",
            "content": (
                f"Write a Python function based on the following task: {prompt}. "
                "Do not include anything other than the code. Avoid using code blocks or extra text."
            ),
        }
    ]
    reply = agent.generate_reply(messages=messages)

    if not reply:
        raise ValueError("No reply received from the agent.")

    reply_content = reply.get("content", "").replace("\nFINISH", "").strip()
    if not reply_content:
        raise ValueError("Agent's reply contained no valid content.")

    return reply_content.replace("```python", "").replace("```", "").strip()


def save_code_to_file(code: str, directory: str) -> str:
    """
    Save the generated Python code to a uniquely named file.

    :param code: The Python code to save.
    :param directory: The directory where the file will be saved.
    :return: The full path of the saved file.
    """
    os.makedirs(directory, exist_ok=True)
    file_path = generate_unique_filename("generated_code", ".py", directory)
    with open(file_path, "w") as file:
        file.write(code)
    return file_path


def write_function(prompt: str) -> Tuple[Any, str]:
    """
    Generate Python code from a prompt and save it to a file.

    :param prompt: The task description for generating the code.
    :return: A tuple containing the generated code and the file path.
    """
    coding_directory = "coding_directory"

    # Initialize the code agent
    code_agent = initialize_code_agent()

    # Generate the code
    code = generate_code(prompt, code_agent)

    # Save the code to a file
    code_file_path = save_code_to_file(code, coding_directory)

    return code, code_file_path
