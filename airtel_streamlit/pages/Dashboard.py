from utils.styles import load_css
import streamlit as st

from api import APIClient


st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide",
)

load_css()

# ---------------------------------
# Authentication Check
# ---------------------------------

if not st.session_state.get("logged_in"):
    st.warning("Please login first.")
    st.stop()


# ---------------------------------
# Load User
# ---------------------------------

user = st.session_state.get("user")

if user is None:

    response = APIClient.me()

    if response.status_code == 200:
        user = response.json()
        st.session_state.user = user
    else:
        st.error("Unable to load user.")
        st.stop()


# ---------------------------------
# Load Tickets
# ---------------------------------

tickets = []

try:

    response = APIClient.get_my_tickets()

    if response.status_code == 200:
        tickets = response.json()

except:
    tickets = []


# ---------------------------------
# Ticket Statistics
# ---------------------------------

total = len(tickets)

open_count = 0
closed_count = 0
in_progress = 0

for ticket in tickets:

    status = ticket["status"]

    if status == "OPEN":
        open_count += 1

    elif status == "IN_PROGRESS":
        in_progress += 1

    elif status == "CLOSED":
        closed_count += 1


# ---------------------------------
# Header
# ---------------------------------

st.title("📊 Dashboard")

st.write(
    f"Welcome back **{user['full_name']}** 👋"
)

st.divider()


# ---------------------------------
# Metrics
# ---------------------------------

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Total Tickets",
        total,
    )

with c2:
    st.metric(
        "Open",
        open_count,
    )

with c3:
    st.metric(
        "In Progress",
        in_progress,
    )

with c4:
    st.metric(
        "Closed",
        closed_count,
    )


st.divider()


# ---------------------------------
# Customer Details
# ---------------------------------

left, right = st.columns(2)

with left:

    st.subheader("👤 Customer Information")

    st.write(f"**Customer ID:** {user['customer_id']}")
    st.write(f"**Email:** {user['email']}")
    st.write(f"**Mobile:** {user['mobile_number']}")

with right:

    st.subheader("📡 Airtel Services")

    st.write(f"**Service:** {user['service_type']}")
    st.write(f"**Customer Type:** {user['customer_type']}")
    st.write(f"**Circle:** {user['circle']}")
    st.write(f"**Language:** {user['preferred_language']}")


st.divider()


# ---------------------------------
# Recent Tickets
# ---------------------------------

st.subheader("🎫 Recent Tickets")

if len(tickets) == 0:

    st.info("No tickets found.")

else:

    for ticket in tickets[:5]:

        with st.expander(
            f"#{ticket['id']} - {ticket['title']}"
        ):

            st.write(
                f"**Priority:** {ticket['priority']}"
            )

            st.write(
                f"**Status:** {ticket['status']}"
            )

            st.write(ticket["description"])


st.divider()


# ---------------------------------
# Quick Actions
# ---------------------------------

st.subheader("⚡ Quick Actions")

a, b, c = st.columns(3)

with a:
    st.info(
        "🎫 Create a new support ticket from the Tickets page."
    )

with b:
    st.info(
        "📄 Upload Airtel documentation from the Knowledge page."
    )

with c:
    st.info(
        "🤖 Chat with the AI Assistant using your uploaded documents."
    )