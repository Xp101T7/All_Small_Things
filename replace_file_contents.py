import sys

def replace_whitespace_in_file_contents(file_path):
    """
    Replace all white spaces in the contents of a specified file with underscores.
    """
    try:
        # Read the content of the file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Replace white spaces with underscores
        new_content = content.replace(' ', '_')
        
        # Write the new content back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        
        print(f"Processed file: {file_path}")
    except FileNotFoundError:
        print(f"The specified file '{file_path}' does not exist.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while processing the file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    """
    Entry point of the script. This block will only be executed if the script is run directly,
    not when it is imported as a module.
    """
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python replace_file_contents.py <file_path>")  # Print usage instructions
        sys.exit(1)  # Exit the script with a status code of 1 (indicating an error)
    
    # Get the file path from the command-line arguments
    file_path = sys.argv[1]
    
    # Process the specified file to replace white spaces in its contents
    replace_whitespace_in_file_contents(file_path)
