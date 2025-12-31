import speech_recognition as sr
import whisper
import warnings
warnings.filterwarnings("ignore")

model = whisper.load_model("base")

def listen_and_transcribe():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source, phrase_time_limit=10)
    
    with open("temp.wav", "wb") as f:
        f.write(audio.get_wav_data())
    
    result = model.transcribe("temp.wav", fp16=False)
    text = result["text"].strip()
    print("You said:", text)
    return text

if __name__ == "__main__":
    listen_and_transcribe()
