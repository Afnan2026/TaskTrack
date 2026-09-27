import os
import sqlite3
import time
import streamlit as st
import openai

# Page Configuration
st.set_page_config(page_title="TaskTrack AI", page_icon="📚", layout="centered")


# --- DATABASE SETUP (SQLite Persistent Storage) ---
def init_db():
    conn = sqlite3.connect("tasktrack.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT,
            task TEXT,
            done INTEGER
        )
    ''')
    conn.commit()
    conn.close()


def get_user_tasks(email):
    conn = sqlite3.connect("tasktrack.db")
    c = conn.cursor()
    c.execute("SELECT id, task, done FROM user_reminders WHERE user_email = ?", (email,))
    rows = c.fetchall()
    conn.close()
    return [{"id": r[0], "task": r[1], "done": bool(r[2])} for r in rows]


def add_user_task(email, task_text):
    conn = sqlite3.connect("tasktrack.db")
    c = conn.cursor()
    c.execute("INSERT INTO user_reminders (user_email, task, done) VALUES (?, ?, 0)", (email, task_text))
    conn.commit()
    conn.close()


def delete_user_task(task_id):
    conn = sqlite3.connect("tasktrack.db")
    c = conn.cursor()
    c.execute("DELETE FROM user_reminders WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()


def update_task_status(task_id, done):
    conn = sqlite3.connect("tasktrack.db")
    c = conn.cursor()
    c.execute("UPDATE user_reminders SET done = ? WHERE id = ?", (1 if done else 0, task_id))
    conn.commit()
    conn.close()


init_db()

# Custom Styling
st.markdown("""
<style>
    .stApp {
        background-color: #eef1f5 !important;
        color: #222222;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .block-container {
        padding-top: 1.5rem !important;
        max-width: 500px !important;
    }
    .app-title {
        text-align: center;
        color: #111111;
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0px;
    }
    .app-subtitle {
        text-align: center;
        color: #555555;
        font-size: 1.05rem;
        font-weight: 500;
        margin-bottom: 20px;
    }
    div.stButton > button {
        background: linear-gradient(180deg, #ffb700 0%, #e6a100 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        border-radius: 12px !important;
        border: 1px solid #cc8f00 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
        padding: 16px 10px !important;
        width: 100% !important;
    }
    .card {
        background: #ffffff;
        color: #222222;
        padding: 20px;
        border-radius: 12px;
        margin-top: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid #e1e5eb;
    }
</style>
""", unsafe_allow_html=True)

# --- SIMPLE DIRECT LOGIN GATE (NO GOOGLE HASSLE) ---
if "user_email" not in st.session_state:
    st.session_state.user_email = None

if not st.session_state.user_email:
    st.markdown("<div style='text-align: center; font-size: 55px;'>⬛🔲</div>", unsafe_allow_html=True)
    st.markdown("<h1 class='app-title'>TaskTrack AI</h1>", unsafe_allow_html=True)
    st.markdown("<p class='app-subtitle'>Enter your name to access your assignments & tools</p>",
                unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Welcome! 👋")

    name_input = st.text_input("Your Name:", placeholder="e.g. Afnan")
    email_input = st.text_input("Your Email:", placeholder="e.g. afnan@gmail.com")

    if st.button("🚀 Enter TaskTrack"):
        if name_input and email_input:
            st.session_state.user_name = name_input
            st.session_state.user_email = email_input
            st.rerun()
        else:
            st.warning("Please fill in both fields to continue.")

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- MAIN DASHBOARD (LOGGED IN USER) ---
user_email = st.session_state.user_email
user_name = st.session_state.get("user_name", "Student")

st.markdown("<div style='text-align: center; font-size: 50px;'>⬛🔲</div>", unsafe_allow_html=True)
st.markdown("<h1 class='app-title'>TaskTrack</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='app-subtitle'>Welcome, {user_name}! | Let us help you solve your homework</p>",
            unsafe_allow_html=True)

col_usr, col_logout = st.columns([3, 1])
with col_usr:
    st.caption(f"Logged in as: `{user_email}`")
with col_logout:
    if st.button("Log out"):
        st.session_state.user_email = None
        st.rerun()

if "active_tool" not in st.session_state:
    st.session_state.active_tool = None


# Socratic AI Helper
def query_smarter_ai(prompt_text):
    api_key = st.secrets.get("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        st.error("API Key missing! Please configure secrets in Streamlit Cloud.")
        return
    with st.spinner("🧠 Smart Socratic AI is breaking down your question..."):
        try:
            client = openai.OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
            response = client.chat.completions.create(
                model="openrouter/auto",
                messages=[
                    {"role": "system",
                     "content": "You are an elite Socratic Tutor. Never state direct solutions directly. Break the problem down step-by-step and ask 1-2 guiding questions."},
                    {"role": "user", "content": prompt_text}
                ]
            )
            st.markdown("### 🎓 Socratic Guidance")
            st.info(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Error reaching AI service: {e}")


st.write("**TaskTrack AI:**")
col_search, col_btn = st.columns([3, 1])
with col_search:
    user_query = st.text_input("Ask me anything", placeholder="Ask any homework question...",
                               label_visibility="collapsed")
with col_btn:
    if st.button("🔍 search"):
        if user_query:
            st.session_state.active_tool = "ai_search"

st.markdown("<br>", unsafe_allow_html=True)

# 2x2 Tool Grid
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
    if st.button("🧠 AI Tutor"):
        st.session_state.active_tool = "ai_search"

st.markdown("<br>", unsafe_allow_html=True)

# Active Tool Panes
if st.session_state.active_tool == "ai_search":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🤖 Smart Socratic AI Tutor")
    if user_query:
        query_smarter_ai(user_query)
    else:
        q_input = st.text_area("Type your question here:", placeholder="e.g. How do I solve x^2 - 4 = 0?")
        if st.button("Get Socratic Hints"):
            if q_input:
                query_smarter_ai(q_input)
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.active_tool == "camera":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📷 Homework Camera Scanner")
    img_file = st.camera_input("Capture picture")
    if img_file is not None:
        st.image(img_file, caption="Captured Homework Image", use_column_width=True)
        notes = st.text_input("Add details about what you need help with:")
        if st.button("Analyze Question"):
            query_smarter_ai(f"Homework photo context: {notes if notes else 'Explain how to solve this step by step.'}")
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.active_tool == "alarm":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("⏰ Study Alarm & Timer")
    timer_seconds = st.number_input("Set Timer Duration (Seconds):", min_value=5, max_value=3600, value=10, step=5)
    if st.button("Start Timer"):
        st.warning(f"Timer running for {timer_seconds} seconds!")
        progress_bar = st.progress(0)
        timer_text = st.empty()
        for i in range(timer_seconds, 0, -1):
            timer_text.markdown(f"### ⏳ Time Remaining: `{i}` seconds")
            progress_bar.progress((timer_seconds - i + 1) / timer_seconds)
            time.sleep(1)
        timer_text.markdown("### 🔔 Time's Up!")
        st.balloons()
        st.audio("https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg", autoplay=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.active_tool == "reminder":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📌 Saved Assignments & Reminders")

    col_in, col_add = st.columns([3, 1])
    with col_in:
        new_task = st.text_input("New Task", label_visibility="collapsed", placeholder="Enter assignment...")
    with col_add:
        if st.button("Add"):
            if new_task:
                add_user_task(user_email, new_task)
                st.rerun()

    st.write("---")
    st.write("### Your Saved Tasks (Database Synced):")

    saved_tasks = get_user_tasks(user_email)
    if not saved_tasks:
        st.info("No reminders saved yet! Add one above.")
    else:
        for t in saved_tasks:
            c1, c2 = st.columns([4, 1])
            with c1:
                is_done = st.checkbox(t["task"], value=t["done"], key=f"db_chk_{t['id']}")
                if is_done != t["done"]:
                    update_task_status(t["id"], is_done)
                    st.rerun()
            with c2:
                if st.button("🗑️", key=f"db_del_{t['id']}"):
                    delete_user_task(t["id"])
                    st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
