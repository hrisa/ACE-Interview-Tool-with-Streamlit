import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="StreamlitChatMessageHistory", page_icon="💬")
st.title("Chatbot")

# Initialize session state for setup and interview phases
if "setup_complete" not in st.session_state:
    st.session_state.setup_complete = False

# Function to toggle setup phase completion
def complete_setup():
    st.session_state.setup_complete = True

# Show setup form if setup is not complete
if not st.session_state.setup_complete:
    st.subheader('Personal Information')

    # Initialize session state for personal information
    if "name" not in st.session_state:
        st.session_state["name"] = ""
    if "experience" not in st.session_state:
        st.session_state["experience"] = ""
    if "skills" not in st.session_state:
        st.session_state["skills"] = ""

    # Get personal information input
    st.session_state["name"] = st.text_input(label="Name", value=st.session_state["name"], placeholder="Enter your name")
    st.session_state["experience"] = st.text_area(label="Experience", value=st.session_state["experience"], placeholder="Describe your experience")
    st.session_state["skills"] = st.text_area(label="Skills", value=st.session_state["skills"], placeholder="List your skills")

    st.write(f"Your information: {st.session_state['name']} {st.session_state['experience']} {st.session_state['skills']}")

    st.subheader('Company and Position', divider='rainbow')

    # Initialize session state for company and position information
    if "level" not in st.session_state:
        st.session_state["level"] = "Junior"
    if "position" not in st.session_state:
        st.session_state["position"] = "Data Scientist"
    if "company" not in st.session_state:
        st.session_state["company"] = "Amazon"

    col1, col2 = st.columns(2)
    with col1:
        st.session_state["level"] = st.radio(
            "Choose level",
            key="visibility",
            options=["Junior", "Mid-level", "Senior"],
            index=["Junior", "Mid-level", "Senior"].index(st.session_state["level"])
        )

    with col2:
        st.session_state["position"] = st.selectbox(
            "Choose a position",
            ("Data Scientist", "Data Engineer", "ML Engineer", "BI Analyst", "Financial Analyst"),
            index=("Data Scientist", "Data Engineer", "ML Engineer", "BI Analyst", "Financial Analyst").index(st.session_state["position"])
        )

    st.session_state["company"] = st.selectbox(
        "Select a Company",
        ("Amazon", "Meta", "Udemy", "365 Company", "Nestle", "LinkedIn", "Spotify"),
        index=("Amazon", "Meta", "Udemy", "365 Company", "Nestle", "LinkedIn", "Spotify").index(st.session_state["company"])
    )

    st.write(f"Your information: {st.session_state['level']} | {st.session_state['position']} | {st.session_state['company']}")

    # Button to complete setup
    if st.button("Start Interview", on_click=complete_setup):
        st.write("Setup complete. Starting interview...")

# Show interview phase if setup is complete
if st.session_state.setup_complete:

    st.info(
    """
    Start by introducing yourself
    """,
    icon="👋",
    )

    # Initialize OpenAI client
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    # Initialize session state for OpenAI model and messages
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o"

    if "messages" not in st.session_state:
        st.session_state.messages = [{
            "role": "system",
            "content": (f"You are an HR executive that interviews an interviewee called {st.session_state['name']} "
                        f"with experience {st.session_state['experience']} and skills {st.session_state['skills']}. "
                        f"You should interview him for the position {st.session_state['level']} {st.session_state['position']} "
                        f"at the company {st.session_state['company']}")
        }]

    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Handle user input and OpenAI response
    if prompt := st.chat_input("Your response"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
