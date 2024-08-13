import tkinter as tk
import json
try:
    from GUI_app import FinanceTrackerGUI
except ImportError: # Making sure the program doesn't crash if GUI_app python file dosen't contains FinanceTrackerGUI
    print("\nGUI file is missing!")

# Global dictionary to store transactions
transactions = {}

# Global lists to sort transactions
income_categories = []
expense_categories = []

# This function is to get a valid number input value it can be either float or integer
def num_input(num_type, message, error_message):
    while True:
        try:
            number = num_type(input(message))
        except ValueError:
            print(error_message)
        else:
            if number < 0:
                print(error_message)
                continue
            else:
                return number

# This function is to check if the input for category of the transaction is valid
def valid_category():
    while True:
        category = input(
            "\nEnter the category of the transaction : ").capitalize()  # Capitalizing the category to maintain in a proper format
        if not category:
            print("You cannot leave category empty!")
            continue
        else:
            return category

# This function is to check if the input for the type of the transaction is valid
def valid_type(category):
    while True:
        get_transaction_type()
        print("\nIf the transaction is income transaction - I")  # To print data to the user
        print("If the transaction is expense transaction - E")
        transactions_type = input("Enter the type of the transaction(I or E) : ").upper()
        if transactions_type not in ("I", "E"):
            print("Invalid input for transaction type (I or E)")

        # If the input category is already there in the records and the user is trying to give the opposite transaction_type
        elif category in income_categories and transactions_type == "E":
            print(f"\n{category} is Income type.")
            print("\nIf the transaction type is wrong - Update the transaction type after completing the entry! ")
            return "I"

        elif category in expense_categories and transactions_type == "I":
            print(f"\n{category} is Expense type.")
            print("\nIf the transaction type is wrong - Update the transaction type after completing the entry!  ")
            return "E"

        else:  # Checking if the input category is already in the temporary file and not in the records, and the user is trying to change the type
            local_transactions = read_file("temp_transactions.txt", [])
            if local_transactions is not None:
                for transaction in local_transactions:
                    if category == transaction[1] and transactions_type != transaction[2]:
                        print(f"\n{category} is opposite transaction type.")
                        print(
                            "\nIf the transaction type is wrong - Update the transaction type after completing the entry!  ")
                        if transactions_type == "I":
                            return "E"
                        else:
                            return "I"
                else:
                    return transactions_type
            else:
                return transactions_type

# Date validation functions
def valid_year():
    while True:
        leap_check = False  # This variable will be used to check if the given year is leap year
        year = num_input(int, "\nPlease enter the year in which the transaction occurred : ", "Invalid year!")

        # Checking if the year is leap year
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            leap_check = True

        # The function is to control date year to be within 2000 and 2024
        if year < 2000 or year > 2024:
            print("Invalid year!")

        else:
            return year, leap_check

# This is to get valid month input
def valid_month():
    while True:
        month = num_input(int, "\nPlease enter the month in which the transaction occurred : ", "Invalid month!")

        if month > 12:  # to ensure there is no more than 12 months
            print("Invalid month!")
        else:
            return month

def valid_day(month, leap_check):
    while True:
        day = num_input(int, "\nPlease enter the day in which the transaction occurred : ", "Invalid day!")

        # To ensure there is no more than 31 days
        if day > 31:
            print("Invalid day!")
            continue

        # To ensure the day is valid for months with 30 days
        if month in (4, 6, 9, 11) and day > 30:
            print("There cannot be more than 30 days on this month. Please try again!")
            continue

        if month == 2:
            # To ensure the day is valid for february on a leap year
            if day > 29 and leap_check:
                print("There cannot be more than 29 days on February of a leap year. Please try again!")
                continue

            # To ensure the day is valid for february on a non-leap year
            elif day > 28 and not leap_check:
                print("There cannot be more than 28 days in february of a non-leap year. Please try again!")
                continue

        return day

def date_input():
    # Date validations
    year, leap_check = valid_year()  # valid year returns 2 values
    month = valid_month()
    day = valid_day(month, leap_check)

    # Formatting the date
    date = f"{year}-{month:02}-{day:02}"
    return date

# This function is to make sure that a user input index is valid
def valid_index(message, index_limit):
    while True:
        index = num_input(int, message, "Please enter a valid index(one from above)")
        if index > index_limit:
            print("Invalid index!")
            continue
        return index

# This function is to print data to the user
def for_loop_index_printer(object, message):
    x = 0  # to print indices for the user to pick
    for item in object:
        print(f"{x} - {item}")
        x += 1

    print(f"{x} - to quit function")
    print(message)
    return (x)

