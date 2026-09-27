import os
import streamlit as st
import openai

# Page Configuration
st.set_page_config(page_title="TaskTrack AI", page_icon="📚", layout="centered")

# Light Gray App Lab Custom Styling
st.markdown("""
<style>
    /* Main Background - Light Gray */
    .stApp {
        background-color: #d9d9d9 !important;
        color: #222222;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .block-container {
        padding-top: 1.5rem !important;
        max-width: 480px !important;
    }

    /* Header & Titles */
    .app-title {
        text-align: center;
        color: #1a1a1a;
        font-size: 2.6rem;
        font-weight: 800;
        margin-bottom: 0px;
    }

    .app-subtitle {
        text-align: center;
        color: #333333;
        font-size: 1rem;
        font-weight: 500;
        margin-bottom: 20px;
    }

    /* Inputs */
    div[data-baseweb="input"] {
        background-color: #ffffff !important;
        border-radius: 6px !important;
        border: 1px solid #999999 !important;
    }

    /* App Lab Yellow Buttons */
    div.stButton > button {
        background: linear-gradient(180deg, #ffae00 0%, #e69d00 100%) !important;
        color: #ffffff !important;
        font-weight: bold !important;
        font-size: 0.95rem !important;
        border-radius: 8px !important;
        border: 1px solid #cc8b00 !important;
        box-shadow: 0 3px 5px rgba(0,0,0,0.2) !important;
        padding: 10px 5px !important;
        width: 100% !important;
    }

    div.stButton > button:hover {
        background: #ffb81a !important;
        color: #ffffff !important;
    }

    /* Content Cards */
    .card {
        background: #ffffff;
        color: #222222;
        padding: 18px;
        border-radius: 10px;
        margin-top: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Application Header Icon & Title
st.markdown("<div style='text-align: center; font-size: 45px; margin-bottom: -10px;'>⬛🔲</div>", unsafe_allow_html=True)
st.markdown("<h1 class='app-title'>TaskTrack</h1>", unsafe_allow_html=True)
st.markdown("<p class='app-subtitle'>Let us help to solve your homework</p>", unsafe_allow_html=True)

if "active_tool" not in st.session_state:
    st.session_state.active_tool = None
if "reminders" not in st.session_state:
    st.session_state.reminders = ["Math Exercises Ch. 4", "History Project"]

# Search Bar Section
st.write("**TaskTrack AI:**")
col_search, col_btn = st.columns([3, 1])
with col_search:
    user_query = st.text_input("Ask me anything", placeholder="Ask me anything", label_visibility="collapsed")
with col_btn:
    if st.button("search"):
        if user_query:
            st.session_state.active_tool = "ai_search"

st.markdown("<br>", unsafe_allow_html=True)

# 2x2 Grid Buttons
row1_col1, row1_col2 = st.columns(2)
with row1_col1:
    if st.button("Camera"):
        st.session_state.active_tool = "camera"
with row1_col2:
    if st.button("Alarm"):
        st.session_state.active_tool = "alarm"

row2_col1, row2_col2 = st.columns(2)
with row2_col1:
    if st.button("Reminder"):
        st.session_state.active_tool = "reminder"
with row2_col2:
    if st.button("Photo"):
        st.session_state.active_tool = "photo"

st.markdown("<br>", unsafe_allow_html=True)

# Bottom Nav Bar
nav1, nav2, nav3, nav4 = st.columns(4)
with nav1:
    if st.button("Settings"):
        st.session_state.active_tool = "settings"
with nav2:
    if st.button("Log out"):
        st.success("Logged out")
with nav3:
    if st.button("Log in"):
        st.session_state.active_tool = "login"
with nav4:
    if st.button("About"):
        st.session_state.active_tool = "about"

# Display Panels
if st.session_state.active_tool == "ai_search":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🤖 Socratic AI Tutor")
    api_key = st.secrets.get("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        st.error("API Key missing in Secrets.")
    else:
        with st.spinner("AI Tutor is thinking..."):
            try:
                client = openai.OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
                response = client.chat.completions.create(
                    model="openrouter/auto",
                    messages=[
                        {"role": "system",
                         "content": "You are a friendly Socratic tutor. Give hints without direct answers."},
                        {"role": "user", "content": user_query}
                    ]
                )
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {e}")
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.active_tool == "camera":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.camera_input("Take a photo of your homework")
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.active_tool == "alarm":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.number_input("Study Timer (Minutes):", value=25)
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.active_tool == "reminder":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📌 Reminders")
    new_t = st.text_input("Add task:")
    if st.button("Add"):
        st.session_state.reminders.append(new_t)
    for r in st.session_state.reminders:
        st.write(f"- {r}")
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.active_tool == "photo":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.file_uploader("Upload assignment image")
    st.markdown("</div>", unsafe_allow_html=True)
