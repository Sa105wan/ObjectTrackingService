import sqlite3

class DatabaseConnection:
    def __init__(self, db_file='server_logs.db'):
        self.db_file = db_file
        self.connection = None

    def __enter__(self):
        """Establish the database connection."""
        self.connection = sqlite3.connect(self.db_file)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the database connection automatically."""
        if self.connection:
            self.connection.close()