# This function is to print data to the user and navigate with the user
def data_printer(message, key_message, user_message):
    print("TRANSACTION CATEGORIES")
    for key in transactions.keys():
        print(key)
    print("Q - to quit function")
    print(message)

    # To make sure that user choice is valid
    while True:
        choice = input("\nEnter your choice : ").capitalize()
        if choice not in transactions.keys() and choice != "Q":
            print("\nInvalid choice!")
            continue
        else:
            break

    if choice != "Q":  # checking if the user wants to quit the function without proceeding
        while True:
            key_check = input(key_message).upper()

            if key_check == "T":
                key_check = True
                break
            elif key_check == "F":
                key_check = False
                break
            else:
                print("Invalid choice!")
                continue
        return key_check, choice

    else:
        print(user_message)
        return False, None

# This function is to get valid confirmation from user on something
def valid_confirmation(message, t_message, f_message, error_message="Invalid choice!"):
    while True:
        confirmation = input(message).upper()
        if confirmation == "T":
            print(t_message)
            return "T"
        if confirmation == "F":
            print(f_message)
            return "F"
        else:
            print(error_message)

# File handling functions
# This function is to safely open any file
def read_file(filename, object):
    content = None
    try:
        with open(filename, "r") as file:
            content = json.load(file)  # storing file content into a variable

    except FileNotFoundError:
        # if the file doesn't exist we are creating the file
        with open(filename, "w") as file:
            json.dump(object, file)  # adding a relevant object to the file (mostly an empty object)

    except json.JSONDecodeError:
        # If the file exists and the file is empty json.JSONDecodeError will occur
        with open(filename, "w") as file:
            json.dump(object, file)  # To mitigate the error an empty object is being serialized

    return content

def load_transactions():
    global transactions

    transactions = read_file("transactions.json", {})

def save_transactions():
    # File can be opened in "w" mode cause the contents of the file has already been extracted and stored safely
    with open("transactions.json", "w") as file:
        json.dump(transactions, file)

# This function is to navigate with another file to store and keep transaction type related info safely
def transaction_type_details(element, operation, new_element=None, transaction_type=None):
    content = read_file("transaction_type.json", {"Income": [], "Expense": []})

    if content is not None:
        if operation == "remove":
            # Filtering out the unwanted element
            content["Income"] = [x for x in content["Income"] if x != element]
            content["Expense"] = [x for x in content["Expense"] if x != element]

        if operation == "replace":
            # replacing new_element with the old_element
            content["Income"] = [new_element if x == element else x for x in content["Income"]]
            content["Expense"] = [new_element if x == element else x for x in content["Expense"]]

            if new_element in content["Income"] and new_element in content["Expense"]:
                print(f"\n{new_element} is in both the types!")
                user_confirmation = valid_confirmation("\nIs this transaction income type? (T/F) : ", "This category is recorded as an income type!", "This category is recorded as expense type!")
                if user_confirmation == "T":
                    content["Expense"].remove(new_element)
                else:
                    content["Income"].remove(new_element)

            # Checking for duplications
            content = {key: list(set(values)) for key, values in content.items()}

        if operation == "append" and element not in content[transaction_type]:
            content[transaction_type].append(element)

        if operation == "change_type":
            if element in content["Income"]:
                # Filtering out the unwanted element
                content["Income"] = [x for x in content["Income"] if x != element]

                # Adding the element to the other transaction type
                content["Expense"].append(element)

            else:
                # Filtering out the unwanted element
                content["Expense"] = [x for x in content["Expense"] if x != element]

                # Adding the element to the other transaction type
                content["Income"].append(element)

    else:
        # Adding transaction category to dictionary when "transaction_type.json" returns none
        content = {"Income": [], "Expense": []}
        if operation == "append":
            content[transaction_type].append(element)

    with open("transaction_type.json", "w") as file:
        json.dump(content, file)  # Making the changes permanent

