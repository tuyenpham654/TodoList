import pyodbc

class AppLogic:
    def __init__(self):
        self.current_user = None

    def login(self, db_manager, username, password):
        try:
            # Sử dụng cơ sở dữ liệu TodoList
            db_manager.use_database()

            # Thực hiện truy vấn kiểm tra người dùng
            query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
            db_manager.cursor.execute(query)
            user = db_manager.cursor.fetchone()  # Lấy một bản ghi
            
            # Kiểm tra kết quả trả về từ truy vấn
            if user:
                print("Đăng nhập thành công!")
                self.set_current_user(user)  # Gán thông tin người dùng cho self.current_user
                self.get_user_name(user)
                return True
            else:
                print("Tên đăng nhập hoặc mật khẩu không đúng.")
                return False
        except pyodbc.Error as e:
            print(f"Lỗi khi thực hiện truy vấn: {e}")
            return False
        
    def set_current_user(self, user):
        self.current_user = user

    def get_user_name(self, user):
        self.current_user = user
        if self.current_user is None:
            print("Chưa có người dùng nào đăng nhập.")
            return None
        try:
            # Giả sử trường thứ hai trong tuple `self.current_user` là tên người dùng
            user_name = self.current_user[4]
            return user_name
        except IndexError:
            print("Không thể lấy tên người dùng từ dữ liệu người dùng hiện tại.")
            return None
        
    def get_user_tasks(self, db_manager):
        print("Current user:", self.current_user)
        if self.current_user is None:
            print("No user is currently logged in.")
            return []
        try:
            # Sử dụng cơ sở dữ liệu TodoList
            db_manager.use_database()

            # Thực hiện truy vấn để lấy các nhiệm vụ của người dùng hiện tại
            user_id = self.current_user[0]  # Assuming the first field is user_id
            query = "SELECT * FROM tasks WHERE user_id = ?"
            db_manager.cursor.execute(query, (user_id,))
            tasks = db_manager.cursor.fetchall()
            
            return tasks
        except pyodbc.Error as e:
            print(f"Lỗi khi thực hiện truy vấn: {e}")
            return []
        finally:
            # Đóng kết nối đến cơ sở dữ liệu
            db_manager.close_connection()
