import subprocess
import requests
import speech_recognition as sr
import webbrowser
import os

APPS = {
    # Code editors and development
    "vscode": {"type": "app", "target": "code"},
    "vs code": {"type": "app", "target": "code"},
    "anti gravity": {"type": "app", "target": "antigravity"},
    "android studio": {
        "type": "app",
        "target": r"C:\Program Files\Android\Android Studio\bin\studio64.exe"
    },
    "dev c++": {"type": "app", "target": "devcpp"},
    "dev-c++": {"type": "app", "target": "devcpp"},
    "intellij": {"type": "app", "target": "idea64"},
    "pycharm": {"type": "app", "target": "pycharm64"},

    # Databases
    "mysql": {
    "type": "app",
    "target": r"C:\Program Files\MySQL\MySQL Workbench 8.0\MySQLWorkbench.exe"
    },
    "mysql workbench": {
        "type": "app",
        "target": r"C:\Program Files\MySQL\MySQL Workbench 8.0\MySQLWorkbench.exe"
    },

    # Browsers
    "google chrome": {"type": "app", "target": "chrome"},
    "google chrome": {"type": "app", "target": "chrome"},
    "brave": {"type": "app", "target": "brave"},
    "edge": {"type": "app", "target": "msedge"},
    "firefox": {"type": "app", "target": "firefox"},

    # Office and productivity
    "wps office": {"type": "app", "target": "wps"},
    "word": {"type": "app", "target": "winword"},
    "excel": {"type": "app", "target": "excel"},
    "powerpoint": {"type": "app", "target": "powerpnt"},
    "notepad": {"type": "app", "target": "notepad.exe"},
    "calculator": {"type": "app", "target": "calc.exe"},

    # Media
    "vlc": {"type": "app", "target": "vlc"},
    "spotify": {"type": "app", "target": "spotify"},
    "paint": {"type": "app", "target": "mspaint.exe"},

    # Windows utilities
    "this pc": {"type": "system", "target": "shell:MyComputerFolder"},
    "file explorer": {"type": "system", "target": "explorer.exe"},
    "task manager": {"type": "system", "target": "taskmgr.exe"},
    "control panel": {"type": "system", "target": "control.exe"},
    "settings": {"type": "system", "target": "ms-settings:"},
    "command prompt": {"type": "system", "target": "cmd.exe"},
    "powershell": {"type": "system", "target": "powershell.exe"},

    # Websites
    "youtube": {"type": "website", "target": "https://www.youtube.com"},
    "github": {"type": "website", "target": "https://github.com"},
    "google": {"type": "website", "target": "https://www.google.com"},
    "gmail": {"type": "website", "target": "https://mail.google.com"},
    "chatgpt": {"type": "website", "target": "https://chatgpt.com"},
    "stackoverflow": {"type": "website", "target": "https://stackoverflow.com"},
    "wikipedia": {"type": "website", "target": "https://www.wikipedia.org"},
}
def speak(text):

    script = """
    Add-Type -AssemblyName System.Speech
    $s = New-Object System.Speech.Synthesis.SpeechSynthesizer
    $text = [Console]::In.ReadToEnd()
    $s.Speak($text)
    $s.Dispose()
    """

    subprocess.run(
        ["powershell", "-NoProfile", "-Command", script],
        input=text,
        text=True,
        check=True
    )

chat_history = []

def ask_ai(prompt):
    chat_history.append({
        "role": "user",
        "content": prompt
    })

    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "llama3.2:3b",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are JARVIS, a helpful personal AI assistant. "
                        "Give direct answers in 2-4 short sentences. "
                        "For simple questions, answer in 1-2 sentences. "
                        "Avoid long lists and markdown formatting. "
                        "Remember the conversation context."
                    )
                },
                *chat_history
            ],
            "stream": False,
            "keep_alive": "10m",
            "options": {
                "num_predict": 100,
                "num_ctx": 2048,
                "temperature": 0.3
                        }
        },
        timeout=120
    )

    response.raise_for_status()

    answer = response.json()["message"]["content"].strip()

    chat_history.append({
        "role": "assistant",
        "content": answer
    })

    return answer



def launch_app(target):
    # 1. If target is a full executable path, launch it directly
    if os.path.isfile(target):
        subprocess.Popen([target])
        return True

    # 2. Try commands available in Windows PATH
    try:
        subprocess.Popen([target], shell=False)
        return True
    except FileNotFoundError:
        pass

    # 3. Check common installation locations
    paths = {
        "brave": [
            os.path.expandvars(
                r"%ProgramFiles%\BraveSoftware\Brave-Browser\Application\brave.exe"
            ),
            os.path.expandvars(
                r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\Application\brave.exe"
            )
        ],
        "chrome": [
            os.path.expandvars(
                r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"
            ),
            os.path.expandvars(
                r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
            ),
            os.path.expandvars(
                r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
            )
        ],
        "code": [
            os.path.expandvars(
                r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe"
            ),
            os.path.expandvars(
                r"%ProgramFiles%\Microsoft VS Code\Code.exe"
            )
        ]
    }

    for path in paths.get(target.lower(), []):
        if os.path.isfile(path):
            subprocess.Popen([path])
            return True

    return False



