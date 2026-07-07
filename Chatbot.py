import streamlit as st
from openai import OpenAI

# Initialize session state for UI message tracking
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you today?"}
    ]

# Initialize official OpenAI client with mandatory OpenRouter headers
client = OpenAI(
    base_url="https://openrouter.ai",
    api_key=st.secrets["TOGETHER_API_KEY"],
    default_headers={
        "HTTP-Referer": "https://localhost:8501", # Tells OpenRouter where the traffic is coming from
        "X-Title": "Build Fast Chatbot"
    }
)

# Create user interface
st.title("🗣️ Conversational Chatbot")
st.subheader("Simple Chat Interface for LLMs by Build Fast with AI")

# Display chat messages on screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if user_input := st.chat_input("Your question"):
    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message instantly
    with st.chat_message("user"):
        st.write(user_input)
    
    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Construct clean payload history context
                api_messages = [
                    {"role": "system", "content": "You are a helpful AI assistant. Have a natural conversation with the user."}
                ]
                
                # Append the history context securely
                for msg in st.session_state.messages[:-1]:
                    api_messages.append({"role": msg["role"], "content": msg["content"]})
                
                # Add current user prompt explicitly
                api_messages.append({"role": "user", "content": user_input})
                
                # Call OpenRouter through the official, verified SDK channel
                response = client.chat.completions.create(
                    model="meta-llama/llama-3.3-70b-instruct:free",
                    messages=api_messages,
                    temperature=0.7
                )
                
                # Extract text content cleanly
                response_content = response.choices[0].message.content
                
                st.write(response_content)
                
                # Add assistant message to history state
                st.session_state.messages.append({"role": "assistant", "content": response_content})
                
            except Exception as e:
                st.error(f"Something went wrong: {e}")
