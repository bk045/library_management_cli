"""This is a main file where functions to request
user input and validation is created. Menu designe and
borrow operation, return operation, adding book,
registering customers are inititated in this file."""

from methodCollection import *
from datetime import datetime

# To clear screen.
def cls():  
    for i in range(50):
        print(" ")
         
# To display main menu.
def home():
    dashes ="-"*30
    labels = ("LIBRARY MANAGEMENT APPLICATION",
              "Add Books",
              "Register Customers",
              "Borrow Book",
              "Return Book",
              "Display Book Records",
              "Display Borrow Records",
              "Display Return Records",
              "Display Customer Records",
              "Exit")

    for i in range(len(labels)):
        if i == 0:
            print("{:^100}".format(dashes))
            print("{:^100}".format(labels[i]))
            print("{:^100}".format(dashes))
        else:
            print("{:>40} {}".format(str(i)+".", labels[i]))
    print("{:^100}".format(dashes))

# To ask for input with string value with no digits.
def askStringValue(statement):
    while True:
        print(statement)
        name = input(">")
        flag = True
        for char in name:
            if char.isdigit():
                flag = False
                break
        if flag:
            return name
        else:
            print("Invalid Input!!! Please include only (a-z, A-Z)!!!")

# To ask yes/no question and validate.
def askYesNoQuestion(statement):
    while True:
        print(statement)
        name = input(">")
        flag = True
        for char in name:
            if char.isdigit() or len(name) > 1:
                print("Invalid Input!!! Please answer with 'Y' or 'N'!!!")
                flag = False
                continue
        if flag:
            return name
# To ask for integer value only.
def askIntegerValue(statement):
    while True:
        print(statement)
        number = input(">")
        if number.isdigit():
            return int(number)
        else:
            print("Invalid Input!!! Please enter only whole numbers!!!")
            continue

# To ask for float value only.
def askFloatValue(statement):
    while True:
        print(statement)
        try:
            number = float(input(">"))
        except ValueError:
            print("Invalid Input!!! Please enter only numeric value!!!")
            continue
        else:
            return float(number)

# To perform borrow operation.
def borrowOperation():
    noOfBooks = 0
    while True:
        displayCustomerRecords()
        customerID = askIntegerValue("Enter Customer ID (DIGITS ONLY)*: ")
        cls()
        if custIDExists(customerID):
            while True:
                while True:
                    displayBookRecords()
                    bookID = askIntegerValue("Enter Book ID (DIGITS ONLY)*: ")
                    if bookIDExists(bookID):
                        currentQty = getQtyFor(bookID)
                        break
                    else:
                        cls()
                        print("Book ID: BOOK-" + str(bookID) +" does not exists!!!")
                        print("Please enter valid ID!!!")
                        continue
                if not currentQty < 1:
                    borrow_result = borrowBook(customerID, bookID)
                    if borrow_result:
                        noOfBooks += 1
                        saveDataTo("borrowList")
                        saveDataTo("bookList")
                        cls()
                        print(getBookNameFor(bookID) + " has been sucessfully borrowed by " + getCustomerNameFor(customerID) + " !!!")
                    answer = askYesNoQuestion("Would the same customer like to borrow more books?(Y/N)")
                    if answer.upper() == "Y":
                        cls()
                        print("Continue borrow with " + getCustomerNameFor(customerID) + "...")
                        print("No Of Books Borrowed so-far", noOfBooks)
                        continue
                    else:
                        cls()
                        print("Generating borrow note...")
                        input("Press ENTER to complete generating the note...")
                        displayBorrowNote(noOfBooks)
                        createBorrowNote(noOfBooks)
                        input("Press ENTER to return to main menu!!!")
                        cls()
                        break
                else:
                    print("Sorry!!! There are no more books to borrow for selected ID!!!")
                    answer = askYesNoQuestion("Would you like to add another book?(Y/N)")      
                    if answer.upper() == "Y":
                        cls()
                        continue
                    else:
                        if noOfBooks > 0:
                            cls()
                            print("Generating borrow note...")
                            input("Press ENTER to complete generating the note...")
                            displayBorrowNote(noOfBooks)
                            createBorrowNote(noOfBooks)
                            input("Press ENTER to return to main menu!!!")
                            cls()        
                break
            break
        else:
            print("Customer with CUST-" + str(customerID) +" does not exists!!!")
            print("Please enter valid ID!!!")
            continue

