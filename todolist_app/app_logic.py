import pyodbc

class AppLogic:

    def login(self, db_manager, username, password):
        try:
            # Sử dụng cơ sở dữ liệu TodoList
            db_manager.use_database()
            #gán username cho biên global username
            # Thực hiện truy vấn kiểm tra người dùng
            query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
            db_manager.cursor.execute(query)
            user = db_manager.cursor.fetchone()  # Lấy một bản ghi
            # Kiểm tra kết quả trả về từ truy vấn
            if user:
                print("Đăng nhập thành công!")
                self.current_user = user  # Gán user vào thuộc tính current_user
                return user
            
            else:
                print("Tên đăng nhập hoặc mật khẩu không đúng.")
        except pyodbc.Error as e:
            print(f"Lỗi khi thực hiện truy vấn: {e}")
            return False
        finally:
            # Đóng kết nối đến cơ sở dữ liệu
            db_manager.close_connection()
        



    def show_category(self, db_manager):
        try:
            # Sử dụng cơ sở dữ liệu TodoList
            db_manager.use_database()

            # Thực hiện truy vấn kiểm tra người dùng
            query = f"SELECT * FROM categories"
            db_manager.cursor.execute(query)
            categoris = db_manager.cursor.fetchall()  
            if categoris:
                return categoris
            else:
                print("Không có dữ liệu")
        except pyodbc.Error as e:
            print(f"Lỗi khi thực hiện truy vấn: {e}")
            return False
        finally:
            # Đóng kết nối đến cơ sở dữ liệu
            pass

    def add_category(self, db_manager,title,decrip):
        try:
            # Sử dụng cơ sở dữ liệu TodoList
            db_manager.use_database()
            # Thực hiện truy vấn kiểm tra người dùng
            query = f"insert into categories(category_name,[description]) values ({title},{decrip});"
            db_manager.cursor.execute(query)
            print("1 row affect")
            db_manager.commit()
        except pyodbc.Error as e:
            print(f"Lỗi khi thực hiện truy vấn: {e}")
            return False
        finally:
            # Đóng kết nối đến cơ sở dữ liệu
            db_manager.close_connection()

