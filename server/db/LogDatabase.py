import json

class LogDatabase:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.create_log_table()

    def create_log_table(self):
        """Create a table for logs if it doesn't exist."""
        with self.db_connection as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    service_name TEXT,
                    ip_address TEXT,
                    location TEXT,
                    grpc_system_response_time REAL,
                    grpc_system_latency REAL,
                    total_response_time REAL,
                    total_latency REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def save_log(self, log_entry):
        """Insert the log entry into the SQL database."""
        with self.db_connection as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO logs (service_name, ip_address, location, 
                                  grpc_system_response_time, grpc_system_latency, 
                                  total_response_time, total_latency)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                log_entry.service_name,
                log_entry.ip_address,
                json.dumps(log_entry.location),  # Convert location dict to JSON string
                log_entry.grpc_system_response_time,
                log_entry.grpc_system_latency,
                log_entry.total_response_time,
                log_entry.total_latency
            ))
            conn.commit()
