# src/db_ops_components/load_json_file.py
import json

def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)