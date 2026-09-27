import streamlit as st
from openai import OpenAI

# Read key securely from Streamlit secrets
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

# Set page title and layout
st.set_page_config(page_title="TaskTrack & AI Tutor", layout="centered")

# Store tasks in Streamlit Session State
if "homework_list" not in st.session_state:
    st.session_state.homework_list = []

st.title("📚 TaskTrack & AI Study Assistant")
st.write("Manage your homework assignments and get guided study hints!")

# Create tabs for the Web UI
tab1, tab2 = st.tabs(["📝 Homework Manager", "🤖 AI Tutor"])

# --- TAB 1: Homework Manager ---
with tab1:
    st.header("Add New Homework")

    with st.form("add_task_form", clear_on_submit=True):
        task_name = st.text_input("Assignment Name")
        due_date = st.date_input("Due Date")
        submit_button = st.form_submit_button("Add Task")

        if submit_button:
            if task_name:
                st.session_state.homework_list.append({
                    "title": task_name,
                    "due_date": str(due_date),
                    "completed": False
                })
                st.success(f"Added '{task_name}' to your list!")
            else:
                st.warning("Please enter an assignment name.")

    st.divider()
    st.header("Your Assignments")

    if not st.session_state.homework_list:
        st.info("No homework added yet!")
    else:
        for index, task in enumerate(st.session_state.homework_list):
            col1, col2 = st.columns([3, 1])
            status_text = "✅ Done" if task["completed"] else "⏳ Pending"
            col1.write(f"**{index + 1}. {task['title']}** (Due: {task['due_date']}) - *{status_text}*")

            if not task["completed"]:
                if col2.button("Mark Done", key=f"done_{index}"):
                    st.session_state.homework_list[index]["completed"] = True
                    st.rerun()

# --- TAB 2: AI Tutor ---
with tab2:
    st.header("🤖 Ask the Socratic AI Tutor")
    st.caption("The tutor provides hints and step-by-step guidance without giving direct answers.")

    user_question = st.text_area("What assignment or question do you need help with?")

    if st.button("Get AI Help"):
        if user_question:
            system_prompt = (
                "You are an encouraging Socratic tutor. "
                "Do NOT write direct essay drafts or solve math problems completely. "
                "Explain the core concept, provide hints, and guide the student step-by-step."
            )

            with st.spinner("AI is thinking..."):
                try:
                    response = client.chat.completions.create(
                        model="openrouter/auto",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_question}
                        ]
                    )
                    st.markdown("### AI Tutor Guidance")
                    st.info(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error connecting to AI: {e}")
        else:
            st.warning("Please type a question first.")