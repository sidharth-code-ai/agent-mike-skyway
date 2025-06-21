import asyncio
from google.genai import types


async def call_agent_async(runner, user_id: str, session_id: str, query: str) -> str:
    """
    Send a user query to the ADK runner and return the final assistant reply as text.

    Args:
        runner: The ADK Runner instance.
        user_id (str): Unique ID for the user session.
        session_id (str): ID of the ADK session.
        query (str): The user's message to send to the agent.

    Returns:
        str: The agent's final text response.
    """
    # Build the user content
    content = types.Content(role="user", parts=[types.Part(text=query)])
    final_response = ""

    # Stream events and capture the final response
    async for event in runner.run_async(
        user_id=user_id, session_id=session_id, new_message=content
    ):
        if event.is_final_response() and event.content and event.content.parts:
            part = event.content.parts[0]
            if hasattr(part, "text") and part.text:
                final_response = part.text.strip()

    return final_response
