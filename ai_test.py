
import requests
import subprocess


import requests

def ask_ai(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 100
            }
        },
        timeout=120
    )

    response.raise_for_status()
    return response.json()["response"].strip()

def speak(text):
    safe_text = text.replace("'", "''")

    script = f"""
    Add-Type -AssemblyName System.Speech
    $s = New-Object System.Speech.Synthesis.SpeechSynthesizer
    $s.Speak('{safe_text}')
    $s.Dispose()
    """

    subprocess.run(
        ["powershell", "-NoProfile", "-Command", script],
        check=True
    )
    
response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3.2:3b",
        "prompt": "Introduce yourself as Thiyagarasan's Ai (he is currently studying CSE 2nd year) in one sentence.",
        "stream": False
    },timeout=120
)
response.raise_for_status()
data = response.json()
print("JARVIS:", data["response"])
speak(data["response"])

