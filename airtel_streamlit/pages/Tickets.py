from utils.styles import load_css
import streamlit as st

from api import APIClient


st.set_page_config(
    page_title="Tickets",
    page_icon="🎫",
    layout="wide",
)

load_css()

if not st.session_state.get("logged_in"):
    st.warning("Please login first.")
    st.stop()


st.title("🎫 Ticket Management")

st.divider()

# ----------------------------
# Create Ticket
# ----------------------------

st.subheader("Create New Ticket")

with st.form("create_ticket"):

    title = st.text_input("Title")

    description = st.text_area("Description")

    priority = st.selectbox(
        "Priority",
        [
            "LOW",
            "MEDIUM",
            "HIGH",
        ],
    )

    submitted = st.form_submit_button(
        "Create Ticket"
    )

    if submitted:

        response = APIClient.create_ticket(
            {
                "title": title,
                "description": description,
                "priority": priority,
            }
        )

        if response.status_code == 201:

            st.success("Ticket Created Successfully")

            st.rerun()

        else:

            try:
                st.error(response.json()["detail"])
            except:
                st.error("Unable to create ticket.")


st.divider()

# ----------------------------
# Ticket List
# ----------------------------

st.subheader("My Tickets")

response = APIClient.get_my_tickets()

if response.status_code != 200:

    st.error("Unable to load tickets.")

    st.stop()

tickets = response.json()

if len(tickets) == 0:

    st.info("No Tickets Found.")

    st.stop()


for ticket in tickets:

    with st.expander(
        f"#{ticket['id']} - {ticket['title']}"
    ):

        st.write(f"**Status:** {ticket['status']}")
        st.write(f"**Priority:** {ticket['priority']}")
        st.write(ticket["description"])

        st.divider()

        col1, col2 = st.columns(2)

        # --------------------
        # Update Ticket
        # --------------------

        with col1:

            st.markdown("### Update")

            new_title = st.text_input(
                "Title",
                value=ticket["title"],
                key=f"title_{ticket['id']}",
            )

            new_description = st.text_area(
                "Description",
                value=ticket["description"],
                key=f"description_{ticket['id']}",
            )

            new_status = st.selectbox(
                "Status",
                [
                    "OPEN",
                    "IN_PROGRESS",
                    "CLOSED",
                ],
                index=[
                    "OPEN",
                    "IN_PROGRESS",
                    "CLOSED",
                ].index(ticket["status"]),
                key=f"status_{ticket['id']}",
            )

            if st.button(
                "Update",
                key=f"update_{ticket['id']}",
            ):

                update_response = APIClient.update_ticket(
                    ticket["id"],
                    {
                        "title": new_title,
                        "description": new_description,
                        "status": new_status,
                    },
                )

                if update_response.status_code == 200:

                    st.success("Ticket Updated")

                    st.rerun()

                else:

                    try:
                        st.error(
                            update_response.json()["detail"]
                        )
                    except:
                        st.error("Update failed.")

        # --------------------
        # Delete Ticket
        # --------------------

        with col2:

            st.markdown("### Delete")

            st.warning(
                "Deleting a ticket cannot be undone."
            )

            if st.button(
                "Delete Ticket",
                key=f"delete_{ticket['id']}",
            ):

                delete_response = APIClient.delete_ticket(
                    ticket["id"]
                )

                if delete_response.status_code == 200:

                    st.success("Ticket Deleted")

                    st.rerun()

                else:

                    try:
                        st.error(
                            delete_response.json()["detail"]
                        )
                    except:
                        st.error("Unable to delete ticket.")