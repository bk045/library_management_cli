"""This file is a collection of all the methods
responsible for reading data from files,
writing data to files,
display of records,
checking status and calculating date and time.
These methods work for back-end operaitons."""


from datetime import date, datetime, timedelta
from classCollection import Book
from classCollection import Return
from classCollection import Borrow
from classCollection import Customer
import sys
#import os

# To return borrow and return path according to the OS.
def getPath(osName, fileName):
    if osName == "darwin" or osName == "linux" or osName == "linux1" or osName == "linux2":
        borrowPath = "../borrows/" + fileName
        returnPath = "../returns/" + fileName
    elif osName == "win32":
        borrowPath = "..\\borrows\\" + fileName
        returnPath = "..\\returns\\" + fileName
    else:
        return []
    return [borrowPath, returnPath]

# To read lines from files and return in the form of list. 
def getRecordsFromFiles(fileName):
    fileName = fileName + ".txt"
    with open(fileName) as fileObj:
        lines = fileObj.readlines()
    return lines

# To convert datetime object into user friendly format.
def getFormatedDateTime(dateObj):
    return dateObj.strftime("%a, %d %b, %Y, %X")

# To get expected return date with respect to borrow date.
def getReturnDateTime(borrowDate):
    return (borrowDate + timedelta(days = 10))

# To check if the transaction is applicable for fine.
def applicableForFine(borrowDate):
    today = datetime.now()
    dateToReturn = getReturnDateTime(borrowDate)
    if today > dateToReturn:
        return True
    else:
        return False

# To calculate extra days applicable for fine.
def calculateExtraDays(borrowDate):
    today = datetime.now()
    dateToReturn = getReturnDateTime(borrowDate)
    if today > dateToReturn:
        excessDays = today - dateToReturn
        index = 0
        for char in str(excessDays):
            if not char == " ":
                index += 1
            else:
                break
        excessDaysStr = str(excessDays)[0:index]
        return int(excessDaysStr)
    else:
        return 0
# To calculate fine for extra days.
def calculateFine(borrowDate):
    fine = float(calculateExtraDays(borrowDate) * 1)
    return fine

# To extract numeric value of Year, from record, featched from text file.
# Used later to create datetime object.
def getYear(dateList):
    splited = dateList.split(" ")
    return int(splited[1])

# To extract numeric value of Month, from record, featched from text file.
# Used later to create datetime object.
def getMonth(dateList):
    months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
    splited = dateList.split(" ")
    for key, value in months.items():
        if key == splited[2]:
            return value
            
# To extract numeric value of Day, from record, featched from text file.
# Used later to create datetime object.
def getDay(dateList):
    splited = dateList.split(" ")
    return int(splited[1])

# To extract numeric value of Hour, from record, featched from text file.
# Used later to create datetime object.
def getHour(dateList):
    hour = ""
    splited = dateList.split(":")
    for char in splited[0]:
        if not char == " ":
            hour = hour + char
    return int(hour)

# To extract numeric value of Minute, from record, featched from text file.
# Used later to create datetime object.
def getMinute(dateList):
    splited = dateList.split(":")
    return int(splited[1])

# To extract numeric value of Second, from record, featched from text file.
# Used later to create datetime object.
def getSecond(dateList):
    splited = dateList.split(":")
    return int(splited[2])

# To create Book objects with the help of records extracted as a list from text file named bookList.txt.
def fetchBookRecords():
    books = []
    if not (len(getRecordsFromFiles("bookList")) == 0):
        bookRecords = getRecordsFromFiles("bookList")
        for record in bookRecords:
            fields = record.split("~");
            books.append(Book(fields[0], fields[1], fields[2], int(fields[3]), float(fields[4])))
        return books
    else:
        return books

# Creating list of Book objects.
books = fetchBookRecords()

# To create Customer objects with the help of records extracted as a list from text file named customerList.txt.
def fetchCustomerRecords():
    customers = []
    if not (len(getRecordsFromFiles("customerList")) == 0):
        customerRecords = getRecordsFromFiles("customerList")
        for record in customerRecords:
            fields = record.split("~")
            customers.append(Customer(fields[0], fields[1], int(fields[2])))
        return customers
    else:
        return customers

# Creating list of Customer objects.
customers = fetchCustomerRecords()

