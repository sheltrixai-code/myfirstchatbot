import streamlit as st
from langchain_together import ChatTogether
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Initialize session state for UI and history tracking
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you today?"}
    ]

# Initialize ChatTogether using OpenRouter's free service
llm = ChatTogether(
    model="meta-llama/llama-3.3-70b-instruct:free",
    together_api_key=st.secrets["TOGETHER_API_KEY"],
    base_url="https://openrouter.ai",
    temperature=0.7
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
    # Add user message to UI state
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.write(user_input)
    
    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Build a clean list of message objects directly for the LLM
                formatted_messages = [
                    SystemMessage(content="You are a helpful AI assistant. Have a natural conversation with the user.")
                ]
                
                # Dynamically load the previous back-and-forth context from session state
                for msg in st.session_state.messages[:-1]:  # Exclude the newest input we just added
                    if msg["role"] == "user":
                        formatted_messages.append(HumanMessage(content=msg["content"]))
                    elif msg["role"] == "assistant":
                        formatted_messages.append(AIMessage(content=msg["content"]))
                
                # Append the brand new question at the end
                formatted_messages.append(HumanMessage(content=user_input))
                
                # Invoke the model directly using the structured messages array
                response = llm.invoke(formatted_messages)
                
                # Extract content safely
                response_content = response.content if hasattr(response, 'content') else str(response)
                
                st.write(response_content)
                
                # Add assistant message to UI history
                st.session_state.messages.append({"role": "assistant", "content": response_content})
                
            except Exception as e:
                st.error(f"Something went wrong: {e}")
