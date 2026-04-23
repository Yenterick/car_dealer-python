# Project imports
from model.command.Command import Command

from db.Sqlite3Connection import Sqlite3Connection

from model.dao.SaleDAO import SaleDAO
from model.vo.SaleVO import SaleVO

class DeleteSale(Command):

    def __init__(self,
                 sale: SaleVO):
        self.sale = sale
        self.sale_id = None

    def redo(self, connection: Sqlite3Connection):
        self.sale_id = self.sale.sale_id
        SaleDAO.delete_sale(self.sale_id)

    def undo(self, connection: Sqlite3Connection):
        SaleDAO.reinsert_sale(
            connection,
            self.sale
        )
