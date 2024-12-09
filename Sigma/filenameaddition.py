import os
from pathlib import Path

def process_files(yaml_folder_path, target_file_path):
    """
    Process YAML files and insert their names into odd-numbered lines of the target file
    while preserving existing content on even-numbered lines.
    
    Args:
        yaml_folder_path (str): Path to folder containing YAML files
        target_file_path (str): Path to the target file to modify
    """
    # Read all YAML filenames from the folder
    yaml_files = sorted([f.name for f in Path(yaml_folder_path).glob("*.yml")])
    
    # Read existing content from the target file
    with open(target_file_path, 'r') as f:
        existing_content = f.readlines()
    
    # Remove any trailing newlines and empty lines
    existing_content = [line.rstrip() for line in existing_content if line.strip()]
    
    # Create new content list
    new_content = []
    
    # Add yaml filenames and existing content alternately
    for i in range(max(len(yaml_files), len(existing_content))):
        # Add YAML filename if available
        if i < len(yaml_files):
            new_content.append(yaml_files[i] + '\n')
        else:
            new_content.append('\n')  # Empty line if no more YAML files
            
        # Add existing content if available (preserve even-numbered lines)
        if i < len(existing_content):
            new_content.append(existing_content[i] + '\n')
        else:
            new_content.append('\n')  # Empty line if no more existing content
    
    # Write the modified content back to the file
    with open(target_file_path, 'w') as f:
        f.writelines(new_content)

def main():
    # Example usage
    yaml_folder = r"C:\Users\hecki\Desktop\Code\sigma\test1"  # Replace with your YAML files folder path
    target_file = r"C:\Users\hecki\Desktop\Code\sigma\testout2.txt"   # Replace with your target file path
    
    try:
        process_files(yaml_folder, target_file)
        print("File processing completed successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()