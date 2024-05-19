import mysql.connector
class DatabaseManager:
    def __init__(self, host, user, password):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
        )
        self.cursor = self.conn.cursor()

    def create_database(self):
        # Create TodoList database if it doesn't exist
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS TodoList")
        self.conn.commit()

    def use_database(self):
        # Use TodoList database
        self.cursor.execute("USE TodoList")

    def create_tables(self):
        # Create users table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                user_id INTEGER PRIMARY KEY,
                                username VARCHAR(255) UNIQUE NOT NULL,
                                password VARCHAR(255) NOT NULL,
                                email VARCHAR(255) UNIQUE,
                                full_name VARCHAR(255),
                                birthday DATE,
                                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                deleted_at TIMESTAMP NULL,
                                status BOOLEAN DEFAULT TRUE
                            )''')

        # Create categories table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS categories (
                                category_id INTEGER PRIMARY KEY,
                                category_name VARCHAR(255) UNIQUE NOT NULL,
                                description TEXT,
                                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                deleted_at TIMESTAMP NULL,
                                status BOOLEAN DEFAULT TRUE
                            )''')

        # Create tasks table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                                task_id INTEGER PRIMARY KEY,
                                user_id INTEGER,
                                category_id INTEGER,
                                title VARCHAR(255) NOT NULL,
                                description TEXT,
                                due_date DATE,
                                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                deleted_at TIMESTAMP NULL,
                                status BOOLEAN DEFAULT TRUE,
                                FOREIGN KEY (user_id) REFERENCES users (user_id),
                                FOREIGN KEY (category_id) REFERENCES categories (category_id)
                            )''')

        self.conn.commit()

    def close_connection(self):
        self.conn.close()

if __name__ == "__main__":
    host = "localhost"
    user = "your_username"
    password = "your_password"

    db_manager = DatabaseManager(host, user, password, "")
    db_manager.create_database()
    db_manager.use_database()
    db_manager.create_tables()
    db_manager.close_connection()
