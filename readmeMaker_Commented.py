import os

def generate_links_for_readme(parent_folder):
    # Initialize the content of the README.md file with a title
    readme_content = "# File Links\n\n"

    # Walk through the directory tree rooted at parent_folder
    for root, _, files in os.walk(parent_folder):
        # Iterate over each file in the current directory
        for file in files:
            # Get the full path of the file
            file_path = os.path.join(root, file)
            # Get the relative path of the file with respect to the parent folder
            relative_path = os.path.relpath(file_path, parent_folder)
            # Replace OS-specific path separator with a forward slash for Markdown compatibility
            relative_path = relative_path.replace(os.sep, '/')
            # Append a Markdown link for the file to the README content
            readme_content += f"[{relative_path}]({relative_path})\n\n"

    # Write the generated content to README.md in the parent folder
    with open(os.path.join(parent_folder, "README.md"), "w") as readme_file:
        readme_file.write(readme_content)

# Example usage:
# Specify the path to the parent folder you want to scan
parent_folder = "path_to_your_folder"
generate_links_for_readme(parent_folder)

