# Project imports
from model.command.Command import Command

from db.Sqlite3Connection import Sqlite3Connection

from model.dao.CustomerDAO import CustomerDAO
from model.vo.CustomerVO import CustomerVO

class InsertCustomer(Command):

    def __init__(self,
                 customer: CustomerVO):
        self.customer = customer
        self.customer_id = None

    def redo(self, connection: Sqlite3Connection):
        # Validating if is the first time we're adding the customer
        if self.customer_id is None:
            self.customer_id = CustomerDAO.insert_customer(
                connection,
                self.customer
            )
            # Update the VO with the new ID
            self.customer.customer_id = self.customer_id
        else:
            # We're reinserting the customer
            CustomerDAO.reinsert_customer(
                connection,
                self.customer
            )

    def undo(self, connection: Sqlite3Connection):
        CustomerDAO.delete_customer(
            self.customer_id
        )
