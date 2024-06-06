import pyodbc

class DatabaseManager:
    def __init__(self, server, user, password, database='master'):
        try:
            self.conn = pyodbc.connect(
                f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                f'SERVER={server};'
                f'UID={user};'
                f'PWD={password};'
                f'DATABASE={database}'
            )
            self.cursor = self.conn.cursor()
            print("Kết nối đến cơ sở dữ liệu SQL Server thành công!")
        except pyodbc.Error as e:
            print(f"Lỗi khi kết nối đến cơ sở dữ liệu SQL Server: {e}")

    def create_database(self):
        try:
            # Tắt autocommit mode
            self.conn.autocommit = True
            
            # Tạo cơ sở dữ liệu TodoList nếu nó chưa tồn tại
            self.cursor.execute("IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'TodoList') CREATE DATABASE TodoList")
            
            # Bật lại autocommit mode
            self.conn.autocommit = False

            self.conn.commit()
            print("Tạo database 'TodoList' thành công!")
        except pyodbc.Error as e:
            print(f"Lỗi khi tạo database: {e}")

    def use_database(self):
        try:
            # Sử dụng cơ sở dữ liệu TodoList
            self.cursor.execute("USE TodoList")
            self.conn.commit()
        except pyodbc.Error as e:
            print(f"Lỗi khi sử dụng database: {e}")

    def create_tables(self):
        try:
            # Tạo bảng users
            self.cursor.execute('''IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' and xtype='U') 
                                    CREATE TABLE users (
                                        user_id INT PRIMARY KEY IDENTITY(1,1),
                                        username VARCHAR(255) UNIQUE NOT NULL,
                                        password VARCHAR(255) NOT NULL,
                                        email VARCHAR(255) UNIQUE,
                                        full_name VARCHAR(255),
                                        birthday DATE,
                                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                                        deleted_at DATETIME NULL,
                                        status INT DEFAULT 1,
                                    )''')

            # Tạo bảng categories
            self.cursor.execute('''IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='categories' and xtype='U') 
                                    CREATE TABLE categories (
                                        category_id INT PRIMARY KEY IDENTITY(1,1),
                                        category_name VARCHAR(255) UNIQUE NOT NULL,
                                        description TEXT,
                                        user_id int,
                                        color nvarchar(50),
                                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                                        deleted_at DATETIME NULL,
                                        status INT DEFAULT 1,
                                    )''')

            # Tạo bảng tasks
            self.cursor.execute('''IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='tasks' and xtype='U') 
                                    CREATE TABLE tasks (
                                        task_id INT PRIMARY KEY IDENTITY(1,1),
                                        user_id INT,
                                        category_id INT,
                                        title VARCHAR(255) NOT NULL,
                                        description TEXT,
                                        due_date DATE,
                                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                                        deleted_at DATETIME NULL,
                                        status INT DEFAULT 1,
                                        FOREIGN KEY (user_id) REFERENCES users (user_id),
                                        FOREIGN KEY (category_id) REFERENCES categories (category_id)
                                    )''')

            self.conn.commit()
            print("Tạo các bảng thành công!")
        except pyodbc.Error as e:
            print(f"Lỗi khi tạo bảng: {e}")

    def add_users_samples(self):
        try:
            # Chèn bản ghi vào bảng users nếu chưa tồn tại
            self.cursor.execute('''INSERT INTO users (username, password, email, full_name, birthday) 
                                SELECT 'admin', 'admin', 'admin@example.com', 'Admin', '2000-01-01'
                                WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = 'admin')''')
            self.cursor.execute('''INSERT INTO users (username, password, email, full_name, birthday) 
                                SELECT 'chieu', 'chieu', 'chieu@example.com', 'Chieu', '2000-01-02'
                                WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = 'chieu')''')
            self.cursor.execute('''INSERT INTO users (username, password, email, full_name, birthday) 
                                SELECT 'tuyen', 'tuyen', 'tuyen@example.com', 'Tuyen', '2000-01-03'
                                WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = 'tuyen')''')
            self.conn.commit()
            print("Thêm người dùng mẫu thành công!")
        except pyodbc.Error as e:
            print(f"Lỗi khi thêm người dùng mẫu: {e}")

    def add_categories_samples(self):
        try:
            # Chèn bản ghi vào bảng categories nếu chưa tồn tại
            self.cursor.execute('''INSERT INTO categories (category_name, description) 
                                SELECT 'Work', 'Công việc hàng ngày'
                                WHERE NOT EXISTS (SELECT 1 FROM categories WHERE category_name = 'Work')''')
            self.cursor.execute('''INSERT INTO categories (category_name, description) 
                                SELECT 'Personal', 'Công việc cá nhân'
                                WHERE NOT EXISTS (SELECT 1 FROM categories WHERE category_name = 'Personal')''')
            self.cursor.execute('''INSERT INTO categories (category_name, description) 
                                SELECT 'Shopping', 'Các mục cần mua'
                                WHERE NOT EXISTS (SELECT 1 FROM categories WHERE category_name = 'Shopping')''')
            self.conn.commit()
            print("Thêm mẫu categories thành công!")
        except pyodbc.Error as e:
            print(f"Lỗi khi thêm mẫu categories: {e}")

    def close_connection(self):
         if self.conn:
            self.conn.close()
            print("Đã đóng kết nối đến cơ sở dữ liệu.")
