import streamlit as st
import requests

# Initialize session state for UI message tracking
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
                
                # CRITICAL HARDCODED TEST: Replace the text inside the quotes below with your real OpenRouter key
                # It must look exactly like: api_key = "sk-or-v1-a1b2c3d4..."
                api_key = "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"
                
                # Direct API call to the chat completions endpoint path
                response = requests.post(
                    "https://openrouter.ai",
                    headers={
                        "Authorization": f"Bearer {api_key.strip()}",
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
                
                try:
                    data = response.json()
                except Exception:
                    data = None

                if data and "choices" in data:
                    response_content = data["choices"]["message"]["content"]
                    st.write(response_content)
                    st.session_state.messages.append({"role": "assistant", "content": response_content})
                elif data and "error" in data:
                    st.error(f"OpenRouter Error response: {data['error']['message']}")
                else:
                    # Capture raw website text response if key configuration fails completely
                    st.error(f"Server response code ({response.status_code}): {response.text[:500]}")
                        
            except Exception as e:
                st.error(f"App processing error indicator: {e}")
