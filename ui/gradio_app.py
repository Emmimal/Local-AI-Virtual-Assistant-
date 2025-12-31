import gradio as gr
from brain import get_response

def respond(message, history):
    response = get_response(message)
    history.append((message, response))
    return "", history

with gr.Blocks(title="My Local AI Assistant") as demo:
    gr.Markdown("# My Private Local AI Assistant")
    gr.Markdown("Powered by Ollama • Fully offline • Built with ❤️ following [this tutorial](https://emitechlogic.com/how-to-build-your-own-ai-virtual-assistant/)")
    
    chatbot = gr.Chatbot(height=600)
    msg = gr.Textbox(label="Ask me anything", placeholder="Type your message here...")
    clear = gr.Button("Clear")

    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)
