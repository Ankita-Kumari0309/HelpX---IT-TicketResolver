from autogen import GroupChat , GroupChatManager ,UserProxyAgent

from agents.classifier_agent import get_classifier_agent
from agents.knowledge_base_agent import get_knowledge_base_agent
from utility.llm_config import llm_config
from tools.knowledge_base_tool import search_similar_solution
from agents.notification_agent import get_notification_agent
from tools.send_email import escalate_ticket_with_email

# Termination condition
def is_termination_msg(message):
    return isinstance(message,dict) and message.get("content","").strip().upper() == "TERMINATE"

# create agents
classifier = get_classifier_agent()
kb_agent = get_knowledge_base_agent()
notification_agent = get_notification_agent() 


# Binding the manually to agent
notification_agent.generate_reply = lambda messages,sender:escalate_ticket_with_email(
    issue=messages[0]["content"]
)

# Register tool with the KB agent
kb_agent.register_for_execution(
    name="search_similar_solution"
)(search_similar_solution)

# create user agent
user = UserProxyAgent(
    name="User",
    human_input_mode="TERMINATE",
    code_execution_config=False,
    is_termination_msg=is_termination_msg,
)

#create group chat with all agents
groupchat = GroupChat(
    agents=[user,classifier,kb_agent],
    messages=[],
    speaker_selection_method="Auto",
    allow_repeat_speaker=False,
    max_round=6
)

# create group chat manager
manager = GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config,
    is_termination_msg=is_termination_msg
)

if __name__ == '__main__':
    # triggering conversation
    user.initiate_chat(
        recipient=manager,
        message="Please resolve this : Outlook crashes every time I open it."

    )
