import os  # Import the os module for interacting with the operating system
import sys  # Import the sys module for accessing command-line arguments

def replace_whitespace_with_underscore(folder):
    """
    Replace all white spaces in file and directory names within the specified folder
    and its subdirectories with underscores.
    """
    # Walk through the directory tree rooted at 'folder'
    for root, dirs, files in os.walk(folder):
        # Iterate over each file in the current directory
        for file in files:
            # Replace white spaces with underscores in the file name
            new_file_name = file.replace(' ', '_')
            # Check if the file name has changed
            if new_file_name != file:
                # Construct full file paths
                old_file_path = os.path.join(root, file)  # Full path to the current file
                new_file_path = os.path.join(root, new_file_name)  # Full path to the new file name
                # Rename the file
                os.rename(old_file_path, new_file_path)
                # Print a message indicating the file was renamed
                print(f"Renamed file: {old_file_path} to {new_file_path}")

        # Iterate over each directory in the current directory
        for dir in dirs:
            # Replace white spaces with underscores in the directory name
            new_dir_name = dir.replace(' ', '_')
            # Check if the directory name has changed
            if new_dir_name != dir:
                # Construct full directory paths
                old_dir_path = os.path.join(root, dir)  # Full path to the current directory
                new_dir_path = os.path.join(root, new_dir_name)  # Full path to the new directory name
                # Rename the directory
                os.rename(old_dir_path, new_dir_path)
                # Print a message indicating the directory was renamed
                print(f"Renamed directory: {old_dir_path} to {new_dir_path}")

if __name__ == "__main__":
    """
    Entry point of the script. This block will only be executed if the script is run directly,
    not when it is imported as a module.
    """
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python rename_files.py <folder_path>")  # Print usage instructions
        sys.exit(1)  # Exit the script with a status code of 1 (indicating an error)
    
    # Get the folder path from the command-line arguments
    folder_path = sys.argv[1]
    
    # Check if the specified path is a directory
    if not os.path.isdir(folder_path):
        print(f"The specified path '{folder_path}' is not a directory.")  # Print an error message
        sys.exit(1)  # Exit the script with a status code of 1 (indicating an error)
    
    # Call the function to replace white spaces with underscores in file and directory names
    replace_whitespace_with_underscore(folder_path)
