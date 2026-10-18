import pyttsx3

engine = pyttsx3.init()
print("Testing speech...")

engine.say("Hello sir, I am Jarvis.")
engine.runAndWait()

print("Speech test finished.")