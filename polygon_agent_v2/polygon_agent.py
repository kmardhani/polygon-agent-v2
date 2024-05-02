from dotenv import load_dotenv
import os
import autogen
from autogen.coding import DockerCommandLineCodeExecutor
from .get_stock_data_from_polygon import (
    get_stock_data_from_polygon,
    get_stock_data_from_Polygon_description,
    param_from_date_description,
    param_ticker_description,
    param_to_date_description,
)

"""
Class to handle Autogen agents for Polygon agent.
"""


class PolygonAgent:

    assistant = None
    user_proxy = None

    def __init__(self):

        load_dotenv()

        config_list = [{"model": "gpt-4-turbo", "api_key": os.getenv("OPENAI_API_KEY")}]

        custom_function_list = [
            {
                "name": "get_stock_data_from_polygon",
                "description": get_stock_data_from_Polygon_description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker": {
                            "type": "string",
                            "description": param_ticker_description,
                        },
                        "from_date": {
                            "type": "string",
                            "description": param_from_date_description,
                        },
                        "to_date": {
                            "type": "string",
                            "description": param_to_date_description,
                        },
                    },
                    "required": ["ticker", "from_date", "to_date"],
                },
            }
        ]

        llm_config = {
            "timeout": 600,
            "seed": 42,
            "config_list": config_list,
            "temperature": 0,
            "functions": custom_function_list,
        }

        assistant_system_message = """
        You are responsible for answering stock price related question.
        Assume there is no python function to execute python code.
        You can only suggest to run the python code in local enviornment.
        Assum no new python modules can be installed in the local enviornment
        """

        self.assistant = autogen.AssistantAgent(
            name="Polygon assistant",
            system_message=assistant_system_message,
            llm_config=llm_config,
        )

        # Create a Docker command line code executor.
        executor = DockerCommandLineCodeExecutor(
            image="python:3.12-slim",
            timeout=10,  # Timeout for each code execution in seconds.
            work_dir=os.getenv(
                "WORK_DIR"
            ),  # Use the temporary directory to store the code files.
        )

        self.user_proxy = autogen.UserProxyAgent(
            name="Polygon user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=5,
            is_termination_msg=lambda x: x.get("content", "")
            and x.get("content", "").rstrip().endswith("TERMINATE"),
            code_execution_config={"executor": executor},
            llm_config=llm_config,
            function_map={
                "get_stock_data_from_polygon": get_stock_data_from_polygon,
            },
            system_message="""Reply TERMINATE if the task has been solved at full satisfaction.  Otherwise, reply CONTINUE, or the reason why the task is not solved yet""",
        )

    def initiate_session(self, question: str) -> str:
        self.user_proxy.initiate_chat(self.assistant, message=question)
        return self.assistant.last_message()['content'] + "--" + self.user_proxy.last_message()['content']
