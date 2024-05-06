import os

# Define the folder structure as a dictionary
folder_structure = {
    "Detection Coverage": ["MITRE Mapping"],
    "Detection Implementation": ["Rule Discovery", "Enabling Rules", "Confidence Tailoring", "Deployment Testing"],
    "Detection Quality": ["Fidelity, Accuracy, Alert Noise/Volume Review", "Current and Updated Use Case Review",
                          "Manual Production Search Testing", "Data Model Review"],
    "Detection Development": ["Developing New Content", "Deploying New Content", "Reviewing Onboarding/Archiving Potential"],
    "Detection and Lifecycle Management": ["Review Dev Process Workflows within SnapAttack"],
    "Threat Research": ["Review Hunt Library", "Review Hunt Results", "Review Scheduled Hunts", "Review IOC Hunter"],
    "Detection Validation": ["Review Attack Script Library", "Review Attack Simulation Functionality"],
    "Reporting": ["Evaluate ATT&CK Matrix Mapping", "Evaluate Detection Dashboard", "Evaluate SOC Manager Dashboard",
                  "Evaluate NIST 800-53 Dashboard", "Evaluate User Activity Dashboard", "Evaluate Content Dashboard"],
    "Vendor Response": ["Evaluate and Score Response Criteria from SnapAttack Team"]
}

# Path where to create the structure
base_path = "SnapAttack_PoC_Evaluation"

# Function to create directories based on the folder structure
def create_directories(base_path, structure):
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    
    for main_folder, sub_folders in structure.items():
        main_folder_path = os.path.join(base_path, main_folder)
        if not os.path.exists(main_folder_path):
            os.makedirs(main_folder_path)
        
        for sub_folder in sub_folders:
            sub_folder_path = os.path.join(main_folder_path, sub_folder)
            if not os.path.exists(sub_folder_path):
                os.makedirs(sub_folder_path)

# Function to create markdown files in each subfolder with the provided content template
def create_markdown_files(base_path, structure):
    content_template = """
- **Evaluation Criteria:**
- **Grade:** [Poor/Good/Excellent]
- **Product Feedback:**
- **Shortcomings:**
- **Vendor Questionnaire:**
    """

    for main_folder, sub_folders in structure.items():
        main_folder_path = os.path.join(base_path, main_folder)
        for sub_folder in sub_folders:
            sub_folder_path = os.path.join(main_folder_path, sub_folder)
            # Create a markdown file for each subfolder
            file_path = os.path.join(sub_folder_path, "evaluation_criteria.md")
            with open(file_path, 'w') as file:
                file.write(content_template)

# Create the folder structure
create_directories(base_path, folder_structure)

# Create markdown files
create_markdown_files(base_path, folder_structure)

print(f"Folder structure and markdown files created under '{base_path}'.")
