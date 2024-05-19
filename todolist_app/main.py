import subprocess
import sys
from gui import App
from database import DatabaseManager

def install_requirements():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

if __name__ == "__main__":
    install_requirements()
    db_manager = DatabaseManager(host="localhost", user="root", password="")
    db_manager.create_database()
    db_manager.use_database()
    db_manager.create_tables()
    app = App()
    app.run()
