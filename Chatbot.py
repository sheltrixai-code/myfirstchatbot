import streamlit as st
import requests

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(page_title="Conversational Chatbot", page_icon="🤖")

st.title("🤖 Conversational Chatbot")
st.subheader("Powered by OpenRouter")

# ----------------------------
# Initialize Chat History
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! How can I help you today?"
        }
    ]

# Display Previous Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ----------------------------
# Get User Input
# ----------------------------
if prompt := st.chat_input("Type your message..."):

    # Display user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant Response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                api_key = st.secrets["OPENROUTER_API_KEY"]

                # Conversation sent to model
                messages = [
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant."
                    }
                ]

                messages.extend(st.session_state.messages)

                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://streamlit.io",
                    "X-Title": "Streamlit Chatbot"
                }

                payload = {
                    "model": "deepseek/deepseek-r1-0528:free",
                    "messages": messages,
                    "temperature": 0.7
                }

                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=60
                )

                # Raise exception if API failed
                response.raise_for_status()

                data = response.json()

                reply = data["choices"][0]["message"]["content"]

                st.markdown(reply)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": reply
                    }
                )

            except KeyError:
                st.error("OPENROUTER_API_KEY not found in Streamlit Secrets.")

            except requests.exceptions.HTTPError:
                try:
                    error_message = response.json()
                except Exception:
                    error_message = response.text
                st.error(f"API Error:\n{error_message}")

            except requests.exceptions.RequestException as e:
                st.error(f"Network Error: {e}")

            except Exception as e:
                st.error(f"Unexpected Error: {e}")

# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:

    st.title("Settings")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hello! How can I help you today?"
            }
        ]
        st.rerun()
