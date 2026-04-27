# Project imports
from typing import Callable
from db.Sqlite3Connection import Sqlite3Connection

from model.command.UndoRedoManager import UndoRedoManager

from ui.consoleUtils import log

class HistoryService:

    def __init__(self, 
                 connection_factory: Callable[[], Sqlite3Connection],
                 undo_manager: UndoRedoManager):
        self.connection_factory = connection_factory
        self.undo_manager = undo_manager

    def undo(self) -> None:
        command = self.undo_manager.get_undo()
        if command is None:
            log("There's nothing to undo.")
            return
        
        with self.connection_factory() as connection:
            command.undo(connection)

        self.undo_manager.push_redo(command)
        
    def redo(self) -> None:
        command = self.undo_manager.get_redo()
        if command is None:
            log("There's nothing to redo.")
            return
        
        with self.connection_factory() as connection:
            command.redo(connection)

        self.undo_manager.push_undo(command)

    def get_history(self) -> list:
        """Returns a list of operations from the undo/redo stacks"""
        history = []
        # Operations that can be undone
        for cmd in reversed(self.undo_manager.undo_stack):
            history.append({
                'operation': cmd.__class__.__name__.replace('Insert', 'Added ').replace('Delete', 'Removed '),
                'status': 'Done'
            })
        # Operations that can be redone
        for cmd in reversed(self.undo_manager.redo_stack):
            history.append({
                'operation': cmd.__class__.__name__.replace('Insert', 'Added ').replace('Delete', 'Removed '),
                'status': 'Undone'
            })
        return history
