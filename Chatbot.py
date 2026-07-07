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
        "HTTP-Referer": "https://localhost:8501",
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
                
                response = client.chat.completions.create(
                    model="meta-llama/llama-3.3-70b-instruct:free",
                    messages=api_messages,
                    temperature=0.7
                )
                
                # FOOLPROOF EXTRACTION: Checks every data format to prevent 'choices' crashes
                if isinstance(response, str):
                    response_content = response
                elif hasattr(response, 'choices') and response.choices:
                    # Check if choices uses array index notation or property notation
                    if isinstance(response.choices, list) and len(response.choices) > 0:
                        choice = response.choices[0]
                        response_content = choice.message.content if hasattr(choice, 'message') else choice.get('message', {}).get('content', str(choice))
                    else:
                        response_content = response.choices.message.content
                elif isinstance(response, dict) and 'choices' in response:
                    response_content = response['choices'][0]['message']['content']
                else:
                    response_content = str(response)
                
                st.write(response_content)
                st.session_state.messages.append({"role": "assistant", "content": response_content})
                
            except Exception as e:
                st.error(f"Something went wrong: {e}")
