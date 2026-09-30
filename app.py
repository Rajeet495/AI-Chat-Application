import streamlit as st
from groq import Groq


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="AI Chat Application",
    page_icon="🤖",
    layout="centered"
)


# -----------------------------
# Title
# -----------------------------

st.title("🤖 AI Chat Application")
st.caption("Powered by an LLM API")


# -----------------------------
# API Client
# -----------------------------

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("GROQ_API_KEY is not configured.")
    st.stop()


# -----------------------------
# Custom Instructions
# -----------------------------

system_instruction = st.text_area(
    "Custom AI Instructions",
    value="You are a helpful AI assistant. Answer clearly and in simple English.",
    height=100
)


# -----------------------------
# Initialize Chat History
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": system_instruction
        }
    ]

# Keep the system instruction updated
st.session_state.messages[0]["content"] = system_instruction


# -----------------------------
# Display Conversation
# -----------------------------

for message in st.session_state.messages:

    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# -----------------------------
# User Input
# -----------------------------

user_prompt = st.chat_input("Type your message here...")


if user_prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):

        with st.spinner("AI is thinking..."):

            try:

                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=st.session_state.messages,
                    temperature=0.7,
                    max_tokens=500
                )

                assistant_response = response.choices[0].message.content

                st.markdown(assistant_response)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": assistant_response
                    }
                )

            except Exception as e:

                st.error("Something went wrong while generating the response.")

                st.caption(f"Error details: {e}")