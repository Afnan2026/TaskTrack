import os
import streamlit as st
import openai

# Page Configuration
st.set_page_config(page_title="TaskTrack AI", page_icon="📚", layout="centered")

# App Lab Red & Yellow Custom Styling
st.markdown("""
<style>
    /* Main Background - Vibrant Red Gradient */
    .stApp {
        background: linear-gradient(135deg, #e52d27 0%, #b31217 100%) !important;
        color: white;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Hide top header padding */
    .block-container {
        padding-top: 2rem !important;
        max-width: 500px !important;
    }

    /* Title & Headers */
    .app-title {
        text-align: center;
        color: #ffffff;
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    .app-subtitle {
        text-align: center;
        color: #fff8e7;
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 25px;
    }

    /* Custom Input Fields */
    div[data-baseweb="input"] {
        background-color: #ffffff !important;
        border-radius: 8px !important;
        border: 2px solid #ffcc00 !important;
    }

    /* Yellow Buttons Styled like App Lab */
    div.stButton > button {
        background: linear-gradient(180deg, #ffdd00 0%, #ffbb00 100%) !important;
        color: #333333 !important;
        font-weight: bold !important;
        font-size: 1rem !important;
        border-radius: 10px !important;
        border: 2px solid #d4a000 !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2) !important;
        padding: 12px 10px !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
    }

    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 10px rgba(0,0,0,0.3) !important;
        background: #ffe033 !important;
    }

    /* Cards for Popup Content */
    .card {
        background: rgba(255, 255, 255, 0.95);
        color: #222222;
        padding: 20px;
        border-radius: 12px;
        margin-top: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# Application Header Icon & Title
st.markdown("<div style='text-align: center; font-size: 50px;'>🟦🟥</div>", unsafe_allow_html=True)
st.markdown("<h1 class='app-title'>TaskTrack</h1>", unsafe_allow_html=True)
st.markdown("<p class='app-subtitle'>Let us help to solve your homework</p>", unsafe_allow_html=True)

# Session State Initializations
if "active_tool" not in st.session_state:
    st.session_state.active_tool = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "reminders" not in st.session_state:
    st.session_state.reminders = ["Math Chapter 4 Exercises", "History Essay Outline"]

# Search Bar Section
st.markdown("### TaskTrack AI")
col_search, col_btn = st.columns([3, 1])
with col_search:
    user_query = st.text_input("Ask me anything", placeholder="Ask me anything...", label_visibility="collapsed")
with col_btn:
    if st.button("Search"):
        if user_query:
            st.session_state.active_tool = "ai_search"
        else:
            st.warning("Please type a question first.")

st.markdown("<br>", unsafe_allow_html=True)

# 2x2 Grid Buttons (Camera, Alarm, Reminder, Photo)
row1_col1, row1_col2 = st.columns(2)
with row1_col1:
    if st.button("📷 Camera"):
        st.session_state.active_tool = "camera"
with row1_col2:
    if st.button("⏰ Alarm"):
        st.session_state.active_tool = "alarm"

row2_col1, row2_col2 = st.columns(2)
with row2_col1:
    if st.button("📌 Reminder"):
        st.session_state.active_tool = "reminder"
with row2_col2:
    if st.button("🖼️ Photo"):
        st.session_state.active_tool = "photo"

st.markdown("<br>", unsafe_allow_html=True)

# Bottom Navigation Bar (Settings, Logout, Login, About)
nav1, nav2, nav3, nav4 = st.columns(4)
with nav1:
    if st.button("Settings"):
        st.session_state.active_tool = "settings"
with nav2:
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.success("Logged out successfully!")
with nav3:
    if st.button("Log in"):
        st.session_state.active_tool = "login"
with nav4:
    if st.button("About"):
        st.session_state.active_tool = "about"

# --- TOOL CONTENT DISPLAY PANELS ---

# 1. AI Search Tool
if st.session_state.active_tool == "ai_search":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🤖 Socratic AI Tutor Guidance")

    api_key = st.secrets.get("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        st.error("API Key not found! Please check your secrets.toml.")
    else:
        with st.spinner("AI Tutor is formulating hints..."):
            try:
                client = openai.OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=api_key
                )
                response = client.chat.completions.create(
                    model="openrouter/auto",
                    messages=[
                        {"role": "system",
                         "content": "You are a friendly Socratic homework tutor. Do NOT give direct answers or solve math problems completely. Ask guiding questions, give hints, and explain core concepts."},
                        {"role": "user", "content": user_query}
                    ]
                )
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Error connecting to AI: {e}")
    st.markdown("</div>", unsafe_allow_html=True)

# 2. Camera Tool
elif st.session_state.active_tool == "camera":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📷 Camera Homework Scanner")
    picture = st.camera_input("Take a photo of your assignment")
    if picture:
        st.image(picture, caption="Scanned Homework")
        st.success("Homework picture captured! Ready for review.")
    st.markdown("</div>", unsafe_allow_html=True)

# 3. Alarm / Study Timer Tool
elif st.session_state.active_tool == "alarm":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("⏰ Pomodoro Study Timer")
    timer_minutes = st.number_input("Set Study Timer (Minutes):", min_value=1, max_value=120, value=25)
    if st.button("Start Timer"):
        st.info(f"Timer set for {timer_minutes} minutes! Focus time starts now.")
    st.markdown("</div>", unsafe_allow_html=True)

# 4. Reminder Tool
elif st.session_state.active_tool == "reminder":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📌 Task Reminders")
    new_task = st.text_input("Add new reminder:")
    if st.button("Add Task"):
        if new_task:
            st.session_state.reminders.append(new_task)
            st.success(f"Added: {new_task}")

    st.write("### Your Current Tasks:")
    for idx, task in enumerate(st.session_state.reminders, 1):
        st.write(f"{idx}. {task}")
    st.markdown("</div>", unsafe_allow_html=True)

# 5. Photo Tool
elif st.session_state.active_tool == "photo":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🖼️ Upload Homework Photo")
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Homework Image")
        st.success("File uploaded successfully!")
    st.markdown("</div>", unsafe_allow_html=True)

# 6. Settings Tool
elif st.session_state.active_tool == "settings":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("⚙️ App Settings")
    st.write("Configure your TaskTrack preferences.")
    st.selectbox("Theme Preference", ["Red & Yellow (Default)", "Dark Mode", "Light Mode"])
    st.checkbox("Enable Push Notifications")
    st.markdown("</div>", unsafe_allow_html=True)

# 7. Login Tool
elif st.session_state.active_tool == "login":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🔑 User Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Submit Login"):
        if username:
            st.session_state.logged_in = True
            st.success(f"Welcome back, {username}!")
    st.markdown("</div>", unsafe_allow_html=True)

# 8. About Tool
elif st.session_state.active_tool == "about":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("ℹ️ About TaskTrack")
    st.write("TaskTrack is a Socratic AI homework assistant and task manager created with Python & Streamlit.")
    st.write("Designed for high school and college students to get guidance without direct answers.")
    st.markdown("</div>", unsafe_allow_html=True)
