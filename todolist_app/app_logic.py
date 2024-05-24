import pyodbc

class AppLogic:

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
                return True
            else:
                print("Tên đăng nhập hoặc mật khẩu không đúng.")
                return False
        except pyodbc.Error as e:
            print(f"Lỗi khi thực hiện truy vấn: {e}")
            return False
        finally:
            # Đóng kết nối đến cơ sở dữ liệu
            db_manager.close_connection()
