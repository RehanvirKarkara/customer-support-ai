import streamlit as st


def load_css():
    st.markdown(
        """
<style>

/* -----------------------------
   Google Font
------------------------------*/

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* -----------------------------
   Main App
------------------------------*/

.stApp{
    background:#f8fafc;
}

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
    padding-left:2.5rem;
    padding-right:2.5rem;
}

/* -----------------------------
   Sidebar
------------------------------*/

section[data-testid="stSidebar"]{
    background:#ffffff;
    border-right:1px solid #e5e7eb;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3{
    color:#111827;
}

section[data-testid="stSidebar"] hr{
    margin-top:10px;
    margin-bottom:10px;
}

/* -----------------------------
   Headers
------------------------------*/

h1{
    font-size:2.2rem !important;
    font-weight:700 !important;
    color:#111827;
}

h2{
    font-weight:700;
    color:#111827;
}

h3{
    font-weight:600;
    color:#374151;
}

/* -----------------------------
   Buttons
------------------------------*/

.stButton > button{

    background:#e60000;
    color:white;

    border:none;

    border-radius:12px;

    height:48px;

    width:100%;

    font-weight:600;

    transition:0.25s;

}

.stButton > button:hover{

    background:#c70000;

    transform:translateY(-1px);

}

/* -----------------------------
   Inputs
------------------------------*/

.stTextInput input,
.stTextArea textarea{

    border-radius:12px;

    border:1px solid #d1d5db;

}

.stSelectbox div[data-baseweb="select"]{

    border-radius:12px;

}

/* -----------------------------
   Cards / Metrics
------------------------------*/

div[data-testid="metric-container"]{

    background:white;

    border-radius:16px;

    padding:20px;

    border:1px solid #ececec;

    box-shadow:
    0 4px 18px rgba(0,0,0,.05);

}

/* -----------------------------
   Chat
------------------------------*/

[data-testid="stChatMessage"]{

    border-radius:18px;

    padding:12px;

    background:white;

    margin-bottom:10px;

    border:1px solid #ececec;

}

/* -----------------------------
   Tables
------------------------------*/

thead tr th{

    background:#f3f4f6 !important;

}

tbody tr:hover{

    background:#fafafa;

}

/* -----------------------------
   Expanders
------------------------------*/

.streamlit-expanderHeader{

    font-weight:600;

}

/* -----------------------------
   Alerts
------------------------------*/

.stAlert{

    border-radius:14px;

}

/* -----------------------------
   Scrollbar
------------------------------*/

::-webkit-scrollbar{

    width:8px;

}

::-webkit-scrollbar-thumb{

    background:#d1d5db;

    border-radius:20px;

}

::-webkit-scrollbar-thumb:hover{

    background:#9ca3af;

}

</style>
""",
        unsafe_allow_html=True,
    )