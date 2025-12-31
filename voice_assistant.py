from voice_input import listen_and_transcribe
from tts import speak
from brain import get_response

print("Voice Assistant Started! Say 'quit' to exit.")

while True:
    try:
        user_input = listen_and_transcribe()
        if "quit" in user_input.lower() or "exit" in user_input.lower():
            speak("Goodbye!")
            break
        
        response = get_response(user_input)
        speak(response)
    except KeyboardInterrupt:
        speak("Goodbye!")
        break
    except Exception as e:
        speak("Sorry, something went wrong.")
        print("Error:", e)
