import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 180)
engine.setProperty('volume', 0.9)

def speak(text: str):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    speak("Hello, I am your local AI assistant.")
