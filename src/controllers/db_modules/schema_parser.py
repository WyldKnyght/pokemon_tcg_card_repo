import contextlib
class SchemaParser:
    @staticmethod
    def parse_schema(schema_path: str) -> dict:
        """
        Parse a schema file and return a dictionary of tables and their columns.

        Args:
            schema_path (str): The path to the schema file.

        Returns:
            dict: A dictionary of tables and their columns.
        """
        with contextlib.suppress(FileNotFoundError):
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