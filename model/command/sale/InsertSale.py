# Project imports
from model.command.Command import Command

from db.Sqlite3Connection import Sqlite3Connection

from model.dao.SaleDAO import SaleDAO
from model.vo.SaleVO import SaleVO

class InsertSale(Command):

    def __init__(self,
                 sale: SaleVO):
        self.sale = sale
        self.sale_id = None

    def redo(self, connection: Sqlite3Connection):
        # Validating if is the first time we're adding the sale
        if self.sale_id is None:
            self.sale_id = SaleDAO.insert_sale(
                connection,
                self.sale
            )
        else:
            # We're reinserting the sale
            SaleDAO.reinsert_sale(
                connection,
                self.sale
            )

    def undo(self, connection: Sqlite3Connection):
        SaleDAO.delete_sale(
            self.sale_id
        )
