import os
from treelib import Tree
import datetime


def generate_folder_structure(root_dir, output_file=None, excluded_dirs=None):
    tree = Tree()
    tree.create_node(root_dir, root_dir)  # Create the root node

    # Convert excluded_dirs to a set (if it's not already)
    excluded_dirs = set(excluded_dirs) if excluded_dirs else set()

    def add_to_tree(directory, parent):
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                if item in excluded_dirs:
                    continue
                node = tree.create_node(item, item_path, parent=parent)
                add_to_tree(item_path, node)
            else:
                # Add files to the tree
                file_name = os.path.basename(item_path)
                tree.create_node(file_name, item_path, parent=parent)

    # Call the add_to_tree function here
    add_to_tree(root_dir, root_dir)  # Build the tree structure

    if output_file:
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(str(tree))

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\nScript last modified: {timestamp}")
    if output_file:
        with open(output_file, "a", encoding="utf-8") as file:
            file.write(f"\nScript last modified: {timestamp}")

if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    admin_dir = os.path.join(project_root, ".admin")
    os.makedirs(admin_dir, exist_ok=True)  # Create docs directory if it doesn't exist
    output_filename = os.path.join(admin_dir, "folder_structure.txt")
    excluded_dirs = {
        ".git",
        ".venv",
        ".vs",
        ".my_files",
        "__pycache__",
        ".github",
        ".admin",
        ".vscode",
        ".myfiles",
        ".mypy_cache"
    }

    print(f"Project Folder Structure for: {project_root}")
    generate_folder_structure(project_root, output_file=output_filename, excluded_dirs=excluded_dirs)

