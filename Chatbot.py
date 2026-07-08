import streamlit as st
import requests

# 1. Initialize session state for UI message tracking
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you today?"}
    ]

# 2. Create the User Interface layout
st.title("🗣️ Conversational Chatbot")
st.subheader("Simple Chat Interface for LLMs by Build Fast with AI")

# 3. Display existing chat messages on screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 4. Handle incoming user questions
if user_input := st.chat_input("Your question"):
    # Add user message to state and display it instantly
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    
    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Build context history stack safely (excluding the very last entry to prevent repeats)
                api_messages = [
                    {"role": "system", "content": "You are a helpful AI assistant. Have a natural conversation with the user."}
                ]
                for msg in st.session_state.messages[:-1]:
                    api_messages.append({"role": msg["role"], "content": msg["content"]})
                
                # Append the current prompt explicitly to the end of the payload stack
                api_messages.append({"role": "user", "content": user_input})
                
                # Fetch key cleanly and verify spacing strips
                api_key = st.secrets["TOGETHER_API_KEY"].strip().replace('"', '').replace("'", "")
                
                # Setup specific, generic browser headers that OpenRouter requires
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://streamlit.io",
                    "X-Title": "Build Fast AI Chatbot App"
                }
                
                # Set payload to auto-route across active OpenRouter free models
                payload = {
                    "model": "openrouter/free",
                    "messages": api_messages,
                    "temperature": 0.7
                }
                
                # Execute direct network call
                response = requests.post(
                    "https://openrouter.ai",
                    headers=headers,
                    json=payload
                )
                
                # Safeguard: Attempt to parse JSON; fallback cleanly if webpage text returns
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
                    # Informative fallback helper message if the API token fails verification
                    st.error("Authentication failed. Please verify that your OpenRouter API Key is correctly entered in your Streamlit Secrets panel.")
                        
            except Exception as e:
                st.error(f"App processing error indicator: {e}")
