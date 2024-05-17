import json
import csv
import random
from faker import Faker
from datetime import datetime

fake = Faker()

def load_lines_from_file(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]

def generate_sysmon_event(event_id, command_line, process_name):
    sysmon_events = {
        1: "Process Create",
        3: "Network Connection",
        5: "Process Terminate",
        7: "Image Load",
        11: "File Create"
    }
    return {
        "EventID": event_id,
        "EventType": sysmon_events.get(event_id, "Unknown"),
        "ComputerName": fake.hostname(),
        "User": fake.user_name(),
        "ProcessID": random.randint(1000, 9999),
        "ProcessName": process_name,
        "CommandLine": command_line,
        "LogonID": random.randint(100000, 999999),
        "LogonGuid": fake.uuid4(),
        "SourceProcessID": random.randint(1000, 9999),
        "SourceProcessName": random.choice(process_names),
        "SourceImage": generate_executable_path(),
        "DestinationProcessID": random.randint(1000, 9999),
        "DestinationProcessName": random.choice(process_names),
        "DestinationImage": generate_executable_path(),
        "UtcTime": datetime.utcnow().isoformat() + "Z"
    }

def generate_executable_path():
    directories = ['C:\\Program Files', 'C:\\Windows', 'C:\\Users\\Public']
    extensions = ['.exe', '.dll']
    directory = random.choice(directories)
    filename = fake.file_name(extension=random.choice(extensions))
    return f"{directory}\\{filename}"

def create_fake_logs(num_logs):
    logs = []
    for _ in range(num_logs):
        event_id = random.choice([1, 3, 5, 7, 11])  # Example Sysmon Event IDs
        command_line = random.choice(commands)
        process_name = random.choice(process_names)
        log = generate_sysmon_event(event_id, command_line, process_name)
        logs.append(log)
    return logs

def save_logs_to_json(logs, filename):
    with open(filename, 'w') as file:
        json.dump(logs, file, indent=4)

def save_logs_to_csv(logs, filename):
    with open(filename, 'w', newline='') as file:
        fieldnames = logs[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for log in logs:
            writer.writerow(log)

if __name__ == "__main__":
    commands_file = 'C:/Users/hecki/Repos/Atomics/atomic-red-team/FakerAtomics/commands.json'
    process_names_file = 'C:/Users/hecki/Repos/Atomics/atomic-red-team/FakerAtomics/process_names.txt'

    commands = load_lines_from_file(commands_file)
    process_names = load_lines_from_file(process_names_file)

    num_logs = 1500  # Number of logs to generate
    json_filename = 'sysmon_fake_logs.json'
    csv_filename = 'sysmon_fake_logs.csv'

    logs = create_fake_logs(num_logs)
    save_logs_to_json(logs, json_filename)
    save_logs_to_csv(logs, csv_filename)

    print(f"{num_logs} fake Sysmon logs have been generated and saved to {json_filename} and {csv_filename}")