# To create Return objects with the help of records extracted as a list from text file named returnList.txt.
def fetchReturnRecords():
    returns = []
    if not (len(getRecordsFromFiles("returnList")) == 0):
        returnRecords = getRecordsFromFiles("returnList")
        for record in returnRecords:
            fields = record.split("~")
            dateList = fields[1].split(",")
            dateObj = datetime(getYear(dateList[2]), getMonth(dateList[1]), getDay(dateList[1]), getHour(dateList[3]), getMinute(dateList[3]), getSecond(dateList[3]), 0)
            returns.append(Return(fields[0], dateObj, fields[2], fields[3], int(fields[4]), "RETURNED"))
        return returns
    else:
        return returns

# Creating list of Return objects.
returns = fetchReturnRecords()

# To create Borrow objects with the help of records extracted as a list from text file named borrowList.txt.
def fetchBorrowRecords():
    borrows = []
    if not (len(getRecordsFromFiles("borrowList")) == 0):
        borrowRecords = getRecordsFromFiles("borrowList")
        for record in borrowRecords:
            fields = record.split("~")
            dateList = fields[1].split(",")
            dateObj = datetime(getYear(dateList[2]), getMonth(dateList[1]), getDay(dateList[1]), getHour(dateList[3]), getMinute(dateList[3]), getSecond(dateList[3]), 0)
            borrows.append(Borrow(fields[0], dateObj, fields[2], fields[3], fields[4], int(fields[5])))
        return borrows
    else:
        return borrows

# Creating list of Borrow objects.
borrows = fetchBorrowRecords()

# To extract respective records as a list, from collection of objects based on file name supplied.
def getRecordsFromList(fileName):
    recordList = []
    line = ""
    if fileName == "bookList":
        for bookRec in books:
            bookID = bookRec.getID()
            name = bookRec.getName()
            author = bookRec.getAuthor()
            qty = str(bookRec.getQty())
            price = str(bookRec.getPrice())
            line = bookID + "~" + name + "~" + author + "~" + qty + "~" + price + "\n"
            recordList.append(line)
        return recordList
    if fileName == "borrowList":
        for borrowRec in borrows:
            refID = borrowRec.getRefID()
            date = getFormatedDateTime(borrowRec.getDate())
            customerID = borrowRec.getCustomerID()
            bookID = borrowRec.getBookID()
            qty = str(borrowRec.getQty())
            status = borrowRec.getStatus()
            line = refID + "~" + date + "~" + customerID + "~" + bookID + "~" + status + "~" + qty + "\n"
            recordList.append(line)
        return recordList
    if fileName == "returnList":
        for returnRec in returns:
            refID = returnRec.getRefID()
            date = getFormatedDateTime(returnRec.getDate())
            customerID = returnRec.getCustomerID()
            bookID = returnRec.getBookID()
            qty = str(returnRec.getQty())
            line = refID + "~" + date + "~" + customerID + "~" + bookID + "~" + qty + "\n"
            recordList.append(line)
        return recordList
    if fileName == "customerList":
        for customerRec in customers:
            customerID = customerRec.getID()
            name = customerRec.getName()
            phone = str(customerRec.getPhone())
            line = customerID + "~" + name + "~" + phone + "\n"
            recordList.append(line)
        return recordList

# To display book records on the terminal.
def displayBookRecords():
    dashes = "-"*80
    print (dashes)
    print('{:*^80}'.format(" BOOK STOCK "))
    print (dashes)
    print ('{:<10s} {:<30s} {:<15s} {:^10s} {:>8s}'.format('Book ID','Name of the Book','Author', 'Quantity', 'Price'))
    print (dashes)
    if not len(books) == 0: 
        for book in books:
            print ('{:<10s} {:<30s} {:<15s} {:^10s} {:>8s}'.format(book.getID(),
                                                                   book.getName(),
                                                                   book.getAuthor(),
                                                                   str(book.getQty()),
                                                                   "$"+str(book.getPrice())))
    else:
        print("Sorry!!! There are no BOOK RECORDS to display!!!")
    print (dashes)

