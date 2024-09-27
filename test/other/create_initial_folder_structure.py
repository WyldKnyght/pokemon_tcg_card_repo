import os

# Define the folder and file structure
structure = {
    "src": {
        "main.py": "",
        "framework": {
            "item.py": "",
            "category.py": ""
        },
        "user_interface": {
            "main_window.py": "",
            "item_view.py": "",
            "category_view.py": ""
        },
        "controllers": {
            "item_controller.py": "",
            "category_controller.py": ""
        },
        "utils": {
            "logger.py": "",
            "helpers.py": ""
        }
    },
    "database": {
        "inventory.db": "",
        "db.py": "",
        "schema.sql": ""
    },
    "tests": {
        "test_items.py": "",
        "test_categories.py": ""
    },
    "docs": {
        "README.md": "",
        "user_guide.md": ""
    },
    "requirements.txt": "",
    ".gitignore": ""
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            # Create directory if it doesn't exist
            if os.path.exists(path):
                print(f"Directory already exists: {path}")
            else:
                os.makedirs(path)
                print(f"Created directory: {path}")
            # Recursively create subdirectories and files
            create_structure(path, content)
        elif not os.path.exists(path):
            with open(path, 'w') as file:
                file.write(content)
            print(f"Created file: {path}")
        else:
            print(f"File already exists: {path}")

# Create the folder and file structure in the current directory
base_path = "."  # Current directory
create_structure(base_path, structure)