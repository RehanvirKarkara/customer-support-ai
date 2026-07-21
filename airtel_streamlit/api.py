import requests
import streamlit as st

from config import API_BASE_URL, REQUEST_TIMEOUT


class APIClient:

    @staticmethod
    def _headers():
        token = st.session_state.get("token")

        headers = {}

        if token:
            headers["Authorization"] = f"Bearer {token}"

        return headers

    # -------------------------
    # AUTH
    # -------------------------

    @staticmethod
    def register(data):

        return requests.post(
            f"{API_BASE_URL}/auth/register",
            json=data,
            timeout=REQUEST_TIMEOUT,
        )

    @staticmethod
    def login(email, password):

        return requests.post(
            f"{API_BASE_URL}/auth/login",
            json={
                "email": email,
                "password": password,
            },
            timeout=REQUEST_TIMEOUT,
        )

    @staticmethod
    def me():

        return requests.get(
            f"{API_BASE_URL}/auth/me",
            headers=APIClient._headers(),
            timeout=REQUEST_TIMEOUT,
        )

    # -------------------------
    # TICKETS
    # -------------------------

    @staticmethod
    def get_my_tickets():

        return requests.get(
            f"{API_BASE_URL}/tickets/me",
            headers=APIClient._headers(),
            timeout=REQUEST_TIMEOUT,
        )

    @staticmethod
    def create_ticket(data):

        return requests.post(
            f"{API_BASE_URL}/tickets/",
            json=data,
            headers=APIClient._headers(),
            timeout=REQUEST_TIMEOUT,
        )

    @staticmethod
    def update_ticket(ticket_id, data):

        return requests.put(
            f"{API_BASE_URL}/tickets/{ticket_id}",
            json=data,
            headers=APIClient._headers(),
            timeout=REQUEST_TIMEOUT,
        )

    @staticmethod
    def delete_ticket(ticket_id):

        return requests.delete(
            f"{API_BASE_URL}/tickets/{ticket_id}",
            headers=APIClient._headers(),
            timeout=REQUEST_TIMEOUT,
        )

    # -------------------------
    # KNOWLEDGE
    # -------------------------

    @staticmethod
    def upload_pdf(file):

        files = {
            "file": (
                file.name,
                file.getvalue(),
                "application/pdf",
            )
        }

        return requests.post(
            f"{API_BASE_URL}/knowledge/upload",
            files=files,
            headers=APIClient._headers(),
            timeout=REQUEST_TIMEOUT,
        )

    @staticmethod
    def get_documents():

        return requests.get(
            f"{API_BASE_URL}/knowledge/",
            headers=APIClient._headers(),
            timeout=REQUEST_TIMEOUT,
        )

    @staticmethod
    def delete_document(document_id):

        return requests.delete(
            f"{API_BASE_URL}/knowledge/{document_id}",
            headers=APIClient._headers(),
            timeout=REQUEST_TIMEOUT,
        )

    # -------------------------
    # CHAT
    # -------------------------

    @staticmethod
    def chat(question, conversation_id=None):

        payload = {
            "question": question,
        }

        if conversation_id:
            payload["conversation_id"] = conversation_id

        return requests.post(
            f"{API_BASE_URL}/chat/",
            json=payload,
            headers=APIClient._headers(),
            timeout=REQUEST_TIMEOUT,
        )

    @staticmethod
    def get_conversations():

        return requests.get(
            f"{API_BASE_URL}/conversations/",
            headers=APIClient._headers(),
            timeout=REQUEST_TIMEOUT,
        )

    @staticmethod
    def get_messages(conversation_id):

        return requests.get(
            f"{API_BASE_URL}/conversations/{conversation_id}",
            headers=APIClient._headers(),
            timeout=REQUEST_TIMEOUT,
        )
        
    '''
    @staticmethod
    def get_documents():

        return requests.get(
            f"{API_BASE_URL}/knowledge/",
            headers=APIClient._headers(),
            timeout=REQUEST_TIMEOUT,
        )
    '''