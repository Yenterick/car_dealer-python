import sqlite3
from sqlite3 import Connection
from typing import Any

# Project imports
from ui.consoleUtils import log

# Context for database connection gestor
class Sqlite3Connection:

    def __init__(self, db_path: str='./'):
        self.db_path = db_path
        self.connection: Connection | None = None

    # What it will do when being loaded with "with"
    def __enter__(self) -> 'Sqlite3Connection':
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row

        log("Connection opened...")

        return self
    
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
        if self.connection is None:
            raise AttributeError("Connection not initialized")
        return getattr(self.connection, name)
