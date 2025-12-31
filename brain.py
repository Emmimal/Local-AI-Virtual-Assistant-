# brain.py - Full-featured agent with memory and tools

from langchain_community.chat_models import ChatOllama
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType, Tool
from langchain_core.messages import SystemMessage
from tools import get_current_date_time, calculator_tool

# Initialize LLM
llm = ChatOllama(model="llama3.2", temperature=0.7)

# Memory for conversation history
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Wrap your tools properly (LangChain expects Tool objects)
tools = [
    get_current_date_time,
    calculator_tool
    # Add more tools here later (RAG, web search, etc.)
]

# Create the agent with memory
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,  # Best for memory + tools
    memory=memory,
    verbose=True,
    handle_parsing_errors=True  # Prevents crashes on bad output
)

# Optional: Set a friendly system prompt
agent.agent.llm_chain.prompt.messages[0] = SystemMessage(content=(
    "You are a helpful, friendly local AI assistant. "
    "Use tools when needed. Be concise and natural in responses."
))

def get_response(user_input: str) -> str:
    """
    Send user input to the agent and return the response.
    """
    try:
        response = agent.invoke({"input": user_input})
        return response["output"]
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

# Simple test loop
if __name__ == "__main__":
    print("Local AI Assistant Ready! (with memory + tools)")
    print("Type 'quit' to exit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Goodbye!")
            break
        reply = get_response(user_input)
        print("Assistant:", reply)
