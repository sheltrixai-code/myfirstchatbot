import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Initialize session state for UI messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you today?"}
    ]

# Initialize session state for LangChain message objects
if "langchain_history" not in st.session_state:
    st.session_state.langchain_history = []

# Initialize ChatOpenAI with Together AI
llm = ChatOpenAI(
    model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
    api_key=st.secrets["TOGETHER_API_KEY"],
    base_url="https://together.xyz",
    temperature=0.7
)

# Create a prompt template with message history
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant. Have a natural conversation with the user."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# Create the chain
chain = prompt_template | llm

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
                # Invoke the chain directly, passing our clean list of history messages
                response = chain.invoke({
                    "input": user_input,
                    "history": st.session_state.langchain_history
                })
                
                # Extract content safely
                response_content = response.content if hasattr(response, 'content') else str(response)
                
                st.write(response_content)
                
                # Append both the human and AI response to LangChain memory history
                st.session_state.langchain_history.append(HumanMessage(content=user_input))
                st.session_state.langchain_history.append(AIMessage(content=response_content))
                
                # Add assistant message to UI history
                st.session_state.messages.append({"role": "assistant", "content": response_content})
                
            except Exception as e:
                st.error(f"Something went wrong: {e}")
