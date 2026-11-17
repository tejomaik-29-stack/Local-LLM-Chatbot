
import streamlit as st
import requests
import time

st.title("🤖 My Local LLM Chatbot")
st.write("Powered by Ollama and Llama 3.2")

# Create chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

        if "time" in message:
            st.caption(f"Response time: {message['time']:.2f} seconds")

# Chat input
question = st.chat_input("Ask me anything...")

if question:
    # Save user's question
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    # Measure response time
    start_time = time.perf_counter()

    try:
        with st.spinner("AI is thinking..."):
            response = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": "llama3.2:1b",
                    "messages": st.session_state.messages,
                    "stream": False
                },
                timeout=120
            )

            response.raise_for_status()
            answer = response.json()["message"]["content"]

        end_time = time.perf_counter()
        response_time = end_time - start_time

    except requests.exceptions.RequestException as e:
        answer = f"Error connecting to Ollama: {e}"
        response_time = time.perf_counter() - start_time

    # Save AI response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "time": response_time
    })

    # Refresh the page
    st.rerun()

# Clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()
