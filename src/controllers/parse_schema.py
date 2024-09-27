# src/controllers/parse_schema.py

def parse_schema(schema_path):
    with open(schema_path, 'r') as f:
        schema = f.read()
    
    tables = {}
    current_table = None
    for line in schema.split('\n'):
        if line.strip().startswith('CREATE TABLE'):
            current_table = line.split('(')[0].split()[-1]
            tables[current_table] = []
        elif current_table and line.strip().startswith(')'):
            current_table = None
        elif current_table:
            column = line.strip().split()[0]
            if column not in ['PRIMARY', 'FOREIGN']:
                tables[current_table].append(column)
    
    return tables