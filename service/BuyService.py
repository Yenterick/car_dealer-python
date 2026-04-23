from typing import List

# Project imports
from db.Sqlite3Connection import Sqlite3Connection

from model.vo.BuyVO import BuyVO
from model.dao.BuyDAO import BuyDAO

from model.command.UndoRedoManager import UndoRedoManager
from model.command.buy.InsertBuy import InsertBuy
from model.command.buy.DeleteBuy import DeleteBuy

from ui.consoleUtils import log

class BuyService:

    def __init__(self, 
                 connection: Sqlite3Connection,
                 undo_manager: UndoRedoManager):
        self.connection = connection
        self.undo_manager = undo_manager

    def get_all_buys(self) -> List[BuyVO]:
        return BuyDAO.get_all_buys()
    
    def get_buy(self, buy_id: int) -> BuyVO | None:
        return BuyDAO.get_buy(buy_id)

    def select_all_supplier_buys(self, supplier_id: int) -> List[BuyVO] | None:
        return BuyDAO.select_all_supplier_buys(self.connection, supplier_id)

    def insert_buy(self, 
                   buy: BuyVO):
        command = InsertBuy(buy)

        with self.connection:
            command.redo(self.connection)

        self.undo_manager.register(command)

    def delete_buy(self,
                   buy: BuyVO) -> None:
        command = DeleteBuy(buy)

        with self.connection:
            command.redo(self.connection)

        self.undo_manager.push_redo(command)


