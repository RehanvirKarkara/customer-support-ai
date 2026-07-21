import streamlit as st

from api import APIClient


def initialize_session():

    defaults = {
        "logged_in": False,
        "token": None,
        "user": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def logout():

    st.session_state.logged_in = False
    st.session_state.token = None
    st.session_state.user = None

    st.rerun()


def login_page():

    initialize_session()

    st.title("📱 Airtel Customer Support AI")
    st.caption("AI Powered Customer Support Portal")

    login_tab, register_tab = st.tabs(
        ["Login", "Register"]
    )

    # --------------------------------------------------
    # LOGIN
    # --------------------------------------------------

    with login_tab:

        st.subheader("Login")

        email = st.text_input(
            "Email",
            key="login_email",
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password",
        )

        if st.button(
            "Login",
            use_container_width=True,
        ):

            if not email or not password:
                st.warning(
                    "Please enter email and password."
                )
                st.stop()

            with st.spinner("Logging in..."):

                try:

                    response = APIClient.login(
                        email,
                        password,
                    )

                    if response.status_code == 200:

                        token = response.json()

                        st.session_state.token = token["access_token"]
                        st.session_state.logged_in = True

                        me = APIClient.me()

                        if me.status_code == 200:
                            st.session_state.user = me.json()

                        st.success("Login Successful")

                        st.rerun()

                    else:

                        try:
                            detail = response.json()["detail"]
                        except Exception:
                            detail = response.text

                        st.error(detail)

                except Exception as e:
                    st.error(str(e))

    # --------------------------------------------------
    # REGISTER
    # --------------------------------------------------

    with register_tab:

        st.subheader("Create Account")

        customer_id = st.text_input(
            "Customer ID"
        )

        full_name = st.text_input(
            "Full Name"
        )

        email = st.text_input(
            "Email",
            key="register_email",
        )

        password = st.text_input(
            "Password",
            type="password",
            key="register_password",
        )

        mobile_number = st.text_input(
            "Mobile Number"
        )

        service_type = st.selectbox(
            "Service Type",
            [
                "PREPAID",
                "POSTPAID",
                "BROADBAND",
                "DTH",
                "AIRTEL_BLACK",
            ],
        )

        customer_type = st.selectbox(
            "Customer Type",
            [
                "REGULAR",
                "PREMIUM",
                "VIP",
            ],
        )

        preferred_language = st.text_input(
            "Preferred Language",
            value="English",
        )

        circle = st.text_input(
            "Circle"
        )

        if st.button(
            "Register",
            use_container_width=True,
        ):

            data = {
                "customer_id": customer_id,
                "full_name": full_name,
                "email": email,
                "password": password,
                "mobile_number": mobile_number,
                "service_type": service_type,
                "customer_type": customer_type,
                "preferred_language": preferred_language,
                "circle": circle,
            }

            with st.spinner("Creating account..."):

                try:

                    response = APIClient.register(
                        data
                    )

                    if response.status_code == 201:

                        st.success(
                            "Registration Successful! Please login."
                        )

                    else:

                        try:
                            detail = response.json()["detail"]
                        except Exception:
                            detail = response.text

                        st.error(detail)

                except Exception as e:
                    st.error(str(e))