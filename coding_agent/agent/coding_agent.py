import os
import ast
from autogen import AssistantAgent, UserProxyAgent, ChatResult
from autogen.coding import LocalCommandLineCodeExecutor
from coding_agent.config import LLM_CONFIG

# Directory for coding tasks
CODING_DIR = "coding_directory"

PROMPT_TEMPLATE = """
You are an expert Python coding assistant. Your task is to solve programming challenges by writing Python code, verifying its correctness, and presenting the final solution.

Use the following format:

Question: the coding task you need to solve
Thought: carefully consider what needs to be done and which tool to use first
Action: the action you need to take using one of the provided tools
Action Input: the input to the action, such as a task description or function name
Observation: the result of the action based on the tool's output
... (this thought/action/action input/observation sequence can repeat as many times as necessary)
Thought: I now have the final solution, which has been verified
Final Answer: the final Python code solution, verified, formatted, and ready for presentation

Begin! DO NOT BREAK AWAY FROM THIS FORMAT.
Question: {input}
"""

def format_prompt(sender, recipient, contenxt):
    """Format the prompt message with the given question."""
    return PROMPT_TEMPLATE.format(input=contenxt["question"])

def initialize_coding_agent():
    """Initialize the coding agent."""
    return AssistantAgent(
        name="Coding Assistant",
        system_message="""
        You are an AI assistant for writing and verifying Python code. 
        Your tasks include:
        - Writing Python functions based on prompts.
        - Creating tests to verify code correctness.
        - Providing feedback on incorrect code and suggesting fixes.
        - Ensuring the code passes tests and presenting the verified solution.

        Respond with "TERMINATE" when the task is fully complete.
        """,
        llm_config=LLM_CONFIG,
    )

def initialize_user_proxy(executor):
    """Initialize the user proxy agent."""
    return UserProxyAgent(
        name="User",
        llm_config=False,
        is_termination_msg=lambda x: x.get("content", "").strip().lower().endswith("terminate"),
        human_input_mode="NEVER",
        max_consecutive_auto_reply=10,
        code_execution_config={"executor": executor},
    )

def create_code_executor():
    """Create a local code executor."""
    return LocalCommandLineCodeExecutor(
        timeout=100,
        work_dir=CODING_DIR,
    )

def setup_agents():
    """Set up and return the agents."""
    executor = create_code_executor()
    return initialize_user_proxy(executor), initialize_coding_agent()

def extract_final_answer(chat_result):
    """Extract the final answer from the chat history."""
    for message in reversed(chat_result.chat_history):
        content = message.get("content", "").lower()
        if "final answer:" in content:
            final_answer = message["content"].split("Final Answer:")[1].strip()
            return f"\n{final_answer}"
    return None

def main():
    os.environ["AUTOGEN_USE_DOCKER"] = "False"
    
    # Set up agents
    user_proxy, coding_agent = setup_agents()

    # Define the task
    task_description = "Write a Python function that takes a list of numbers and returns the average of the numbers."

    # Start the conversation
    chat_result = user_proxy.initiate_chat(
        coding_agent,
        message=format_prompt,
        question=task_description,
    )

    # Extract and display results
    final_solution = extract_final_answer(chat_result)
    
    print("Final Answer:", final_solution)

if __name__ == "__main__":
    main()