# To display return records on the terminal.
def displayReturnRecords():
    dashes = "-"*72
    print (dashes)
    print('{:*^72}'.format(" RETURN RECORDS "))
    print (dashes)
    print ('{:<10s} {:^25s} {:^12s} {:^10s}'.format('Refrence ID',
                                                           'Date of Return',
                                                           'Customer ID',
                                                           'Book ID'))
    print (dashes)
    if not len(returns) == 0:
        for returnRec in returns:
            print ('{:<10s} {:^25s} {:^12s} {:^10s}'.format(returnRec.getRefID(),
                                                                   getFormatedDateTime(returnRec.getDate()),
                                                                   returnRec.getCustomerID(),
                                                                   returnRec.getBookID()))
    else:
        print("Sorry!!! There are no RETURN RECORDS to display!!!")
    print (dashes)

# To display customer records on the terminal.
def displayCustomerRecords():
    dashes = "-"*52
    print (dashes)
    print('{:*^52}'.format(" CUSTOMER RECORDS "))
    print (dashes)
    print ('{:<10s} {:^25s} {:^12s}'.format('Customer ID',
                                            'Full Name',
                                            'Phone Number'))
    print (dashes)
    if not len(customers) == 0:
        for customerRec in customers:
            print ('{:<10s} {:^25s} {:^12s}'.format(customerRec.getID(),
                                                    customerRec.getName(),
                                                    str(customerRec.getPhone())))
    else:
        print("Sorry!!! There are no CUSTOMER RECORDS to display!!!")
    print (dashes)

# To display borrow records on the terminal.
def displayBorrowRecords():
    dashes = "-"*90
    print (dashes)
    print('{:*^90}'.format(" BORROW RECORDS "))
    print (dashes)
    print ('{:<10s} {:^25s}   {:^12s} {:^10s} {:^13s}'.format('Refrence ID',
                                                           'Date of Borrow',
                                                           'Customer ID',
                                                           'Book ID',
                                                           'Status'))
    print (dashes)
    if not len(borrows) == 0:
        for borrowRec in borrows:
            print ('{:<10s} {:^25s} {:^12s} {:^10s} {:^15s}'.format(borrowRec.getRefID(),
                                                                   getFormatedDateTime(borrowRec.getDate()),
                                                                   borrowRec.getCustomerID(),
                                                                   borrowRec.getBookID(),
                                                                   borrowRec.getStatus()))
    else:
        print("Sorry!!! There are no BORROW RECORDS to display!!!")        
    print (dashes)


# To generate next reference ID based on last record reference ID.
def nextRefID():
    if not len(borrows) == 0:
        lastIndex = len(borrows) - 1
        borrowRecord = borrows[lastIndex]
        refID = borrowRecord.getRefID()
        refIDList = refID.split("-")
        number = int(refIDList[1]) + 1
        return "REF-" + str(number)
    else:
        return "REF-1"

# To generate next book ID based on last record book ID.
def nextBookID():
    if not len(books) == 0:
        lastIndex = len(books) - 1
        bookRecord = books[lastIndex]
        bookID = bookRecord.getID()
        bookIDList = bookID.split("-")
        number = int(bookIDList[1]) + 1
        return "BOOK-" + str(number)
    else:
        return "BOOK-1"

# To generate next customer ID based on last record customer ID.
def nextCustomerID():
    if not len(customers) == 0:
        lastIndex = len(customers) - 1
        customerRecord = customers[lastIndex]
        customerID = customerRecord.getID()
        customerIDList = customerID.split("-")
        number = int(customerIDList[1]) + 1
        return "CUST-" + str(number)
    else:
        return "CUST-1"

# To check if reference ID exists in any borrow records.
def refIDExists(refIDNum):
    refID = "REF-" + str(refIDNum)
    for borrowRec in borrows:
        if refID == borrowRec.getRefID():
            return True
    return False

# To check if book ID exists in any book records.
def bookIDExists(bookIDNum:int):
    bookID = "BOOK-" + str(bookIDNum)
    for bookRec in books:
        if bookID == bookRec.getID():
            return True
    return False

# To check if customer ID exists in any customer records.
def custIDExists(custIDNum:int):
    customerID = "CUST-" + str(custIDNum)
    for customersRec in customers:
        if customerID == customersRec.getID():
            return True
    return False

# To perform borrow action and append Borrow object to the respective list.        
def borrowBook(customerIDNum:int, bookIDNum:int):
    refID = nextRefID()
    today = datetime.now()
    customerID = "CUST-" + str(customerIDNum)
    bookID = "BOOK-" + str(bookIDNum)
    for book in books:
        if bookID == book.getID():
            presentQty = book.getQty() 
            book.setQty(presentQty - 1)
            borrows.append(Borrow(refID, today, customerID, bookID, "ACTIVE", 1))
            return True
    return False

