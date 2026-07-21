from utils.styles import load_css
import streamlit as st

from auth import (
    initialize_session,
    login_page,
    logout,
)
from api import APIClient


# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="Airtel Customer Support AI",
    page_icon="📱",
    layout="wide",
)
load_css()

initialize_session()


# -----------------------------------
# Login Screen
# -----------------------------------

if not st.session_state.logged_in:
    login_page()
    st.stop()


# -----------------------------------
# Verify User
# -----------------------------------

if st.session_state.user is None:

    response = APIClient.me()

    if response.status_code == 200:

        st.session_state.user = response.json()

    else:

        st.session_state.logged_in = False
        st.session_state.token = None
        st.rerun()


user = st.session_state.user


# -----------------------------------
# Sidebar
# -----------------------------------

with st.sidebar:

    st.title("📱 Airtel AI")

    st.divider()

    st.write(f"**{user['full_name']}**")
    st.caption(user["email"])

    st.write("")

    st.success("Logged In")

    st.divider()

    st.info(
        """
Use the navigation menu on the left
to access:

• Dashboard

• Tickets

• Knowledge

• Chat
"""
    )

    st.divider()

    if st.button(
        "Logout",
        use_container_width=True,
    ):
        logout()


# -----------------------------------
# Main Page
# -----------------------------------

st.title("🚀 Airtel Customer Support AI")

st.success(
    f"Welcome back, {user['full_name']}!"
)

st.write(
    """
This portal provides AI-powered customer support for Airtel users.

Use the navigation menu on the left to access all available modules.
"""
)

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Customer ID",
        user["customer_id"],
    )

    st.metric(
        "Service",
        user["service_type"],
    )

with col2:

    st.metric(
        "Customer Type",
        user["customer_type"],
    )

    st.metric(
        "Circle",
        user["circle"],
    )

st.divider()

st.subheader("Available Modules")

c1, c2 = st.columns(2)

with c1:

    st.markdown(
        """
### 🎫 Ticket Management

- Create Tickets
- View Your Tickets
- Update Tickets
- Delete Tickets
"""
    )

with c2:

    st.markdown(
        """
### 🤖 AI Knowledge Base

- Upload PDFs
- AI Chatbot
- Conversation History
- RAG Search
"""
    )