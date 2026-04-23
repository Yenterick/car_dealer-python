# Project imports
from model.command.Command import Command

from db.Sqlite3Connection import Sqlite3Connection

from model.dao.BuyDAO import BuyDAO
from model.vo.BuyVO import BuyVO

class DeleteBuy(Command):

    def __init__(self,
                 buy: BuyVO):
        self.buy = buy
        self.buy_id = None

    def redo(self, connection: Sqlite3Connection):
        self.buy_id = self.buy.buy_id
        BuyDAO.delete_buy(self.buy_id)

    def undo(self, connection: Sqlite3Connection):
        BuyDAO.reinsert_buy(
            connection,
            self.buy
        )