# To perform return action and append Return object to the respective list.
def returnBook(refIDNum:int):
    refID = "REF-" + str(refIDNum)
    for borrowRec in borrows:
        if refID == borrowRec.getRefID():
            customerID = borrowRec.getCustomerID()
            bookID = borrowRec.getBookID()
            today = datetime.now()
            for book in books:
                if bookID == book.getID():
                    previousQty = book.getQty()
                    book.setQty(previousQty + 1)
                    returns.append(Return(refID, today, customerID, bookID, 1, "RETURNED"))
                    borrowRec.setReturned()
                    return True
    return False

# To add book and append Book object to the respective list.
def addBook(name:str, author:str, qty:int, price:float):
    books.append(Book(nextBookID(), name, author, qty, price))
    return True

# To add customer and append Customer object to the respective list.
def addCustomer(name:str, phone:int):
    customers.append(Customer(nextCustomerID(), name, phone))
    return True

# To get quantity of particular book form books stock.    
def getQtyFor(bookIDNum:int):
    bookID = "BOOK-" + str(bookIDNum)
    for bookRec in books:
        if bookRec.getID() == bookID:
            return bookRec.getQty()

# To get borrow price for particular book form books stock.
def getPriceFor(bookIDNum:int):
    bookID = "BOOK-" + str(bookIDNum)
    for bookRec in books:
        if bookRec.getID() == bookID:
            return bookRec.getPrice()

# To get book name for particular book form books stock.       
def getBookNameFor(bookIDNum:int):
    bookID = "BOOK-" + str(bookIDNum)
    for bookRec in books:
        if bookRec.getID() == bookID:
            return bookRec.getName()

# To get customer name for particular customer form customer record.
def getCustomerNameFor(customerIDNum:int):
    customerID = "CUST-" + str(customerIDNum)
    for customerRec in customers:
        if customerRec.getID() == customerID:
            return customerRec.getName()

# To get date of borrow for particular transaction form borrow record.        
def getBorrowDate(refIDNum):
    refID = "REF-" + str(refIDNum)
    for borrowRec in borrows:
        if refID == borrowRec.getRefID():
            return borrowRec.getDate()

# To get date of return for particular transaction form return record.
def getReturnDate(refIDNum):
    refID = "REF-" + str(refIDNum)
    for returnRec in returns:
        if refID == returnRec.getRefID():
            return returnRec.getDate()

# To save data from list to txt file.
def saveDataTo(fileName):
    records = getRecordsFromList(fileName)
    fileName = fileName + ".txt"
    with open(fileName, 'w') as fileObj:
        for record in records:
            fileObj.writelines(record)

# To check if a borrowed book is returned.
def statusIsActive(refIDNum:int):
    refID = "REF-" + str(refIDNum)
    for borrowRec in borrows:
        if borrowRec.getRefID() == refID and borrowRec.getStatus() == "ACTIVE":
            return True
    return False

# To check if any borrow transactions are left to return.
def leftToReturn():
    for borrowRec in borrows:
        if borrowRec.getStatus() == "ACTIVE":
            return True
    return False

# To generate list with return records applicable for return note. 
def getReturnNoteRecord(noOfBooks):
    returnRecords = []
    for i in range(len(returns), len(returns) - noOfBooks, -1):
        returnRecords.append(returns[i-1])
    return returnRecords

# To generate list with borrow records applicable for borrow note.
def getBorrowNoteRecord(noOfBooks):
    borrowRecords = []
    for i in range(len(borrows), len(borrows) - noOfBooks, -1):
        borrowRecords.append(borrows[i-1])
    return borrowRecords

