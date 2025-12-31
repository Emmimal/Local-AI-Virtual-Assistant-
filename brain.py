import ollama
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_community.chat_models import ChatOllama

llm = ChatOllama(model="llama3.2", temperature=0.7)
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory)

def get_response(user_input: str) -> str:
    response = conversation.predict(input=user_input)
    return response

# Simple test
if __name__ == "__main__":
    print("Local AI Assistant Ready! Type 'quit' to exit.")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["quit", "exit"]:
            break
        reply = get_response(user_input)
        print("Assistant:", reply)
