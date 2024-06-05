import pyodbc
from datetime import datetime
class Auth:
    current_user = None
    curret_category=None
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
    def category(self,category_id):
        Auth.currnet_category=category_id
        pass
    @classmethod
    def get_current_user(cls):
        # print(self.current_user)
        return cls.current_user
    def get_current_category(cls):
        print(cls.curret_category)
        return cls.curret_category

class AppLogic:

    def get_user_tasks(self, db_manager):
        user = Auth.get_current_user()
        if user is None:
            print("Chưa có người dùng nào đăng nhập.")
            return []
        try:
            # Sử dụng cơ sở dữ liệu TodoList
            db_manager.use_database()

            user_id = user[0]  # Assuming the first field is user_id
            query = "SELECT * FROM tasks WHERE user_id = ? AND deleted_at IS NULL AND status = 1"
            db_manager.cursor.execute(query, (user_id,))
            tasks = db_manager.cursor.fetchall()
            
            return tasks
        except pyodbc.Error as e:
            print(f"Lỗi khi thực hiện truy vấn: {e}")
            return []
    
    def get_user_tasks_other(self, db_manager):
        user = Auth.get_current_user()
        if user is None:
            print("Chưa có người dùng nào đăng nhập.")
            return []
        try:
            # Sử dụng cơ sở dữ liệu TodoList
            db_manager.use_database()

            user_id = user[0]  # Assuming the first field is user_id
            query = "SELECT * FROM tasks WHERE user_id = ? AND status != 1"
            db_manager.cursor.execute(query, (user_id,))
            tasks = db_manager.cursor.fetchall()
            
            return tasks
        except pyodbc.Error as e:
            print(f"Lỗi khi thực hiện truy vấn: {e}")
            return []

    def get_user_categories(self, db_manager):
        user = Auth.get_current_user()
        if user is None:
            print("Chưa có người dùng nào đăng nhập.")
            return []
        try:
            # Sử dụng cơ sở dữ liệu TodoList
            db_manager.use_database()

            user_id = user[0]  # Assuming the first field is user_id
            query = "SELECT * FROM categories WHERE user_id = ? AND deleted_at IS NULL AND status = 1"
            db_manager.cursor.execute(query, (user_id,))
            categories = db_manager.cursor.fetchall()
            
            return categories
        except pyodbc.Error as e:
            print(f"Lỗi khi thực hiện truy vấn: {e}")
            return []

    def add_task(self, db_manager, title, category_id=None, description=None, due_date=None):
        user = Auth.get_current_user()
        if user is None:
            print("No user is currently logged in.")
            return False
        
        try:
            # Sử dụng cơ sở dữ liệu TodoList
            db_manager.use_database()

            user_id = user[0]  # Assuming the first field is user_id
            query = """INSERT INTO tasks (user_id, category_id, title, description, due_date, updated_at, created_at, status) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
            current_datetime = datetime.now()
            status = 1 
            db_manager.cursor.execute(query, (user_id, category_id, title, description, due_date, current_datetime, current_datetime, status))
            db_manager.conn.commit()
            print("Task added successfully!")
            return True
        except pyodbc.Error as e:
            print(f"Lỗi khi thực hiện truy vấn: {e}")
            return False
        
    def destroy_task(self, db_manager, task_id):
        user = Auth.get_current_user()
        if user is None:
            print("No user is currently logged in.")
            return False  
        try:
            # Sử dụng cơ sở dữ liệu TodoList
            db_manager.use_database()

            user_id = user[0]  # Assuming the first field is user_id
            query = """UPDATE tasks 
                    SET deleted_at = ?,
                    status = ?  
                    WHERE task_id = ? AND user_id = ?"""
            current_datetime = datetime.now()
            status = 0
            db_manager.cursor.execute(query, (current_datetime, status, task_id, user_id))
            db_manager.conn.commit()
            print("Task destroyed successfully!")
            return True
        except pyodbc.Error as e:
            print(f"Lỗi khi thực hiện truy vấn: {e}")
            return False
        
    def destroy_category(self, db_manager, category_id):
        user = Auth.get_current_user()
        if user is None:
            print("No user is currently logged in.")
            return False  
        try:
            # Sử dụng cơ sở dữ liệu TodoList
            db_manager.use_database()

            user_id = user[0]  # Assuming the first field is user_id
            query = """UPDATE category 
                    SET deleted_at = ?,
                    status = ?  
                    WHERE category_id = ? AND user_id = ?"""
            current_datetime = datetime.now()
            status = 0
            db_manager.cursor.execute(query, (current_datetime, status, category_id, user_id))
            db_manager.conn.commit()
            print("Category destroyed successfully!")
            return True
        except pyodbc.Error as e:
            print(f"Lỗi khi thực hiện truy vấn: {e}")
            return False
    def get_task_by_id(self, db_manager, task_id):
        query = "SELECT * FROM tasks WHERE task_id = ? AND deleted_at IS NULL AND status = 1"
        result = db_manager.cursor.execute(query, (task_id,))
        task = result.fetchone() 
        print(task)
        return task
    
    def update_task(self, db_manager, task_id, title=None, category_id=None, description=None, due_date=None):
        user = Auth.get_current_user()
        if user is None:
            print("No user is currently logged in.")
            return False

        try:
            # Sử dụng cơ sở dữ liệu TodoList
            db_manager.use_database()

            current_datetime = datetime.now()

            # Tạo câu lệnh SQL UPDATE dựa trên các tham số được cung cấp
            update_fields = []
            update_values = []

            if title is not None:
                update_fields.append("title = ?")
                update_values.append(title)

            if category_id is not None:
                update_fields.append("category_id = ?")
                update_values.append(category_id)

            if description is not None:
                update_fields.append("description = ?")
                update_values.append(description)

            if due_date is not None:
                try:
                    due_date_str = due_date.strftime('%Y-%m-%d') 
                    update_fields.append("due_date = ?")
                    update_values.append(due_date_str)
                except AttributeError:
                    print("Invalid due date format")


            # Nếu không có trường nào được cập nhật, thông báo và kết thúc
            if not update_fields:
                print("No fields to update.")
                return False

            # Thêm trường updated_at vào danh sách cập nhật
            update_fields.append("updated_at = ?")
            update_values.append(current_datetime)

            # Thêm task_id vào danh sách giá trị cho điều kiện WHERE
            update_values.append(task_id)

            # Tạo câu lệnh SQL UPDATE hoàn chỉnh
            update_query = f"""UPDATE tasks SET {', '.join(update_fields)} WHERE task_id = ?"""

            # Thực hiện truy vấn UPDATE
            db_manager.cursor.execute(update_query, tuple(update_values))
            db_manager.conn.commit()
            print("Task updated successfully!")
            return True
        except pyodbc.Error as e:
            print(f"Lỗi khi thực hiện truy vấn: {e}")
            return False
    
    def completed_task(self, db_manager, task_id):
        user = Auth.get_current_user()
        if user is None:
            print("No user is currently logged in.")
            return False  
        try:
            # Sử dụng cơ sở dữ liệu TodoList
            db_manager.use_database()

            user_id = user[0]  # Assuming the first field is user_id
            query = """UPDATE tasks 
                    SET updated_at = ?,
                        status = ? 
                    WHERE task_id = ? AND user_id = ?"""
            current_datetime = datetime.now()
            status = 2
            db_manager.cursor.execute(query, (current_datetime, status, task_id, user_id))
            db_manager.conn.commit()
            print("Task marked as completed successfully!")
            return True
        except pyodbc.Error as e:
            print(f"Lỗi khi thực hiện truy vấn: {e}")
            return False

    def list_categories(self, db_manager):
        user = Auth.get_current_user()
        if user is None:
            print("Chưa có người dùng nào đăng nhập.")
            return []
        try:
            # Sử dụng cơ sở dữ liệu TodoList
            db_manager.use_database()

            user_id = user[0]
            # Thực hiện truy vấn kiểm tra người dùng
            query = f"SELECT * FROM categories where user_id = ? AND deleted_at IS NULL AND status = 1"
            db_manager.cursor.execute(query,(user_id,))
            categoris = db_manager.cursor.fetchall()  
            if categoris:
                return categoris
            else:
                print("Không có dữ liệu")
        except pyodbc.Error as e:
            print(f"Lỗi khi thực hiện truy vấn: {e}")
            return False
            
    def get_user_name(self):
        user = Auth.get_current_user()
        if user is None:
            print("Chưa có người dùng nào đăng nhập.")
            return None
        try:
            user_name = user[4]
            return user_name
        except IndexError:
            print("Không thể lấy tên người dùng từ dữ liệu người dùng hiện tại.")
            return None
        
    def get_user_by_id(self, db_manager, user_id):
        query = "SELECT * FROM users WHERE user_id = ?"
        result = db_manager.cursor.execute(query, (user_id,))
        user_data = result.fetchone()
        if user_data:
            user = {
                "user_id": user_data[0],
                "email": user_data[3],
                "full_name": user_data[4],
                "birthday": user_data[5],
                "updated_at": user_data[6],
                "created_at": user_data[7],
                "deleted_at": user_data[8]
            }
            return user
        else:
            return None
        
    def update_user(self, db_manager, user_id, email, full_name, birthday):
        try:
            query = """
            UPDATE users 
            SET email = ?, full_name = ?, birthday = ?, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
            """
            db_manager.cursor.execute(query, ( email, full_name, birthday, user_id))
            db_manager.conn.commit()
            return True
        except Exception as e:
            print("Error while updating user:", e)
            return False
        
    def change_password(self, db_manager, user_id, old_password, new_password):
        # Truy vấn để lấy mật khẩu hiện tại từ cơ sở dữ liệu
        query = "SELECT password FROM users WHERE user_id = ?"
        result = db_manager.cursor.execute(query, (user_id,))
        current_password = result.fetchone()[0]

        # Kiểm tra xem mật khẩu hiện tại có khớp với mật khẩu đã nhập không
        if old_password != current_password:
            return False

        # Nếu mật khẩu hiện tại khớp, tiến hành cập nhật mật khẩu mới vào cơ sở dữ liệu
        update_query = "UPDATE users SET password = ? WHERE user_id = ?"
        db_manager.cursor.execute(update_query, (new_password, user_id))
        db_manager.conn.commit()
        return True
    
    def register(self, db_manager,username, password ,email,full_name, birthday):
        # Kiểm tra xem người dùng có tồn tại trong cơ sở dữ liệu chưa
        query = "SELECT * FROM users WHERE username = ?"
        result = db_manager.cursor.execute(query, (username,))
        existing_user = result.fetchone()
        if existing_user:
            return False, "Tên người dùng đã tồn tại. Vui lòng chọn một tên người dùng khác."
    
        # Thêm người dùng mới vào cơ sở dữ liệu
        query = "INSERT INTO users (username, password, email, full_name, birthday) VALUES (?, ?, ?, ?, ?)"
        try:
            db_manager.cursor.execute(query, ( username, password, email, full_name, birthday))
            db_manager.conn.commit()
            return True, "Đăng ký thành công."
        except Exception as e:
            return False, f"Lỗi: {str(e)}"
    
    def add_category(self, db_manager,category_name, description=None):
        user = Auth.get_current_user()
        if user is None:
            print("No user is currently logged in.")
            return False
        
        try:
            # Sử dụng cơ sở dữ liệu TodoList
            db_manager.use_database()

            user_id = user[0]  # Assuming the first field is user_id
            query = """INSERT INTO categories (category_name, description, user_id, updated_at, created_at, status) 
                    VALUES (?, ?, ?, ?, ?, ?)"""
            current_datetime = datetime.now()
            status = 1 
            db_manager.cursor.execute(query, (category_name, description, user_id, current_datetime, current_datetime, status))
            db_manager.conn.commit()
            print("Category added successfully!")
            return True
        except pyodbc.Error as e:
            print(f"Lỗi khi thực hiện truy vấn: {e}")
            return False

    def get_category_by_id(self, db_manager, category_id):
        query = "SELECT * FROM categories WHERE category_id = ? AND deleted_at IS NULL AND status = 1"
        result = db_manager.cursor.execute(query, (category_id,))
        task = result.fetchone() 
        print(task)
        return task
    
    def update_category(self, db_manager, category_id, name=None, description=None):
        user = Auth.get_current_user()
        if user is None:
            print("No user is currently logged in.")
            return False

        try:
            # Sử dụng cơ sở dữ liệu TodoList
            db_manager.use_database()

            current_datetime = datetime.now()

            # Tạo câu lệnh SQL UPDATE dựa trên các tham số được cung cấp
            update_fields = []
            update_values = []

            if name is not None:
                update_fields.append("category_name = ?")
                update_values.append(name)

            if description is not None:
                update_fields.append("description = ?")
                update_values.append(description)


            # Nếu không có trường nào được cập nhật, thông báo và kết thúc
            if not update_fields:
                print("No fields to update.")
                return False

            # Thêm trường updated_at vào danh sách cập nhật
            update_fields.append("updated_at = ?")
            update_values.append(current_datetime)

            # Thêm task_id vào danh sách giá trị cho điều kiện WHERE
            update_values.append(category_id)

            # Tạo câu lệnh SQL UPDATE hoàn chỉnh
            update_query = f"""UPDATE categories SET {', '.join(update_fields)} WHERE category_id = ?"""

            # Thực hiện truy vấn UPDATE
            db_manager.cursor.execute(update_query, tuple(update_values))
            db_manager.conn.commit()
            print("Category updated successfully!")
            return True
        except pyodbc.Error as e:
            print(f"Lỗi khi thực hiện truy vấn: {e}")
            return False
        
    def get_task_by_category(self, db_manager,category_id):
        user = Auth.get_current_user()
        if user is None:
            print("Chưa có người dùng nào đăng nhập.")
            return []
        try:
            # Sử dụng cơ sở dữ liệu TodoList
            db_manager.use_database()

            user_id = user[0]  # Assuming the first field is user_id
            query = "SELECT * FROM tasks WHERE user_id = ? AND category_id = ? AND deleted_at IS NULL AND status = 1"
            db_manager.cursor.execute(query, (user_id,category_id))
            tasks = db_manager.cursor.fetchall()
            
            return tasks
        except pyodbc.Error as e:
            print(f"Lỗi khi thực hiện truy vấn: {e}")
            return []
    
    def get_task_by_category_other(self, db_manager,category_id):
        user = Auth.get_current_user()
        if user is None:
            print("Chưa có người dùng nào đăng nhập.")
            return []
        try:
            # Sử dụng cơ sở dữ liệu TodoList
            db_manager.use_database()

            user_id = user[0]  # Assuming the first field is user_id
            query = "SELECT * FROM tasks WHERE user_id = ? AND category_id = ? AND status != 1"
            db_manager.cursor.execute(query, (user_id,category_id))
            tasks = db_manager.cursor.fetchall()
            
            return tasks
        except pyodbc.Error as e:
            print(f"Lỗi khi thực hiện truy vấn: {e}")
            return []






