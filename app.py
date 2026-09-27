import os
import streamlit as st
import openai

# Page Configuration
st.set_page_config(page_title="TaskTrack & AI Study Assistant", page_icon="📚", layout="centered")

# Clean White Aesthetic Styling
st.markdown("""
<style>
    /* Main Background - Clean Light / White */
    .stApp {
        background-color: #f8f9fa !important;
        color: #212529;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .block-container {
        padding-top: 2rem !important;
        max-width: 600px !important;
    }

    /* Titles & Headers */
    .app-title {
        color: #1a1a1a;
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .app-subtitle {
        color: #6c757d;
        font-size: 1rem;
        margin-bottom: 25px;
    }

    /* Input Card Container */
    .card {
        background: #ffffff;
        color: #212529;
        padding: 20px;
        border-radius: 12px;
        margin-top: 15px;
        border: 1px solid #e9ecef;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }

    /* Clean Styled Buttons */
    div.stButton > button {
        background-color: #ffffff !important;
        color: #333333 !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        border: 1px solid #ced4da !important;
        padding: 10px !important;
        width: 100% !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04) !important;
        transition: all 0.2s ease !important;
    }

    div.stButton > button:hover {
        background-color: #f1f3f5 !important;
        border-color: #adb5bd !important;
    }
</style>
""", unsafe_allow_html=True)

# Application Header
st.markdown("📚 <span class='app-title'>TaskTrack & AI Study Assistant</span>", unsafe_allow_html=True)
st.markdown("<p class='app-subtitle'>Manage your homework assignments and get guided study hints!</p>",
            unsafe_allow_html=True)

# Session State Initializations
if "active_tool" not in st.session_state:
    st.session_state.active_tool = "homework"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "reminders" not in st.session_state:
    st.session_state.reminders = []

# Top Tab Navigation
tab1, tab2 = st.tabs(["📝 Homework Manager", "🤖 AI Tutor"])

with tab1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Add New Homework")
    task_name = st.text_input("Assignment Name", placeholder="e.g., Math Exercises Chapter 4")
    due_date = st.date_input("Due Date")
    if st.button("Add Task"):
        if task_name:
            st.session_state.reminders.append({"name": task_name, "date": str(due_date)})
            st.success(f"Added '{task_name}' successfully!")

    if st.session_state.reminders:
        st.write("---")
        st.subheader("Your Homework List")
        for idx, task in enumerate(st.session_state.reminders, 1):
            st.write(f"**{idx}. {task['name']}** — Due: `{task['date']}`")
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Ask the Socratic AI Tutor")
    st.caption("The tutor provides hints and step-by-step guidance without giving direct answers.")

    user_query = st.text_area("What assignment or question do you need help with?",
                              placeholder="e.g., solve the math problem 2+11=?")

    if st.button("Get AI Help"):
        if user_query:
            api_key = st.secrets.get("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_API_KEY")
            if not api_key:
                st.error("API Key missing! Check your Streamlit Secrets.")
            else:
                with st.spinner("AI Tutor is thinking..."):
                    try:
                        client = openai.OpenAI(
                            base_url="https://openrouter.ai/api/v1",
                            api_key=api_key
                        )
                        response = client.chat.completions.create(
                            model="openrouter/auto",
                            messages=[
                                {"role": "system",
                                 "content": "You are a friendly Socratic tutor. Do NOT give direct answers or final solutions. Ask guiding questions, give hints, and break down steps."},
                                {"role": "user", "content": user_query}
                            ]
                        )
                        st.markdown("### AI Tutor Guidance")
                        st.info(response.choices[0].message.content)
                    except Exception as e:
                        st.error(f"Error connecting to AI: {e}")
        else:
            st.warning("Please type a question or problem first.")
    st.markdown("</div>", unsafe_allow_html=True)
