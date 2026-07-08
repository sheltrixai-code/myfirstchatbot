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
                # Build context stack safely
                api_messages = [{"role": "system", "content": "You are a helpful AI assistant."}]
                for msg in st.session_state.messages:
                    api_messages.append({"role": msg["role"], "content": msg["content"]})
                
                # Fetch key cleanly and verify spacing strips
                api_key = st.secrets["TOGETHER_API_KEY"].strip().replace('"', '').replace("'", "")
                
                # Setup official validation headers requested by OpenRouter
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://streamlit.app", # Fixed security gateway bypass route
                    "X-Title": "Build Fast AI Chatbot App"
                }
                
                payload = {
                    "model": "meta-llama/llama-3.3-70b-instruct:free",
                    "messages": api_messages,
                    "temperature": 0.7
                }
                
                # Execute direct post call
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload
                )
                
                # Explicit error block scanner
                if response.status_code != 200:
                    st.error(f"OpenRouter Gateway Refusal (Status {response.status_code}): {response.text}")
                else:
                    data = response.json()
                    if "choices" in data:
                        response_content = data["choices"][0]["message"]["content"]
                        st.write(response_content)
                        st.session_state.messages.append({"role": "assistant", "content": response_content})
                    else:
                        st.error(f"Unexpected Data Layout: {data}")
                        
            except Exception as e:
                st.error(f"App processing error indicator: {e}")