# To create borrow note (file), containing borrow record applicable for borrow note.
def createBorrowNote(noOfBooks):
    records = getBorrowNoteRecord(noOfBooks)
    customerID = records[0].getCustomerID()
    customerName = getCustomerNameFor(int(customerID[5:]))
    borrowDate = records[0].getDate()
    # HEAD: Preparing upper part of the note including heading, customer and borrow details.
    fName = "BN-" + str(datetime.now()) + "-" + customerName + ".txt"
    dashes = "-"*80 + "\n"
    spaces = "           "
    headingSpaces = "                                      "
    heading = headingSpaces + "BORROW NOTE" + "\n"
    firstInfo = "Customer ID: " + customerID + "\n"
    secondInfo = "Customer Name: " + customerName + "\n"
    borrowInfo = "Date of Borrow: " + getFormatedDateTime(borrowDate) + "\n"
    returnInfo = "Date to Return: " + getFormatedDateTime(getReturnDateTime(borrowDate)) + "\n"
    dataList = []
    dataList.append(dashes)
    dataList.append(heading)
    dataList.append(dashes)
    dataList.append(firstInfo)
    dataList.append(secondInfo)
    dataList.append(borrowInfo)
    dataList.append(returnInfo)
    dataList.append(dashes)
    # BODY: Extracting data from each borrow record, creating lines and appending to list.
    totalPrice = 0
    for record in records:
        bookID = record.getBookID()
        bookIDNum = int(bookID[5:])
        dataItem = record.getRefID() + spaces + getBookNameFor(bookIDNum) + spaces + bookID + spaces + str(record.getQty()) + spaces + "$" + str(getPriceFor(bookIDNum)) + "\n"
        dataList.append(dataItem)
        totalPrice += getPriceFor(bookIDNum)
    # FOOT: Positioning calculated total price and note on the footer.
    price = "Total Price: $" + str(totalPrice) + "\n"
    note = "NOTE: Fine of $1.0 per book shall apply for every extra day!!!" + "\n"
    dataList.append(dashes)
    dataList.append(price)
    dataList.append(dashes)
    dataList.append(note)
    dataList.append(dashes)
    # Wrinting lines into a new file using list.
    borrowPath = getPath(sys.platform, fName)[0]
    with open(borrowPath, "w") as fileObj:
        for line in dataList:
            fileObj.write(line)
        return True

# To create return note (file), containing return record applicable for return note.
def createReturnNote(noOfBooks):
    records = getReturnNoteRecord(noOfBooks)
    refID = records[0].getRefID()
    refIDNum = int(refID[4:])
    customerID = records[0].getCustomerID()
    customerName = getCustomerNameFor(int(customerID[5:]))
    returnDate = records[0].getDate()
    borrowDate = getBorrowDate(refIDNum)
    # HEAD: Preparing upper part of the note including heading, customer, borrow and return details.
    fName = "RN-" + str(datetime.now()) + "-" + customerName + ".txt"
    dashes = "-"*92 + "\n"
    spaces = "          "
    headingSpaces = "                                             "
    heading = headingSpaces + "RETURN NOTE" + "\n"
    firstInfo = "Customer ID: " + customerID + "\n"
    secondInfo = "Customer Name: " + customerName + "\n"
    borrowInfo = "Date of Borrow: " + getFormatedDateTime(borrowDate) + "\n"
    returnInfo = "Date of Return: " + getFormatedDateTime(returnDate) + "\n"
    expectedInfo = "Date to Return: " + getFormatedDateTime(getReturnDateTime(borrowDate)) + "\n"
    dataList = []
    dataList.append(dashes)
    dataList.append(heading)
    dataList.append(dashes)
    dataList.append(firstInfo)
    dataList.append(secondInfo)
    dataList.append(borrowInfo)
    dataList.append(returnInfo)
    dataList.append(expectedInfo)
    dataList.append(dashes)
    # BODY: Extracting data from each return record, creating lines and appending to list.
    totalPrice = 0
    basePrice = 0
    fine = 0
    for record in records:
        bookID = record.getBookID()
        bookIDNum = int(bookID[5:])
        dataItem = record.getRefID() + spaces + getBookNameFor(bookIDNum) + spaces + bookID + spaces + "$" + str(getPriceFor(bookIDNum)) + spaces + str(calculateExtraDays(borrowDate)) +  spaces + "$" + str(calculateFine(borrowDate)) + "\n"
        dataList.append(dataItem)
        basePrice += getPriceFor(bookIDNum)
        fine += calculateFine(borrowDate)
    totalPrice = float(basePrice + fine)
    # FOOT: Positioning calculated total price and note on the footer.
    price = "Total Price: $" + str(totalPrice) + "\n"
    note = "NOTE: Total fine of $" + str(fine) + " has been applied for extra day(s)!!!" + "\n"
    dataList.append(dashes)
    dataList.append(price)
    dataList.append(dashes)
    if applicableForFine(borrowDate):
        dataList.append(note)
        dataList.append(dashes)
    # Wrinting lines into a new file using list.
    returnPath = getPath(sys.platform, fName)[1]
    with open(returnPath, "w") as fileObj:
        for line in dataList:
            fileObj.write(line)
        return True

