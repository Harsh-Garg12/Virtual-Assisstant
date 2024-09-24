import speech_recognition as sr
import pyttsx3
import sounddevice as sd
import numpy as np
import datetime

recognizer = sr.Recognizer()
speaker = pyttsx3.init()

def speak(text: str):
    speaker.say(text)
    speaker.runAndWait()

def listen_for_command():
    # Parameters for sounddevice
    sample_rate = 16000  # Google API prefers 16kHz
    duration = 4  # Record for 5 seconds (you can adjust this)
    
    # Notify the user that listening has started
    speak("Hi, I am here to assist you with any query")

    # Capture audio using sounddevice
    print("Listening...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()  # Wait for the recording to finish

    # Convert sounddevice's audio to recognizer's format
    audio_np = np.squeeze(audio_data)  # Remove single-dimensional entries
    audio_bytes = audio_np.tobytes()  # Convert to bytes
    audio = sr.AudioData(audio_bytes, sample_rate, 2)  # 2 bytes per sample for 16-bit audio

    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        print("Could not understand audio. Please try again.")
        return None
    except sr.RequestError:
        print("Unable to access the Google Speech Recognition API.")
        return None

if __name__ == "__main__":
    command = listen_for_command()
    if 'time' in command and 'date' in command:
        time = datetime.datetime.now().strftime('%I:%M%p')
        today = datetime.date.today()
        date_text = today.strftime("%A, %B %d, %Y")

        speak("Today is " + date_text + " and the time right now is " + time)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M%p')
        speak("Current time is " + time)
    elif 'date' in command:
        today = datetime.date.today()
        date_text = today.strftime("%A, %B %d, %Y")
        print(date_text)
        speak("Today's date is " + date_text)
    else:
        speak("It's great to talk with you")
