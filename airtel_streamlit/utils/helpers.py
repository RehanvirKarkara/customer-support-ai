from datetime import datetime


def format_datetime(value):

    if not value:
        return "-"

    try:

        dt = datetime.fromisoformat(value)

        return dt.strftime("%d %b %Y %I:%M %p")

    except:

        return value


def status_icon(status):

    icons = {
        "OPEN": "🟢",
        "IN_PROGRESS": "🟡",
        "CLOSED": "🔴",
    }

    return icons.get(status, "⚪")


def priority_icon(priority):

    icons = {
        "LOW": "🟢",
        "MEDIUM": "🟡",
        "HIGH": "🔴",
    }

    return icons.get(priority, "⚪")