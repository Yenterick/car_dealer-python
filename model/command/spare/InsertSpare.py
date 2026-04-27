# Project imports
from model.command.Command import Command

from db.Sqlite3Connection import Sqlite3Connection

from model.dao.SpareDAO import SpareDAO
from model.vo.SpareVO import SpareVO

class InsertSpare(Command):

    def __init__(self,
                 spare: SpareVO):
        self.spare = spare
        self.spare_id = None

    def redo(self, connection: Sqlite3Connection):
        # Validating if is the first time we're adding the spare
        if self.spare_id is None:
            self.spare_id = SpareDAO.insert_spare(
                connection,
                self.spare
            )
            # Update the VO with the new ID
            self.spare.spare_id = self.spare_id
        else:
            # We're reinserting the spare
            SpareDAO.reinsert_spare(
                connection,
                self.spare
            )

    def undo(self, connection: Sqlite3Connection):
        SpareDAO.delete_spare(
            self.spare_id
        )
