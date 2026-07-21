from utils.styles import load_css
import streamlit as st

from api import APIClient


st.set_page_config(
    page_title="AI Chat",
    page_icon="🤖",
    layout="wide",
)

load_css()

# ---------------------------------------
# Authentication
# ---------------------------------------

if not st.session_state.get("logged_in"):
    st.warning("Please login first.")
    st.stop()


# ---------------------------------------
# Session Initialization
# ---------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None


st.title("🤖 Airtel AI Assistant")

st.caption(
    "Ask questions about Airtel services or your uploaded knowledge base."
)

st.divider()


# ---------------------------------------
# Sidebar - Conversation Controls
# ---------------------------------------

with st.sidebar:

    st.subheader("Conversation")

    if st.button(
        "🆕 New Conversation",
        use_container_width=True,
    ):
        st.session_state.messages = []
        st.session_state.conversation_id = None
        st.rerun()

    st.divider()

    st.write("Current Conversation")

    if st.session_state.conversation_id:
        st.success(
            f"Conversation #{st.session_state.conversation_id}"
        )
    else:
        st.info("New Conversation")


# ---------------------------------------
# Display Previous Messages
# ---------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if "sources" in message:

            if message["sources"]:

                with st.expander("Sources"):

                    for source in message["sources"]:
                        st.write(f"• {source}")


# ---------------------------------------
# Chat Input
# ---------------------------------------

prompt = st.chat_input(
    "Ask anything about Airtel..."
)

if prompt:

    # User Message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)

    # Assistant Message

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = APIClient.chat(
                question=prompt,
                conversation_id=st.session_state.conversation_id,
            )

            if response.status_code == 200:

                data = response.json()

                # -----------------------------
                # Flexible response parsing
                # -----------------------------

                answer = (
                    data.get("answer")
                    or data.get("response")
                    or data.get("message")
                    or "No response received."
                )

                conversation_id = data.get("conversation_id")

                if conversation_id is not None:
                    st.session_state.conversation_id = conversation_id

                sources = (
                    data.get("sources")
                    or data.get("citations")
                    or []
                )

                st.markdown(answer)

                if sources:

                    with st.expander("Sources"):

                        for source in sources:
                            st.write(f"• {source}")

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "sources": sources,
                    }
                )

            else:

                try:
                    error = response.json()["detail"]
                except Exception:
                    error = response.text

                st.error(error)