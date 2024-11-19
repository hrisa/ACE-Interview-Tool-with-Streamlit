from openai import OpenAI
import streamlit as st

st.set_page_config(page_title="Streamlit Chat", page_icon="💬")
st.title("Chatbot")

st.subheader('Personal information', divider='rainbow')

name = st.text_input(label = "Name", value="", max_chars=None, placeholder="Enter your name")

experience = st.text_area(label = "Expirience", value="", height=None, max_chars=None, placeholder="Describe your experience")

skills = st.text_area(label = "Skills", value="", height=None, max_chars=None, placeholder="List your skills")

st.write(f"Your information: {name} {experience} {skills}")

st.subheader('Company and Position', divider='rainbow')

col1, col2 = st.columns(2)
with col1:
    level = st.radio(
    "Choose level",
    key="visibility",
    options=["Junior", "Mid-level", "Senior"],
    )

with col2:
    position = st.selectbox(
    "Choose a position",
    ("Data Scientist", "Data engineer", "ML Engineer", "BI Analyst", "Financial Analyst"))

company = st.selectbox(
    "Select a Company",
    ("Amazon", "Meta", "Udemy", "365 Company", "Nestle", "LinkedIn", "Spotify"))

st.write(f"Your information: {level} | {position} | {company}")

 # We start the interview here



client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": f"You are an HR executive that interviews an interviewee called {name} with expirience {experience} and skills {skills}. You should interview him for the position {level} {position} at the company {company}"}]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    

if prompt := st.chat_input("What is up?"):
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