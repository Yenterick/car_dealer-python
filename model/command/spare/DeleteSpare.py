# Project imports
from model.command.Command import Command

from db.Sqlite3Connection import Sqlite3Connection

from model.dao.SpareDAO import SpareDAO
from model.vo.SpareVO import SpareVO

class DeleteSpare(Command):

    def __init__(self,
                 spare: SpareVO):
        self.spare = spare
        self.spare_id = None

    def redo(self, connection: Sqlite3Connection):
        self.spare_id = self.spare.spare_id
        SpareDAO.delete_spare(self.spare_id)

    def undo(self, connection: Sqlite3Connection):
        SpareDAO.reinsert_spare(
            connection,
            self.spare
        )
