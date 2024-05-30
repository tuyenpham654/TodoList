import pyodbc
class Auth:
    current_user = None
    
    def __init__(self):
        pass

    def login(self, db_manager, username, password):
        try:
            db_manager.use_database()
            query = f"SELECT * FROM users WHERE username = ? AND password = ?"
            db_manager.cursor.execute(query, (username, password))
            user = db_manager.cursor.fetchone()
            
            # Kiểm tra kết quả trả về từ truy vấn
            if user:
                Auth.current_user = user  # Gán thông tin người dùng cho biến class
                return user
            else:
                print("Tên đăng nhập hoặc mật khẩu không đúng.")
                return False
        except pyodbc.Error as e:
            print(f"Lỗi khi thực hiện truy vấn: {e}")
            return False
        
    def set_current_user(self, user):
        self.current_user = user
        
    @classmethod
    def get_current_user(cls):
        # print(self.current_user)
        return cls.current_user

class AppLogic:

    def get_user_tasks(self, db_manager):
        user = Auth.get_current_user()
        if user is None:
            print("Chưa có người dùng nào đăng nhập.")
            return []
        try:
            # Sử dụng cơ sở dữ liệu TodoList
            db_manager.use_database()

            # Thực hiện truy vấn để lấy các nhiệm vụ của người dùng hiện tại
            user_id = user[0]  # Assuming the first field is user_id
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
            
    def get_user_name(self):
        auth = Auth()
        user = auth.get_current_user()
        print("get", user)
        if user is None:
            print("Chưa có người dùng nào đăng nhập.")
            return None
        try:
            # Giả sử trường thứ hai trong tuple `self.current_user` là tên người dùng
            user_name = user[4]
            return user_name
        except IndexError:
            print("Không thể lấy tên người dùng từ dữ liệu người dùng hiện tại.")
            return None
