import os
from pathlib import Path
from autogen import AssistantAgent
from utility.prompt import classifier_prompt 
from dotenv import load_dotenv
from utility.llm_config import llm_config

load_dotenv()

def get_classifier_agent():
    agent_cls = AssistantAgent(
        name="ClassifierAgent",
        llm_config=llm_config,
        system_message = classifier_prompt
    )
    return agent_cls