import streamlit as st
import ollama


# Page configuration
st.set_page_config(
    page_title="Local AI Chatbot",
    page_icon="🤖",
    layout="centered"
)


# Title
st.title("🤖 Local AI Chatbot")
st.write("Powered by Qwen3:4b and Ollama")


# Custom instructions
system_instruction = st.text_area(
    "Custom AI Instructions",
    value="You are a helpful AI assistant. Answer clearly and in simple English.",
    height=100
)


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": system_instruction
        }
    ]


# Update system instruction
st.session_state.messages[0]["content"] = system_instruction


# Display previous messages
for message in st.session_state.messages:

    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# User input
user_prompt = st.chat_input("Type your message here...")


if user_prompt:

    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("Qwen3 is thinking..."):

            try:

                response = ollama.chat(
                    model="qwen3:4b",
                    messages=st.session_state.messages
                )

                assistant_response = response["message"]["content"]

                st.markdown(assistant_response)

                # Save AI response
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": assistant_response
                    }
                )

            except Exception as e:

                st.error("Unable to connect to Ollama.")

                st.code(str(e))