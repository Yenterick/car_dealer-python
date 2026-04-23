# Project imports
from db.Sqlite3Connection import Sqlite3Connection

from model.command.UndoRedoManager import UndoRedoManager

from ui.consoleUtils import log

class HistoryService:

    def __init__(self, 
                 connection: Sqlite3Connection,
                 undo_manager: UndoRedoManager):
        self.connection = connection
        self.undo_manager = undo_manager

    def undo(self) -> None:
        command = self.undo_manager.get_undo()
        if command is None:
            log("There's nothing to undo.")
            return
        
        with self.connection:
            command.undo(self.connection)

        self.undo_manager.push_redo(command)
        
    def redo(self) -> None:
        command = self.undo_manager.get_redo()
        if command is None:
            log("There's nothing to redo.")
            return
        
        with self.connection:
            command.redo(self.connection)

        self.undo_manager.push_undo(command)
