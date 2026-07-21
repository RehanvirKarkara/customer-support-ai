import streamlit as st


def section_header(title, emoji="📌"):

    st.markdown(f"## {emoji} {title}")


def empty_state(message):

    st.info(message)


def page_title(title, subtitle=None):

    st.title(title)

    if subtitle:
        st.caption(subtitle)


def metric_row(metrics):

    cols = st.columns(len(metrics))

    for col, metric in zip(cols, metrics):

        with col:

            st.metric(
                metric["label"],
                metric["value"],
            )