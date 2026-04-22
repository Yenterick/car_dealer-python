import sqlite3
from sqlite3 import Connection
from typing import Optional, Any

# Project imports
from ui.consoleUtils import log

# Context for database connection gestor
class Sqlite3Connection:

    def __init__(self, db_path: str='./'):
        self.db_path = db_path
        self.connection: Optional[Connection] = None

    # What it will do when being loaded with "with"
    def __enter__(self) -> Connection | None:
        if self.connection is None:
            return 

        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row

        log("Connection opened...")

        return self.connection
    
    # What it will do when the contexts ends or when it gets an exceptions
    def __exit__(self, exec_type, exec, traceback) -> bool | None:
        if self.connection is None:
            return 
        
        if exec_type is None:
            log("Commiting to exit...")

            self.connection.commit()

        # If it gets an exception
        else:
            log("Undoing changes because of an error...")
            log(f"Exception Type -> {exec_type}")
            log(f"Exception -> {exec}")
            self.connection.rollback()

        self.connection.close()

        return False
    
    def __getattr__(self, name) -> Any:
        return getattr(self.connection, name)
