import streamlit as st
import requests

# Initialize session state for UI message tracking
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you today?"}
    ]

# Create user interface
st.title("🗣️ Conversational Chatbot")
st.subheader("Simple Chat Interface for LLMs by Build Fast with AI")

# Display chat messages on screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if user_input := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.write(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                api_messages = [
                    {"role": "system", "content": "You are a helpful AI assistant. Have a natural conversation with the user."}
                ]
                
                for msg in st.session_state.messages[:-1]:
                    api_messages.append({"role": msg["role"], "content": msg["content"]})
                
                api_messages.append({"role": "user", "content": user_input})
                
                headers = {
                    "Authorization": f"Bearer {st.secrets['TOGETHER_API_KEY']}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://localhost:8501",
                    "X-Title": "Build Fast Chatbot"
                }
                
                payload = {
                    "model": "meta-llama/llama-3.3-70b-instruct:free",
                    "messages": api_messages,
                    "temperature": 0.7
                }
                
                response = requests.post(
                    "https://openrouter.ai",
                    headers=headers,
                    json=payload
                )
                
                # Check for standard server response issues immediately
                if response.status_code != 200:
                    st.error(f"Server sent error code {response.status_code}. Raw content: {response.text}")
                else:
                    response_json = response.json()
                    if "choices" in response_json:
                        response_content = response_json["choices"][0]["message"]["content"]
                        st.write(response_content)
                        st.session_state.messages.append({"role": "assistant", "content": response_content})
                    else:
                        st.error(f"Unexpected response data format: {response_json}")
                
            except Exception as e:
                st.error(f"Execution Error: {e}")