# This function is to read from the "temp_transactions.txt" and transfer them to "transactions.json"
def read_bulk_transactions_from_file(filename):
    load_transactions()

    # bulk reading from the text file
    details = read_file(filename, [])

    if details is not None:
        for transaction in details:
            # Temporary dictionary to achieve the required format
            temp_dict = {}
            temp_dict["amount"] = transaction[0]
            temp_dict["date"] = transaction[3]

            # checking for transaction type
            if transaction[2] == "I":
                # Updating "transaction_type.json" file
                transaction_type_details(transaction[1], "append", transaction_type="Income")

            else:
                # Updating "transaction_type.json" file
                transaction_type_details(transaction[1], "append", transaction_type="Expense")

            # Checking if the current category is an existing key in the dictionary
            if transaction[1] in transactions.keys():
                transactions[transaction[1]].append(temp_dict)

            else:
                # creating a new key (category), if category doesn't exist
                transactions[transaction[1]] = [temp_dict]

        save_transactions()  # Making changes permanent

        # Deleting entries on the temporary txt file
        file = open("temp_transactions.txt", "w")
        file.close()

# This function is to retrieve data from transaction_type file
def get_transaction_type():
    global income_categories, expense_categories

    # If you try to add a function before creating the file, error will occur
    content = read_file("transaction_type.json", {"Income": [], "Expense": []})

    if content is None:
        content = {"Income": [], "Expense": []}

    # Retrieving transaction type details from the file
    income_categories = content["Income"]
    expense_categories = content["Expense"]

# This function allows users to add transactions directly from an external file
def add_file_transactions():
    # Giving instructions to the user on the file should be
    print("\nThe transactions on the file should be on the following format to add transactions : ")
    print("\nFormat - [[amount, category, type, date]]")
    print("Amount   - Numeric value")
    print("Category - Cannot be empty")
    print("Type     - 'I' or 'E'")
    print("Date     - 'YYYY-MM-DD'")
    print("\nExample - [[10000.0, 'Rent & utilities', 'E', '2024-03-16'], [15000.0, 'Revenue', 'I', '2024-03-15']]")
    filename = input("\nEnter the file name : ")

    content = read_file(filename, [])

    if content is not None:
        if type(content) == list:
            get_transaction_type()  # To get transaction type related info on the records
            local_list = []  # Local list to keep track of eligible transactions
            for transaction in content:
                if type(transaction) != list or len(transaction) != 4:  # Checking eligibility for the format
                    print()  # To maintain order on the output
                    print(transaction)
                    print("The transaction is not in the required format!")
                    continue

                elif type(transaction[0]) != float:  # Checking if amount is numeric
                    print()
                    print(transaction)
                    print("The transaction amount must be a numerical value!")
                    print("This transaction will not be added!")
                    continue

                elif type(transaction[1]) != str:  # Checking if category is valid
                    print()
                    print(transaction)
                    print("The transaction category is invalid!")
                    print("This transaction will not be added!")
                    continue

                elif not (transaction[1]):  # Checking if category is empty
                    print()
                    print(transaction)
                    print("The transaction category cannot be empty!")
                    print("This transaction will not be added!")
                    continue

                elif transaction[2] not in ("I", "E"):  # Checking if transaction type is valid
                    print()
                    print(transaction)
                    print("The transaction type is invalid!")
                    print("This transaction will not be added!")
                    continue

                elif transaction[1] in income_categories and transaction[2] == "E":
                    print(f"\n{transaction[1]} is Income type.")
                    print("If the transaction type is incorrect, temporarily update the transaction to the incorrect type and modify it after adding it to the system!")
                    continue

                elif transaction[1] in expense_categories and transaction[2] == "T":
                    print(f"\n{transaction[1]} is Expense type.")
                    print("If the transaction type is incorrect, temporarily update the transaction to the incorrect type and modify it after adding it to the system!")
                    continue

                elif len(transaction[
                             3]) != 10:  # Checking if date is valid, date can have only 10 characters in the given format
                    print()
                    print(transaction)
                    print("The date on the transaction is invalid!")
                    print("This transaction will not be added!")
                    continue

                # Checking for year validity
                elif not (transaction[3][:4].isdigit()) or int(transaction[3][:4]) > 2024 or int(
                        transaction[3][:4]) < 2000:
                    print()
                    print(transaction)
                    print("Invalid year on the date. Please try again!")
                    print("This transaction will not be added!")
                    continue

                # checking for month validity
                elif not (transaction[3][5:7].isdigit()) or int(transaction[3][5:7]) > 12:
                    print()
                    print(transaction)
                    print("Invalid month on the date. Please try again!")
                    print("This transaction will not be added!")
                    continue

                # checking for day validity
                elif not (transaction[3][8:].isdigit()) or int(transaction[3][8:]) > 31:
                    print()
                    print(transaction)
                    print("Invalid day on the date. Please try again!")
                    print("This transaction will not be added!")
                    continue

                elif int(transaction[3][5:7]) == 2:
                    year = int(transaction[3][:4])
                    leap_check = False  # Checking if the given year is leap year
                    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                        leap_check = True

                    if int(transaction[3][
                           8:]) > 29 and leap_check:  # Checking if the day is valid for february on a leap year
                        print()
                        print(transaction)
                        print("There cannot be more than 29 days in February on a leap year. Please try again!")
                        print("This transaction will not be added!")
                        continue

                    elif int(transaction[3][
                             8:]) > 28 and not leap_check:  # Checking if the date is valid for february on non-leap year
                        print()
                        print(transaction)
                        print("There cannot be more than 28 days in February on a non-leap year. Please try again!")
                        print("This transaction will not be added!")
                        continue

                elif transaction[3][4] != "-" or transaction[3][7] != "-":  # Checking for the format of the date
                    print()
                    print(transaction)
                    print("The transaction date is correct but missing the format!")
                    print("This transaction will not be added!")
                    continue

                else:
                    local_list.append(transaction)

            if len(local_list) == 0:
                print("\nThere are no transactions that are eligible to add!")

            elif len(local_list) != len(content):
                # Reading from the text file
                details = read_file("temp_transactions.txt", [])

                if details is None:
                    details = []

                print()  # To maintain an order
                print(local_list)
                print("\nThese transactions may already exist in the records, posing a risk of duplication.")

                confirmation = valid_confirmation("\nWould you like to add these transactions to the records? (T/F) : ", "\nTransactions added!", "\nNo transactions were added!")
                if confirmation == "T":
                    for i in local_list:
                        details.append(i)

                    with open("temp_transactions.txt", "w") as file:
                        json.dump(details, file)

                    read_bulk_transactions_from_file("temp_transactions.txt")

            else:
                print("\nThe transactions on this file are eligible to add!")
                print("These transactions may already exist in the records, posing a risk of duplication.")

                confirmation = valid_confirmation("\nWould you like to add these transactions to the records? (T/F) : ", "\nTransactions added!", "\nNo transactions were added!")
                if confirmation == "T":
                    read_bulk_transactions_from_file(filename)
        else:
            print("\nThe transactions are not in the required format!")
    else:
        print("\nFollowing could be the reasons why this file is not eligible:")
        print("1. File doesn't exist")
        print("2. File is empty")
        print("3. File format doesn't meet the requirement")

