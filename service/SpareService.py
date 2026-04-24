from typing import List, Callable

# Project imports
from db.Sqlite3Connection import Sqlite3Connection

from model.vo.SpareVO import SpareVO
from model.dao.SpareDAO import SpareDAO

from model.command.UndoRedoManager import UndoRedoManager
from model.command.spare.InsertSpare import InsertSpare
from model.command.spare.DeleteSpare import DeleteSpare

from ui.consoleUtils import log

class SpareService:

    def __init__(self, 
                 connection_factory: Callable[[], Sqlite3Connection],
                 undo_manager: UndoRedoManager):
        self.connection_factory = connection_factory
        self.undo_manager = undo_manager

    def get_all_spares(self) -> List[SpareVO]:
        return SpareDAO.get_all_spares()
    
    def get_spare(self, spare_id: int) -> SpareVO | None:
        return SpareDAO.get_spare(spare_id)

    def select_all_supplier_spares(self, supplier_id: int) -> List[SpareVO] | None:
        with self.connection_factory() as connection:
            return SpareDAO.select_all_supplier_spares(connection, supplier_id)

    def insert_spare(self, 
                     spare: SpareVO):
        command = InsertSpare(spare)

        with self.connection_factory() as connection:
            command.redo(connection)

        self.undo_manager.register(command)

    def delete_spare(self,
                     spare: SpareVO) -> None:
        command = DeleteSpare(spare)

        with self.connection_factory() as connection:
            command.redo(connection)

        self.undo_manager.push_redo(command)
