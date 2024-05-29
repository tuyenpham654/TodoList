import subprocess
import sys

def install_requirements():
    try:
        # In nội dung của tệp requirements.txt
        with open("requirements.txt", "r") as f:
            requirements = f.read()
            print("Nội dung của requirements.txt:")
            print(requirements)
        
        # Cài đặt các yêu cầu
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("requirements.txt không tồn tại.")
        sys.exit(1)

# Gọi hàm cài đặt môi trường trước khi import các thư viện khác
install_requirements()

from gui import App
from database import DatabaseManager
if __name__ == "__main__":
    db_manager = DatabaseManager(server="localhost", user="sa", password="sa")
    db_manager.create_database()
    db_manager.use_database()
    db_manager.create_tables()
    db_manager.add_users_samples()
    db_manager.add_categories_samples()
    app = App(db_manager)
    app.run()