# To display borrow note on terminal.
def displayBorrowNote(noOfBooks):
    records = getBorrowNoteRecord(noOfBooks)
    customerID = records[0].getCustomerID()
    customerName = getCustomerNameFor(int(customerID[5:]))
    borrowDate = records[0].getDate()
    # HEAD:                                  
    dashes = "-"*75
    print(dashes)
    print('{:*^75}'.format(" BORROW NOTE "))
    print (dashes)
    print()
    print ('{:<30s} {:>20s}'.format("Customer ID: " + customerID, "Date(Borrowed): " + getFormatedDateTime(borrowDate)))
    print ('{:<30s} {:>20s}'.format("Name: " + customerName, "Date(To Return): " + getFormatedDateTime(getReturnDateTime(borrowDate))))
    print (dashes)
    # BODY:
    if not len(records) == 0:
        print ('{:<10s} {:^25s} {:^12s} {:^10s} {:^15s}'.format("Reference ID", "Name of the Book", "Book ID", "Quantity", "Price"))
        print (dashes)
        totalPrice = 0
        for record in records:
            bookID = record.getBookID()
            bookIDNum = int(bookID[5:])
            print ('{:<10s} {:^25s}  {:^12s} {:^10s}  {:^15s}'.format(record.getRefID(),
                                                                    getBookNameFor(bookIDNum),
                                                                    bookID,
                                                                    str(record.getQty()),
                                                                    "$" + str(getPriceFor(bookIDNum))))
            totalPrice += getPriceFor(bookIDNum)
        # FOOT:
        print(dashes)
        print('{:<53s} {:>15s}'.format(" ", "Total Price:  $" + str(totalPrice)))
        print(dashes)
        print("NOTE: Fine of $1.0 per book shall apply for every extra day!!!")
        print(dashes)
    else:
        print("Sorry!!! There are no BORROW NOTES to display!!!")        
        print (dashes)


# To display return note on terminal.
def displayReturnNote(noOfBooks:int):
    records = getReturnNoteRecord(noOfBooks)
    refID = records[0].getRefID()
    refIDNum = int(refID[4:])
    customerID = records[0].getCustomerID()
    customerName = getCustomerNameFor(int(customerID[5:]))
    returnDate = records[0].getDate()
    borrowDate = getBorrowDate(refIDNum)                           
    # HEAD:
    dashes = "-"*90
    print(dashes)
    print('{:*^90}'.format(" RETURN NOTE "))
    print (dashes)
    print ('{:<40s} {:>30s}'.format("Customer ID: " + customerID, "Date(Borrowed): " + getFormatedDateTime(borrowDate)))
    print ('{:<40s} {:>30s}'.format("Name: " + customerName, "Date(Returned): " + getFormatedDateTime(returnDate)))
    print (dashes)
    # BODY:
    if not len(records) == 0:
        print ('{:<10s} {:^25s} {:^12s} {:^10s} {:^15s} {:^15s}'.format("Reference ID", "Name of the Book", "Book ID", "Price", "Extra Days", "Fine"))
        print (dashes)
        bookPrice = 0
        fine = 0.0
        for record in records:
            bookID = record.getBookID()
            bookIDNum = int(bookID[5:])
            print ('{:<10s} {:^25s}  {:^12s} {:^10s}  {:^15s} {:^15s}'.format(record.getRefID(),
                                                                    getBookNameFor(bookIDNum),
                                                                    bookID,
                                                                    "$" + str(getPriceFor(bookIDNum)),
                                                                    str(calculateExtraDays(borrowDate)),
                                                                    "$" + str(calculateFine(borrowDate))))
            bookPrice += getPriceFor(bookIDNum)
            fine += calculateFine(borrowDate)
        totalPrice = bookPrice + fine
        # FOOT:
        print(dashes)
        print('{:<69s} {:>15s}'.format(" ", "Total Price:  $" + str(totalPrice)))
        print(dashes)

        if applicableForFine(borrowDate):
            print("NOTE: Total fine of $" + str(fine) + " has been applied for extra day(s)!!!")
            print(dashes)
    else:
        print("Sorry!!! There are no RETURN NOTES to display!!!")        
        print (dashes)


