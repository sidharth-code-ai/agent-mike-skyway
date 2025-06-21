import requests
from google.adk.tools import ToolContext
import os
from dotenv import load_dotenv

load_dotenv()


def book_viewing(
    name: str,
    phoneNumber: str,
    time: str,
    propertyAddress: str,
    timezone: str,
    tool_context: ToolContext,
) -> dict:
    """
    Call this function to schedule a personalized property viewing for a potential client.
    This is typically triggered after a lead expresses interest in a property and is ready to book a visit.

    Usage:
        This function can be used within automated workflows or AI agents to collect user details and book viewings.
        Ensure that all required fields (name, phone number, and time) are provided before calling.

    Args:
        name (str): Full name of the client requesting the viewing.
        phoneNumber (str): Valid contact number for follow-up and confirmation with country Code (Eg: "+919495972317","+17012266051").
        time (str): A Natural Language Descriptive Word of the Time  When The User Would Like To Book An Appointment. E.g. Thursday At 02:30 PM, Monday 01:30 PM, Wednesday 09:00 AM , Tomorrow 05:00 PM , The Day After Tomorrow 08:00 AM.
        timezone (str, optional): Timezone for the provided time.
    """
    url = os.getenv("BOOKING_LINK")
    payload = {
        "name": name,
        "phoneNumber": phoneNumber,
        "time": time,
        "timezone": timezone,
    }
    try:
        response = requests.post(url=url, json=payload)
        return {"status": "success", "message": response.text}
    except Exception as e:
        return {
            "status": "failure",
            "message": "There was an issue trying to book the viewing, please try again later.",
        }
