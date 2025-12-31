import streamlit as st
from brain import get_response

# Page config
st.set_page_config(
    page_title="My Local AI Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 My Private Local AI Assistant")
st.markdown("""
Powered by **Ollama** • Fully offline • No data leaves your device  
Built following the tutorial:  
[How to Build Your Own AI Virtual Assistant with Python (2025)](https://emitechlogic.com/how-to-build-your-own-ai-virtual-assistant/)
""")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_response(prompt)
        st.markdown(response)
    
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Optional sidebar info
with st.sidebar:
    st.header("About")
    st.write("This is a fully local AI assistant running on your machine.")
    st.write("• LLM: Ollama (e.g., Llama 3.2)")
    st.write("• Privacy: 100% offline")
    st.write("• Source: [GitHub Repo](https://github.com/Emmimal/Local-AI-Virtual-Assistant)")
    
    st.header("Clear Chat")
    if st.button("Clear conversation history"):
        st.session_state.messages = []
        st.rerun()