# Feature implementations
def add_transaction():
    # List  to store the transaction details
    details_list = []

    # User inputs
    amount = num_input(float, "\nEnter the amount of the transaction : ", "\nInvalid Amount!")
    category = valid_category()
    transaction_type = valid_type(category)
    date = date_input()

    # Creating a list with the details of the transaction
    details_list.extend([amount, category, transaction_type, date])

    # Reading from the text file
    details = read_file("temp_transactions.txt", [details_list])

    if details is None:
        details = []

    # Checking for duplicated entries
    # Reading the "transactions.json" file to check for duplications on the existing records
    main_content = read_file("transactions.json", {})

    if main_content is not None and category in main_content.keys():
        for dictionary in main_content[category]:
            if dictionary["amount"] == details_list[0] and dictionary["date"] == details_list[3]:
                print(f"\n{category} - {dictionary}")
                print("This transaction is getting duplicated!")

                # cCnfirming if the user has duplicated transaction purposefully
                user_confirmation = valid_confirmation("\nWould you like to add this transaction again? (T/F) : ", "\nTransaction has been added!", "Transaction was not duplicated!")
                if user_confirmation == "T":
                    details.append(details_list)
                    break
                else:
                    break
        # If the loop is not broken (entry not in the dictionary) transaction will get appended
        else:
            details.append(details_list)
            print("\nTransaction added!")

    # Checking for duplicated transactions on the text file
    else:
        if details_list in details:
            print(f"\n{details_list}")
            print("This transaction is getting duplicated!")

            # Confirming if the user has duplicated transaction purposefully
            confirmation = valid_confirmation("\nWould you like to add this transaction again? (T/F) : ", "\nTransaction has been duplicated!", "Transaction was not duplicated!")
            if confirmation == "T":
                # Duplicating transaction if the user wants
                details.append(details_list)

        else:
            # Updating list
            details.append(details_list)
            print("\nTransaction added!")

    # updating transaction for the "temp_transactions.json" file
    with open("temp_transactions.txt", "w") as file:
        json.dump(details, file)

