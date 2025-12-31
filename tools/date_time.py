from langchain_core.tools import tool
from datetime import datetime

@tool
def get_current_date_time() -> str:
    """Returns the current date and time. Useful when user asks for time, date, or 'what day is it?'"""
    now = datetime.now()
    return now.strftime("%A, %B %d, %Y at %I:%M %p")
