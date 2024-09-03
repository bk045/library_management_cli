"""This file consists of Book, Return, Borrow and Customer class.
They are used to create respective objects"""

class Book():
    def __init__(self, bookID:str, name:str, author:str, qty:int, price:float):
        self.bookID = bookID
        self.name = name.upper()
        self.author = author.upper()
        self.qty = int(qty)
        self.price = float(price)

    def getID(self):
        return self.bookID

    def getName(self):
        return self.name

    def getAuthor(self):
        return self.author

    def getQty(self):
        return self.qty

    def getPrice(self):
        return self.price

    def setQty(self, qty):
        self.qty = qty

    def setPrice(self, price:float):
        self.price = float(price)

    def setName(self, name:str):
        self.name = str(name).upper()

    def setAuthor(self, author:str):
        self.author = str(author).upper()

class Borrow():
    def __init__(self, refID:str, date, customerID:str, bookID:str, status:str, qty:int):
        self.refID = refID
        self.date = date
        self.customerID = customerID
        self.bookID = bookID
        self.qty = int(qty)
        self.status = status.upper()

    def getRefID(self):
        return self.refID

    def getDate(self):
        return self.date
    
    def getBookID(self):
        return self.bookID

    def getCustomerID(self):
        return self.customerID

    def getQty(self):
        return self.qty

    def getStatus(self):
        return self.status

    def setQty(self, qty:int):
        self.qty = int(qty)

    def setReturned(self):
        self.status = "RETURNED"


class Return():
    def __init__(self, refID:str, date, customerID:str, bookID:str, qty:int, status:str):
        self.refID = refID
        self.date = date
        self.customerID = customerID
        self.bookID = bookID
        self.qty = int(qty)
        self.status = str(status).upper()

    def getRefID(self):
        return self.refID

    def getDate(self):
        return self.date
    
    def getBookID(self):
        return self.bookID

    def getCustomerID(self):
        return self.customerID

    def getQty(self):
        return self.qty

    def getStatus(self):
        return self.status

    def setQty(self, qty:int):
        self.qty = int(qty)

class Customer():
    def __init__(self, customerID:str, name:str, phone:int):
        self.customerID = customerID
        self.name = name.upper()
        self.phone = int(phone)

    def getID(self):
        return self.customerID

    def getName(self):
        return self.name

    def getPhone(self):
        return self.phone