# To perform return operation.
def returnOperation():
    noOfBooks = 0
    while True:
        if leftToReturn():
            displayBorrowRecords()
            refIDNum = askIntegerValue("Enter Reference ID (DIGITS ONLY)*: ")
            if refIDExists(refIDNum):
                if statusIsActive(refIDNum):
                    return_result = returnBook(refIDNum)
                    if return_result:
                        saveDataTo("returnList")
                        saveDataTo("borrowList")
                        cls()
                        print("Book for REF-" + str(refIDNum) + " is sucessfully returned!!!")
                        noOfBooks += 1
                        answer = askYesNoQuestion("Would you like to return another book form the same borrow note?(Y/N)")
                        if answer.upper() == "Y":
                            cls()
                            continue
                        else:
                            cls()
                            print("Generating RETURN NOTE...")
                            input("Press ENTER to complete generating the note...")
                            displayReturnNote(noOfBooks)
                            createReturnNote(noOfBooks)
                            input("Press ENTER to return to main menu!!!")
                            break
                else:
                    cls()
                    print("Sorry!!! REF-" + str(refIDNum) + " is already returned!!!")
                    continue
            else:
                cls()
                displayBorrowRecords()
                print("")
                print("Sorry!!! REF-" + str(refIDNum) + " does not exists!!!")
                continue
        else:
            print("Sorry!!! There are no books left to return!!!")
            displayBorrowRecords()
            if noOfBooks > 0:
                print("Generating RETURN NOTE...")
                input("Press ENTER to complete generating the note...")
                cls()
                displayReturnNote(noOfBooks)
                createReturnNote(noOfBooks)
                input("Press ENTER to return to main menu!!!")
                break
            input("Press ENTER to return to main menu!!!")
            break

# To add customer.
def addCustomerOperation():
    while True:
        customerName = askStringValue("Enter Customer Name: ")
        phone = askIntegerValue("Enter Phone No: ")
        customer_result = addCustomer(customerName, phone)
        if customer_result:
            saveDataTo("customerList")
            cls()
            print(customerName.upper() + " has been sucessfully added!!!")
        answer = askYesNoQuestion("Would you like to add another record?(Y/N)")
        if answer.upper() == "N":
            break

# To add book.
def addBookOperation():
    while True:
        bookName = askStringValue("Enter Book Name: ")
        author = askStringValue("Enter Author: ")
        qty = askIntegerValue("Enter Quantity: ")
        price = askFloatValue("Enter Price: ")
        book_result = addBook(bookName, author, qty, price)
        if book_result:
            saveDataTo("bookList")
            cls()
            print(bookName.upper() + " has been sucessfully added!!!")
        answer = askYesNoQuestion("Would you like to add another record?(Y/N)")
        if answer.upper() == "N":
            break

# Block of code that starts program.
while True:
    home()
    print("")
    choice = askIntegerValue("Enter your choice:")
    if choice > 10 or choice < 1:
        print("Input out of range!!! Please enter number between 1-9!!!")
        continue
    elif choice == 1:
        cls()
        print("You have selected to ADD BOOK!!!\n")
        addBookOperation()
        cls()
        continue
    elif choice == 2:
        cls()
        print("You have selected REGISTER CUSTOMER!!!\n")
        addCustomerOperation()
        cls()
        continue
    elif choice == 3:
        cls()
        print("You have selected to BORROW BOOK!!!\n")
        if not len(customers) == 0:
            if not len(books) == 0:
                borrowOperation()
            else:
                print("Sorry!!! There are no books!!!")
                input("Press ENTER to ADD NEW BOOK!!!")
                addBookOperation()
        else:
            print("Sorry!!! There are no customers to lend!!!")
            input("Press ENTER to REGISTER CUSTOMER!!!")
            addCustomerOperation()
        continue
    elif choice == 4:
        cls()
        print("You have selected to RETURN BOOK")
        if not len(borrows) == 0:
            returnOperation()
            cls()
        else:
            print("Sorry!!! There are no books borrowed so-far!!!")
            input("Press ENTER to return to main menu!!!")
        continue
    elif choice == 5:
        cls()
        displayBookRecords()
        input("Press ENTER to continue ...")
        cls()
        continue
    elif choice == 6:
        cls()
        displayBorrowRecords()
        input("Press ENTER to continue ...")
        cls()
        continue
    elif choice == 7:
        cls()
        displayReturnRecords()
        input("Press ENTER to continue ...")
        cls()
        continue
    elif choice == 8:
        cls()
        displayCustomerRecords()
        input("Press ENTER to continue ...")
        cls()
        continue
    else:
        cls()
        print("Program terminated!!!")
        break

