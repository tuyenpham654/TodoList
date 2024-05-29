import subprocess
import sys
from gui import App
from database import DatabaseManager

def install_requirements():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

if __name__ == "__main__":
    install_requirements()
    db_manager = DatabaseManager(server="localhost", user="sa", password="123456")
    db_manager.create_database()
    db_manager.use_database()
    db_manager.create_tables()
    db_manager.add_users_samples()
    db_manager.add_categories_samples()
    app = App(db_manager)
    app.run()
