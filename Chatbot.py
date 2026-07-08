import streamlit as st
import requests

# 1. Initialize session state for UI message tracking
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you today?"}]

# 2. Render user interface headers
st.title("🗣️ Conversational Chatbot")
st.subheader("Simple Chat Interface for LLMs by Build Fast with AI")

# 3. Render previous chat text dialogue components 
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 4. Process incoming conversation prompts
if user_input := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Structure message data history context payload array
                api_messages = [{"role": "system", "content": "You are a helpful AI assistant."}]
                for msg in st.session_state.messages[:-1]:
                    api_messages.append({"role": msg["role"], "content": msg["content"]})
                api_messages.append({"role": "user", "content": user_input})
                
                # Extract api key cleanly from Streamlit Cloud Secrets dashboard environment
                api_key = st.secrets["TOGETHER_API_KEY"].strip().replace('"', '').replace("'", "")
                
                # Execute direct network call with universal headers
                response = requests.post(
                    "https://openrouter.ai",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://streamlit.io",
                        "X-Title": "Build Fast AI Chatbot App",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    },
                    json={
                        # UNIVERSAL FREEMIUM ROUTER: Automatically finds an available online free model
                        "model": "openrouter/free",
                        "messages": api_messages,
                        "temperature": 0.7
                    }
                )
                
                # Check for bad server authentication gateway loops before parsing json structures
                if "html" in response.text.lower() or response.status_code == 401:
                    st.error("Authentication Error: The OpenRouter API key inside your Streamlit Cloud Secrets panel is invalid or copied incorrectly. Please generate a fresh key starting with 'sk-or-v1-' on OpenRouter and save it again.")
                else:
                    data = response.json()
                    if "choices" in data and len(data["choices"]) > 0:
                        response_content = data["choices"][0]["message"]["content"]
                        st.write(response_content)
                        st.session_state.messages.append({"role": "assistant", "content": response_content})
                    elif "error" in data:
                        st.error(f"OpenRouter Gateway Error Message: {data['error']['message']}")
                    else:
                        st.error(f"Unexpected Data Structure. Server status {response.status_code}. Response: {response.text[:200]}")
                        
            except Exception as e:
                st.error(f"App internal loop processing error: {e}")
