import os
import yaml
import json

ATOMICS_DIR = "C:/Users/hecki/Repos/Atomics/atomic-red-team/atomics/"
OUTPUT_FILE = "commands.json"

def extract_commands_from_yaml(yaml_content):
    commands = []
    try:
        data = yaml.safe_load(yaml_content)
        for test in data.get("atomic_tests", []):
            if "executor" in test and "command" in test["executor"]:
                commands.append(test["executor"]["command"])
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
    return commands

def main():
    commands = []

    for root, _, files in os.walk(ATOMICS_DIR):
        for file in files:
            if file.endswith(".yaml"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        yaml_content = f.read()
                        commands.extend(extract_commands_from_yaml(yaml_content))
                    except UnicodeDecodeError as e:
                        print(f"Error reading {file_path}: {e}")

    with open(OUTPUT_FILE, "w", encoding='utf-8') as output_file:
        json.dump(commands, output_file, indent=4, ensure_ascii=False)

    print(f"Extracted {len(commands)} commands and saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
