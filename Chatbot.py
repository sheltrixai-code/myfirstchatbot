import streamlit as st
import requests

# Initialize session state for UI message tracking
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you today?"}]

# Create user interface layout
st.title("🗣️ Conversational Chatbot")
st.subheader("Simple Chat Interface for LLMs by Build Fast with AI")

# Display existing chat messages on screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Handle incoming user questions
if user_input := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Build context history stack safely
                api_messages = [{"role": "system", "content": "You are a helpful AI assistant."}]
                for msg in st.session_state.messages[:-1]:
                    api_messages.append({"role": msg["role"], "content": msg["content"]})
                api_messages.append({"role": "user", "content": user_input})
                
                # Fetch key cleanly from Streamlit secrets config
                api_key = st.secrets["TOGETHER_API_KEY"].strip().replace('"', '').replace("'", "")
                
                # CRITICAL HEADERS: Added User-Agent to bypass OpenRouter's bot firewall challenge
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://streamlit.io",
                    "X-Title": "Build Fast AI Chatbot App",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                }
                
                payload = {
                    "model": "google/gemini-2.5-flash:free",
                    "messages": api_messages,
                    "temperature": 0.7
                }
                
                # Execute direct network call
                response = requests.post(
                    "https://openrouter.ai",
                    headers=headers,
                    json=payload
                )
                
                try:
                    data = response.json()
                except Exception:
                    data = None

                if data and "choices" in data:
                    response_content = data["choices"][0]["message"]["content"]
                    st.write(response_content)
                    st.session_state.messages.append({"role": "assistant", "content": response_content})
                elif data and "error" in data:
                    st.error(f"OpenRouter System Error: {data['error']['message']}")
                else:
                    st.error(f"Server sent text fallback structure. First 300 characters: {response.text[:300]}")
                        
            except Exception as e:
                st.error(f"App processing error indicator: {e}")
