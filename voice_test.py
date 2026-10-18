
import subprocess

def speak(text):
    script = f'''
    Add-Type -AssemblyName System.Speech
    $s = New-Object System.Speech.Synthesis.SpeechSynthesizer
    $s.Speak("{text}")
    $s.Dispose()
    '''

    subprocess.run(
        ["powershell", "-NoProfile", "-Command", script],
        check=True
    )

speak("Hello sir, I am Jarvis. Voice system is online.")
