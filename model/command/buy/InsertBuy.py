# Project imports
from model.command.Command import Command

from db.Sqlite3Connection import Sqlite3Connection

from model.dao.BuyDAO import BuyDAO
from model.vo.BuyVO import BuyVO

class InsertBuy(Command):

    def __init__(self,
                 buy: BuyVO):
        self.buy = buy
        self.buy_id = None

    def redo(self, connection: Sqlite3Connection):
        # Validating if is the first time we're adding the buy
        if self.buy_id is None:
            self.buy_id = BuyDAO.insert_buy(
                connection,
                self.buy
            )
        else:
            # We're reinserting the buy
            BuyDAO.reinsert_buy(
                connection,
                self.buy
            )

    def undo(self, connection: Sqlite3Connection):
        BuyDAO.delete_buy(
            self.buy_id
        )
