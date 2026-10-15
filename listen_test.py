import subprocess

import pyttsx3

import speech_recognition as sr

def open_app(name):
    app=name+".exe"
    subprocess.Popen(app)

engine=pyttsx3.init()
engine.say("Hello Sir ,how was your day ...")
engine.say("Do you need to say something ...")

engine.runAndWait()
recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("JARVIS: Listening...")
    recognizer.adjust_for_ambient_noise(source, duration=1)
    audio = recognizer.listen(
    source,
    timeout=5,
    phrase_time_limit=5
)

try:
    command = recognizer.recognize_google(audio)
    print("You said:", command)

except sr.WaitTimeoutError:
    print("JARVIS: I didn't hear anything.")

except sr.UnknownValueError:
    print("JARVIS: I couldn't understand you.")

except sr.RequestError:
    print("JARVIS: Speech service unavailable.")

open_app(command)