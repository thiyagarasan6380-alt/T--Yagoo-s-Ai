
def parse_command(command):
    command = command.lower().strip()
    command = command.replace("jarvis", "", 1)
    command = command.strip(" ,.!?")

    # Split a sentence into separate actions
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

def execute_actions(actions):
    for item in actions:
        action = item["action"]
        target = item["target"]

        if action == "open":
            print(f"Opening application: {target}")

        elif action == "create_file":
            print(f"Creating file: {target}")

        elif action == "ask_ai":
            print(f"Asking AI: {target}")


tests = [
    "Open Android Studio",
    "Jarvis, open VS Code",
    "Create a file named ex.java",
    "What is Java?",
    "Open VS Code and create a file named ex.java",
    "Jarvis, open Android Studio and open VS Code"
]

command = "Open VS Code and create a file named ex.java"

actions = parse_command(command)
execute_actions(actions)