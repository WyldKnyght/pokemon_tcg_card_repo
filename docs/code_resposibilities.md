1. db_operations.py:
   - Provides a high-level interface for database operations
   - Manages database transactions
   - Coordinates database setup, table creation, data loading, and data validation
   - Executes queries
   - Manages the connection pool

2. data_load.py:
   - Handles loading of set data and card data into the database
   - Reads JSON files containing card and set information
   - Filters data based on test mode settings
   - Uses DataInsert for actual data insertion
   - Manages the overall data loading process

3. connection_pool.py:
   - Manages a pool of database connections
   - Provides methods for getting and returning connections
   - Handles connection validation and cleanup
   - Implements connection timeout and retry logic
   - Provides pool status information and reset functionality

4. config.py:
   - Centralizes configuration settings for the entire application
   - Loads environment variables from a .env file
   - Defines constants like database paths, data directories, and test sets
   - Provides methods for validating configuration settings
   - Offers a method to print the current configuration

5. data_check.py:
   - Initializes with a database cursor and retrieves table information from the schema
   - Performs checks on card-related data for specific card IDs
   - Performs checks on set-related data for specific set IDs
   - Counts and reports the number of rows in all database tables
   - Verifies the existence of all expected tables in the database
   - Provides a comprehensive method to run all checks in sequence
   - Implements error handling for check operations
   - Utilizes logging to report check results and any issues encountered

6. data_execute.py:
   - Provides a unified interface for executing various SQL operations
   - Implements retry logic for handling database locks during query execution
   - Executes SQL queries and returns results
   - Executes SQL schema scripts, handling existing table errors
   - Executes SQL scripts with retry functionality
   - Performs batch insert operations with error handling and logging
   - Utilizes error handling decorators for consistent error management
   - Logs detailed information about execution errors for debugging purposes

7. data_insert.py:
   - Provides a class (DataInsert) for handling data insertion operations into the database
   - Generates SQL insert statements dynamically based on table names and columns
   - Performs bulk insert operations for efficient data loading
   - Handles insertion of both card and set data into their respective tables
   - Manages data insertion within database transactions for data integrity
   - Implements error handling and logging for insert operations
   - Supports flexible data insertion based on table prefixes (e.g., 'card_', 'set_')
   - Utilizes the provided database schema for accurate data insertion

8. data_processor.py:
   - Provides a DataProcessor class for processing and loading card data into the database
   - Parses the database schema from a SQL file
   - Prepares row data for insertion, handling different data types and structures
   - Implements retry logic for database operations in case of database locks
   - Processes card files in chunks for efficient memory usage and database insertion
   - Supports both test mode and full data loading mode
   - Uses ijson for memory-efficient parsing of large JSON files
   - Provides progress tracking using tqdm for long-running operations
   - Handles file reading and JSON parsing errors with appropriate logging
   - Coordinates with DataInsert class for actual data insertion operations

9. data_validator.py:
   - Provides a DataValidator class for validating the integrity and completeness of the database
   - Uses the DataCheck class to perform specific validation checks
   - Validates sample card data by checking related information across multiple tables
   - Validates sample card set data by examining set-related tables
   - Checks row counts for all tables in the database
   - Implements progress tracking using tqdm for long-running validation processes
   - Coordinates the execution of multiple validation checks in sequence
   - Provides a high-level interface for comprehensive database validation

10. db_connection.py:
   - Provides a function `get_db_connection` for establishing a connection to the SQLite database
   - Configures the database connection with specific performance-optimizing settings:
     - Sets the journal mode to WAL (Write-Ahead Logging) for improved concurrency
     - Configures the cache size for better performance
     - Sets the synchronous mode to optimize write performance
   - Allows customization of connection parameters such as timeout and isolation level
   - Uses the database path specified in the Config class
   - Returns a configured SQLite connection object ready for use

11. schema_manager.py:
   - Provides a SchemaManager class for managing the database schema
   - Implements methods for creating and updating database tables
   - Executes the SQL schema file, handling existing table errors
   - Sets up the database with optimized SQLite pragmas for improved performance
   - Uses error handling and logging for schema execution operations
   - Utilizes the database connection from db_connection.py
   - Provides a static method for initial database setup, including schema execution and pragma configuration
   - Separates schema execution logic from table creation, allowing for flexible schema management

12. update_repo.py:
   - Provides functionality to update a Git repository
   - Implements a `run_command` function for executing shell commands safely
   - Defines an `update_repo` function to check for and pull updates from a remote repository
   - Includes error handling and logging for Git operations
   - Uses the Config class to get the repository path
   - Implements a main function to orchestrate the repository update process
   - Checks for the existence of the repository path before attempting to update
   - Logs the status of the update process, including success and failure messages

13. main.py:
   - Serves as the main entry point for the application
   - Sets up logging for the entire application
   - Prints the current configuration settings
   - Orchestrates the overall process flow:
     - Updates the repository
     - Updates the database schema
     - Populates the database with data
     - Validates the database contents
   - Implements error handling for the main process
   - Provides a clean exit in case of errors

14. schema.sql:
   - Defines the structure of the Pokemon TCG card database
   - Creates tables for storing card information, including:
     - Main tables: cards, card_sets
     - Card attribute tables: card_subtypes, card_types, card_evolves_to, card_rules
     - Card detail tables: card_ancient_traits, card_abilities, card_attacks
     - Card game-related tables: card_weaknesses, card_resistances, card_retreat_cost
     - Card metadata tables: card_national_pokedex_numbers, card_legalities, card_images
     - Card market data tables: card_tcgplayer, card_cardmarket
   - Creates tables for storing set information: set_legalities, set_images
   - Establishes relationships between tables using foreign keys
   - Implements indexes on frequently queried columns for improved performance
   - Uses SQLite-specific pragmas for optimizing database operations
   - Provides a comprehensive structure for storing detailed information about Pokemon cards and sets
   - Allows for efficient querying and data retrieval across various aspects of the Pokemon TCG
