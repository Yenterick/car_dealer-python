from service.HistoryService import HistoryService

class HistoryController:

    def __init__(self, history_service: HistoryService):
        self.history_service = history_service

    def undo(self) -> None:
        self.history_service.undo()

    def redo(self) -> None:
        self.history_service.redo()

    def get_history(self) -> list:
        """Return a list of dicts describing the undo/redo stacks"""
        history = []

        for cmd in self.history_service.undo_manager.undo_stack:
            history.append({
                'operation': type(cmd).__name__,
                'status': '↩️ Undoable'
            })

        for cmd in self.history_service.undo_manager.redo_stack:
            history.append({
                'operation': type(cmd).__name__,
                'status': '↪️ Redoable'
            })

        return history
