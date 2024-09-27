import sqlite3

def extract_schema_to_file(db_file, output_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    
    # Create a cursor object to interact with the database
    cursor = conn.cursor()
    
    # Execute the command to get the schema
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
    
    # Fetch all results
    schema = cursor.fetchall()
    
    # Open the output file in write mode
    with open(output_file, 'w') as file:
        # Write each table's schema to the file
        for table in schema:
            if table[0]:  # Ensure there is a valid SQL statement
                file.write(table[0] + ';\n\n')  # Add a semicolon and newline for readability
    
    # Close the connection
    conn.close()

# Replace 'your_database_file.db' with your actual database file path
# Replace 'output_schema.sql' with your desired output file name
extract_schema_to_file('M:\dev_env\my_inventory_manager\database\inventory.db', 'output_schema.sql')