import asyncio
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from agent_mike.agent import root_agent
from utils import call_agent_async


load_dotenv()


# Create the Storage Databse of the presistent storage
db_url = "sqlite:///./my_agent_data.db"
session_sevice = DatabaseSessionService(db_url=db_url)
APP_NAME = "Memory Agent"


# Part 2: Define initial State
# Skip this as we don't have an initial state

# Part 3: Create a Runner
runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_sevice)

# GET EVENT LOOP FOR SYNC HANDLER


def chat(user_id: str, query: str) -> str:
    """
    Send a user query to the ADK agent under a persistent session.

    - Looks up or creates a session for `user_id`
    - Runs the agent with the given `query`
    - Returns the agent's final reply as plain text
    """

    # Get or create event loop
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Find or create sessions
    existing = session_sevice.list_sessions(app_name=APP_NAME, user_id=user_id)

    if existing.sessions:
        session_id = existing.sessions[0].id
    else:
        session_id = session_sevice.create_session(
            app_name=APP_NAME, user_id=user_id
        ).id

    # Run the agent and return its reply
    agent_reply = loop.run_until_complete(
        call_agent_async(runner, user_id, session_id, query)
    )
    return agent_reply
