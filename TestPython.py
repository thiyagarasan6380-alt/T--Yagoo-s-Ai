import pyttsx3
import subprocess

engine=pyttsx3.init()
engine.say("Hello bro.I am your Ai")
engine.say("Tell me what to do")

engine.runAndWait()
def open_app(name):
    subprocess.Popen(name)
open_app("calc.exe")