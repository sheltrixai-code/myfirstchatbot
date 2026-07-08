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
                for msg in st.session_state.messages[:-1]:
                    api_messages.append({"role": msg["role"], "content": msg["content"]})
                api_messages.append({"role": "user", "content": user_input}) 
                # Fetch key cleanly and verify spacing strips
                api_key = st.secrets["TOGETHER_API_KEY"].strip().replace('"', '').replace("'", "") 
                # Direct API Call to the chat completions endpoint path
                response = requests.post(
                    "https://openrouter.ai",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://streamlit.io",
                        "X-Title": "Build Fast AI Chatbot App"
                    },
                    json={
                        "model": "openrouter/free",
                        "messages": api_messages,
                        "temperature": 0.7
                    }
                ) 
                # Verify if the payload is valid JSON content
                try:
                    data = response.json()
                except Exception:
                    data = None
                if data and "choices" in data:
                    response_content = data["choices"][0]["message"]["content"]
                    st.write(response_content)
                    st.session_state.messages.append({"role": "assistant", "content": response_content})
                elif data and "error" in data:
                    st.error(f"OpenRouter Error: {data['error']['message']}")
                else:
                    # Security catch to display if the key authentication fails
                    st.error("Authentication failed. Please verify that your OpenRouter API Key is correctly entered in your Streamlit Secrets panel.")  
            except Exception as e:
                st.error(f"App processing error indicator: {e}")