def view_transactions_CLI():
    read_bulk_transactions_from_file("temp_transactions.txt")  # Pushing all the transactions to the main file

    # The user can only view transactions if there are existing transactions
    if transactions:
        get_transaction_type()
        transaction_number = 1  # To order the transactions
        for category, entries in transactions.items():
            for entry in entries:
                amount = entry["amount"]
                date = entry["date"]

                if category in income_categories:
                    transaction_type = "Income"
                else:
                    transaction_type = "Expense"
                print(f"\nTransaction number - {transaction_number}")
                print(f"Amount of the transaction    = {amount} LKR")
                print(f"category  of the transaction = {category}")
                print(f"Type of the transaction      = {transaction_type}")
                print(f"date of the transaction      = {date}")

                transaction_number += 1

    else:
        print("\nThere are no transactions to view!")

def view_transactions_GUI():
    read_bulk_transactions_from_file("temp_transactions.txt")  # Pushing all the transactions to the main file

    root = tk.Tk()
    try:
        app = FinanceTrackerGUI(root)
    except NameError: # Making sure the program doesn't crash if GUI_app python file is missing
        print("\nGUI file doesn't exist!")
    else:
        print("\nOpening GUI app!")
        app.display_transactions(app.transactions)
        root.mainloop()
        print("\nClosing GUI app!")

# The function is designed to update a single value at a time
def update_transaction():
    read_bulk_transactions_from_file("temp_transactions.txt")  # Pushing all the transactions to the main file

    # the user can only update transactions if they exist
    if transactions:
        view_transactions_CLI()  # For the user to choose the transaction to update
        print()  # To maintain order

        key_check, choice = data_printer("\nChose the category of the transaction you want to update", "\nDo you wish to update the category name itself? (T/F) : ", "\nNo transactions were updated!")

        if key_check:
            category = valid_category()  # Getting updated category from the user

            # If the correct category is already there in the dictionary, trying to update could overwrite and result in data loss
            if category not in transactions.keys():
                transactions[category] = transactions.pop(choice)  # Updating the key
            else:
                # This will enable adding multiple wrong entries to the correct category as well
                for entry in transactions[choice]:
                    transactions[category].append(
                        entry)  # Appending all the entries under the wrong category name to the right one

                # deleting the wrong category name entries
                del transactions[choice]
            print("\nTransaction updated!")

            # updating the transaction_type contents
            transaction_type_details(choice, "replace", new_element=category)

        else:
            if choice is not None:
                type_category = valid_confirmation("\nWould you like to change the type of the transaction? (T/F) : ", "\nTransaction type converted!", "\nTransaction type remains unchanged!")
                if type_category == "T":
                    get_transaction_type()
                    transaction_type_details(choice, "change_type")  # Updating transaction_type file

                print()  # To maintain order
                limit = for_loop_index_printer(transactions[choice], "Choose the index of an entry if you want to update it")

                chosen_entry = valid_index("\nEnter your choice : ", limit)

                if chosen_entry != limit:
                    print("1 - To update transaction amount")
                    print("2 - To update transaction date")
                    choose = valid_index("\nEnter your choice : ", 2)

                    confirmation = valid_confirmation("\nDo you want to update this transaction? (T/F) : ", "\nProceeding to update!", "\nNo transactions were updated!")
                    if confirmation == "T":
                        if choose == 1:
                            amount = num_input(float, "\nEnter the amount of the transaction : ", "\nInvalid Amount!")
                            transactions[choice][chosen_entry]["amount"] = amount

                        else:
                            date = date_input()
                            transactions[choice][chosen_entry]["date"] = date

                        print("\nTransaction updated!")

                else:
                    print("\nNo transactions were updated!")

        save_transactions()  # To make the changes permanent
    else:
        print("\nThere are no transactions to update!")

def delete_transaction():
    read_bulk_transactions_from_file("temp_transactions.txt")  # pushing all the transactions to the main file

    # The user can only delete a transaction if there are existing transactions
    if transactions:
        view_transactions_CLI()  # To make it easier for the user to choose the transaction to delete
        print()  # To maintain an order

        key_check, choice = data_printer("\nChose the category of the transaction you want to delete", "\nWould you like to delete all entries within this category? (T/F) : ", "\nNo transactions were deleted!")

        if key_check:
            confirmation = valid_confirmation("\nDo you want to delete all entries on this category? (T/F) : ", f"\nAll entries have been deleted!", "\nNo transactions were deleted!")
            if confirmation == "T":
                del transactions[choice]
                transaction_type_details(choice, "remove")  # To update transaction_type content

        else:
            if choice is not None:
                limit = for_loop_index_printer(transactions[choice],
                                               "Choose the index of an entry if you want to delete it")

                chosen_entry = valid_index("\nEnter your choice : ", limit)

                if chosen_entry != limit:
                    confirmation = valid_confirmation(
                        "\nWould you like to delete this transaction permanently? (T/F) : ",
                        "\nTransaction deleted successfully!", "\nNo transactions were deleted!")
                    if confirmation == "T":
                        del transactions[choice][chosen_entry]
                        # Checking if there are multiple transactions on that category
                        if len(transactions[choice]) > 0:
                            pass

                        # If there was only one entry on a key, deleting that entry will result in an empty list
                        else:
                            del transactions[choice]  # Deleting the key if that occurs
                            transaction_type_details(choice, "remove")  # To update transaction_type content

        save_transactions()  # To make changes permanent

    else:
        print("\nThere are no transactions to delete!")

