import os
from dotenv import load_dotenv

load_dotenv()

class ConfigManager:
    def __init__(self):
        self.database_connection_string = os.getenv("DATABASE_CONNECTION_STRING")
        self.file_storage_path = os.getenv("FILE_STORAGE_PATH")
        self.security_key = os.getenv("SECURITY_KEY")
    
    def get_database_connection_string(self):
        return self.database_connection_string
    
    def get_file_storage_path(self):
        return self.file_storage_path
    
    def get_security_key(self):
        return self.security_key
    
config_manager = ConfigManager()
print(config_manager.get_database_connection_string())
print(config_manager.get_file_storage_path())
print(config_manager.get_security_key())