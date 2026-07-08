import streamlit as st
import requests

# Set up simple web layout
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you today?"}]

st.title("🗣️ Conversational Chatbot")
st.subheader("Simple Chat Interface for LLMs by Build Fast with AI")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if user_input := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Build conversation payload
                api_messages = [{"role": "system", "content": "You are a helpful AI assistant."}]
                for msg in st.session_state.messages:
                    api_messages.append({"role": msg["role"], "content": msg["content"]})
                
                # Fetch token cleanly
                api_key = st.secrets["TOGETHER_API_KEY"].strip().replace('"', '').replace("'", "")
                
                # Make standard network post request
                response = requests.post(
                    "https://openrouter.ai",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "meta-llama/llama-3.3-70b-instruct:free",
                        "messages": api_messages,
                        "temperature": 0.7
                    }
                )
                
                # Direct fail-proof text handler
                if response.status_code != 200:
                    st.error(f"OpenRouter Connection Error (Status {response.status_code}): {response.text}")
                else:
                    data = response.json()
                    response_content = data["choices"][0]["message"]["content"]
                    st.write(response_content)
                    st.session_state.messages.append({"role": "assistant", "content": response_content})
                    
            except Exception as error_msg:
                st.error(f"App processing error indicator: {error_msg}")