def parse_command(command):
    command = command.lower().strip()
    command = command.replace("jarvis", "", 1)
    command = command.strip(" ,.!?")

    parts = command.split(" and ")
    actions = []

    for part in parts:
        part = part.strip(" ,.!?")

        if part.startswith("open "):
            target = part[5:].strip()
            actions.append({
                "action": "open",
                "target": target or None
            })

        elif part.startswith("create a file named "):
            filename = part.replace(
                "create a file named ", "", 1
            ).strip()

            actions.append({
                "action": "create_file",
                "target": filename or None
            })

        else:
            actions.append({
                "action": "ask_ai",
                "target": part
            })

    return actions


def open_app(command):
    command = command.lower().strip()

    for app_name, details in sorted(
        APPS.items(),
        key=lambda item: len(item[0]),
        reverse=True
    ):
        if app_name in command:
            app_type = details["type"]
            target = details["target"]

            try:
                if app_type == "website":
                    webbrowser.open(target)

                elif app_type == "system":
                    subprocess.Popen(
                        ["explorer.exe", target]
                        if target.startswith("shell:")
                        else [target],
                        shell=False
                    )

                elif app_type == "app":
                    if not launch_app(target):
                        print(f"JARVIS: Executable not found for {app_name}")
                        speak(f"I couldn't locate {app_name}")
                        return True

                speak(f"Opening {app_name}")
                print(f"JARVIS: Launched {app_name}")
                return True

            except OSError as error:
                print(f"JARVIS: Could not open {app_name}: {error}")
                speak(f"I couldn't open {app_name}")
                return True

    return False


def execute_actions(actions):
    for item in actions:
        action = item["action"]
        target = item["target"]

        if not target:
            speak("Please specify what you want me to do.")
            continue

        if action == "open":
            if not open_app(target):
                speak(f"I don't know how to open {target}")

        
            elif action == "create_file":
                filename = os.path.basename(target).strip()

                if not filename or filename in (".", ".."):
                    speak("Please give me a valid filename.")
                    continue

                try:
                    file_path = os.path.abspath(filename)

                    with open(file_path, "x", encoding="utf-8"):
                        pass

                    if os.path.isfile(file_path):
                        print(f"JARVIS: File verified at: {file_path}")
                        speak(f"File created successfully: {filename}")
                    else:
                        print("JARVIS: File verification failed.")
                        speak("I couldn't verify that the file was created.")

                except FileExistsError:
                    print(f"JARVIS: File already exists at: {file_path}")
                    speak("That file already exists.")

                except OSError as error:
                    print("JARVIS: File creation failed:", error)
                    speak("I couldn't create the file.")


            elif action == "ask_ai":
                        answer = ask_ai(target)
                        print("JARVIS:", answer)
                        speak(answer)


speak("Hello sir. JARVIS is ready.")

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("JARVIS: Calibrating microphone...")
    recognizer.adjust_for_ambient_noise(source, duration=0.5)
    print("JARVIS: Listening...")

    while True:
        try:
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=5
            )

            command = recognizer.recognize_google(audio).strip()
            print("You said:", command)

            
            command_lower = command.lower().strip()

            shutdown_commands = [
                "jarvis stop",
                "stop jarvis",
                "shutdown jarvis",
                "shut down jarvis",
                "shut down jarv",
                "shutdown jarv",
                "exit jarvis",
                "quit jarvis"
            ]

            if any(phrase in command_lower for phrase in shutdown_commands):
                speak("Shutting down. Goodbye sir.")
                break


            
            if command_lower in ["open", "open the", "launch", "start"]:
                speak("Which application should I open?")
                continue

            print("JARVIS: Processing command...")
            


            # Handle incomplete app-opening commands
            if command_lower in ["open", "open the", "launch", "start"]:
                speak("Which application should I open?")
                continue

            answer = ask_ai(command)
            print("JARVIS:", answer)
            print("JARVIS: Starting speech...")
            speak(answer)
            print("JARVIS: Speech finished.")

        except sr.WaitTimeoutError:
            print("JARVIS: Still waiting for your command.")

        except sr.UnknownValueError:
            print("JARVIS: I couldn't understand that.")

        except sr.RequestError:
            print("JARVIS: Speech recognition service unavailable.")

        except requests.RequestException as error:
            print("JARVIS: AI connection error:", error)
            speak("I couldn't connect to my AI brain.")