def display_summary():
    read_bulk_transactions_from_file("temp_transactions.txt")

    # The user can only have these features if there are existing transactions
    if transactions:
        while True:
            print("\n--SUMMARY ON TRANSACTIONS.")
            print("1. Total Income")
            print("2. Total Expense")
            print("3. Net Income")
            print("4. Number of Transactions")
            print("5. Income Transactions")
            print("6. Expense Transactions")
            print("7. Exit")
            summary_choice = input("Enter your choice : ")
            # To categorize transaction amount according to the amount
            income_amount = []
            expense_amount = []

            get_transaction_type()  # updating the transaction types of existing records

            for key, value in transactions.items():  # categorising income and expense transactions
                for entry in value:
                    if key in income_categories:
                        income_amount.append(entry["amount"])
                    else:
                        expense_amount.append(entry["amount"])

            total_income = sum(income_amount)
            total_expense = sum(expense_amount)
            net_income = total_income - total_expense

            if summary_choice == "1":
                print(f"\nThe total income is {total_income} LKR")

            elif summary_choice == "2":
                print(f"\nThe total expense is {total_expense} LKR")

            elif summary_choice == "3":
                if net_income > 0:
                    print(f"\nThe net income is {net_income} LKR")
                else:
                    print(f"\nYou have no income. The net loss is {abs(net_income)} LKR")

            elif summary_choice == "4":
                num_of_transactions = 0
                for list in transactions.values():
                    num_of_transactions += len(list)
                print(f"\nThe number of transactions are : {num_of_transactions}")

            elif summary_choice == "5":
                if len(income_categories) > 0:  # checking for income transaction
                    print("\nThe transactions with income are: ")
                    for category, entries in transactions.items():
                        if category in income_categories:
                            for entry in entries:
                                print(f"{category} - {entry}")
                else:
                    print("\nThere are no income transactions!")

            elif summary_choice == "6":
                if len(expense_categories) > 0:  # checking for income transaction
                    print("\nThe transactions with expense are: ")
                    for category, entries in transactions.items():
                        if category in expense_categories:
                            for entry in entries:
                                print(f"{category} - {entry}")
                else:
                    print("\nThere are no expense transactions!")

            elif summary_choice == "7":
                print("\nExiting the 'Display Summary' function")
                break
            else:
                print("\nInvalid choice. Please try again!")
    else:
        print("\nThere are no transactions to display!")

def main_menu():
    load_transactions()  # Load transactions at the start
    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Display Summary")
        print("6. Save & Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            while True:
                print("\n1. Add Transactions directly to the system")
                print("2. Add transactions from an external file")
                print("3. Quit")
                user_choice = input("Enter your choice: ")
                if user_choice == "1":
                    add_transaction()
                elif user_choice == "2":
                    add_file_transactions()
                elif user_choice == "3":
                    print("\nExiting function")
                    break
                else:
                    print("\nInvalid choice. Please try again.")
        elif choice == '2':
            while True:
                print("\n1. View transactions on Command Line Interface")
                print("2. View transactions on Graphical User Interface")
                print("3. Quit")
                user_choice = input("Enter your choice: ")
                if user_choice == "1":
                    view_transactions_CLI()
                    break
                elif user_choice == "2":
                    view_transactions_GUI()
                    break
                elif user_choice == "3":
                    print("\nExiting function")
                    break
                else:
                    print("\nInvalid choice. Please try again.")
        elif choice == '3':
            update_transaction()
        elif choice == '4':
            delete_transaction()
        elif choice == '5':
            display_summary()
        elif choice == '6':
            read_bulk_transactions_from_file("temp_transactions.txt")
            print("\nSaving & exiting program.")
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
