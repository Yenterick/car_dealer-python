# Project imports
from model.command.Command import Command

from db.Sqlite3Connection import Sqlite3Connection

from model.dao.CustomerDAO import CustomerDAO
from model.vo.CustomerVO import CustomerVO

class DeleteCustomer(Command):

    def __init__(self,
                 customer: CustomerVO):
        self.customer = customer
        self.customer_id = None

    def redo(self, connection: Sqlite3Connection):
        self.customer_id = self.customer.customer_id
        CustomerDAO.delete_customer(self.customer_id)

    def undo(self, connection: Sqlite3Connection):
        CustomerDAO.reinsert_customer(
            connection,
            self.customer
        )
