from dotenv import load_dotenv

from google.genai import types
import google.genai.types as types
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts import InMemoryArtifactService
from .utils import load_instruction_from_file
from .tools.validation_tool import validate_events
from .tools.session_tool import assign_sessions
from .tools.dedup_tool import deduplicate_events
from .tools.load_data import load_event_file


#---------SubAgents--------
validation_agent = LlmAgent(
    name="validation_agent",
    model="gemini-2.0-flash",
    tools=[validate_events],
    instruction=load_instruction_from_file("instructions/validation_instruct.txt"),
    description="You are a data validation agent. Use the tool to validate event logs.",
    output_key="validated_state",
)

dedup_agent = LlmAgent(
    name="dedup_agent",
    model="gemini-2.0-flash",
    tools=[deduplicate_events],
    instruction=load_instruction_from_file("instructions/dedup_instruct.txt"),
    description="You are a deduplication agent. Removes duplicate entries from validated events.",
    output_key="dedup_state",
)

session_agent = LlmAgent(
    name="session_agent",
    model="gemini-2.0-flash",
    tools=[assign_sessions],
    description="Assigns session IDs to deduplicated user events and exports as CSV.",
    instruction=load_instruction_from_file("instructions/session_instruct.txt"),
    output_key="sessionized_events",
)

data_pipeline_agent = LlmAgent(
    name="data_pipeline_agent",
    model="gemini-2.0-flash",
    description="You are a pipeline controller agent. First, convert user input into structured events using available tools. Then orchestrate validation, deduplication, and add session using sub-agents in sequence.",
    instruction=load_instruction_from_file("instructions/data_pipeline_instruct.txt"),
    tools=[load_event_file],
    sub_agents=[validation_agent, dedup_agent, session_agent],
)
root_agent = data_pipeline_agent

# Runner setup
load_dotenv()
APP_NAME = "data_pipeline"
SESSION_ID = "session_001"
USER_ID = "user_001"

# Services
session_service = InMemorySessionService()
session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)

runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service
)

empty_message = types.Content(role="user", parts=[
    types.Part(text="Hi")
])

events = runner.run(
    user_id=USER_ID,
    session_id=SESSION_ID,
    new_message=empty_message
)

for event in events:
    if event.is_final_response():
        print("Agent Response:\n", event.content.parts[0].text)