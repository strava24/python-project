import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json

class FinanceTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.create_widgets()

        # Getting the transactions from the file
        entries = self.load_transactions("transactions.json")
        self.transactions = self.valid_transactions(entries)
        if not self.transactions:
            messagebox.showinfo("Status", "No transactions on the system!")

        # Getting transaction type related information
        transaction_type = self.load_transactions("transaction_type.json")
        # Checking for the validity of content on transaction type file
        if type(transaction_type) != dict or len(transaction_type.keys()) != 2 or "Income" not in transaction_type.keys() or "Expense" not in transaction_type.keys():
            self.income_transactions = [] # Giving empty lists to these variables if transactions are invalid to prevent program from crashing
            self.expense_transactions = []
            existing_warning = self.warnings_label.cget("text") # Getting the currently displayed warnings
            if existing_warning: # This is just to maintain order
                modified_warning = existing_warning + "\nTransactions type file isn't accessible!" # Modifying the warnings
                self.warnings_label.config(text=modified_warning)
            else:
                self.warnings_label.config(text="Transactions type file isn't accessible!")

        else: # Sorting transactions according to its type
            self.income_transactions = transaction_type["Income"]
            self.expense_transactions = transaction_type["Expense"]
            self.detail_label.config(text="⚪ - Income Type\n⚫ - Expense Type")

        # This variable is to keep track of the order of each column's order / To toggle between the ascending and descending order
        self.column_order = {"Date": True, "Category": True, "Amount": True}
        # If the type of transaction category is unknown this variable will hold that category
        self.unknown_keys = []

        # This is to enable search functionality, when the user clicks ENTER on keyboard
        self.root.bind("<Return>", self.search_transactions)

    def create_widgets(self):
        # Search bar and button
        search_frame = ttk.Frame(self.root)  # Creating another frame for search feature
        search_frame.pack(fill="x")  # Packing the frame in a way that fills the window horizontally

        self.search_entry = ttk.Entry(search_frame, width=86)  # Creating entry field
        self.search_entry.pack(padx=5, side="left")  # Packing it with padding

        search_button = ttk.Button(search_frame, text="Search", command=self.search_transactions)  # Creating search button
        search_button.pack(side="left")  # Packing the search button
        # Frame for table and scrollbar
        tree_frame = ttk.Frame(self.root) # Creating the frame
        tree_frame.pack(fill = "both") # Packing the frame in a way that fills the window

        # Treeview for displaying transactions
        cols = ("Date", "Category", "Amount") # Initialising the columns
        self.treeview = ttk.Treeview(tree_frame, columns=cols, show="headings") # Creating treeview

        # Giving headings to the columns
        self.treeview.heading("Date", text="Date", command=lambda c="Date": self.sort_columns(c))
        self.treeview.heading("Category", text="Category", command=lambda c="Category": self.sort_columns(c))
        self.treeview.heading("Amount", text="Amount", command=lambda c="Amount": self.sort_columns(c))

        # Packing treeview to the left with padding to make the treeview more appealing
        self.treeview.pack(side="left", fill="both", padx=5, pady=5)

        # Scrollbar for the Treeview
        scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.treeview.yview) # Creating the scrollbar with a link to the treeview
        scroll.pack(side="right", fill="y") # Packing the scrollbar to the right
        self.treeview.configure(yscrollcommand=scroll.set) # Making treeview respond to the changes made to scrollbar

        # Warning area to display invalid transactions if there are any
        self.detail_label = ttk.Label(self.root, text="")
        self.detail_label.pack(fill="x", padx=15, pady=5, side="right")
        self.warnings_label = ttk.Label(self.root, text="", foreground="red")
        self.warnings_label.pack(fill="x", padx=5, pady=5)

    def load_transactions(self, filename):
        try: # Trying to open the file and read
            with open(filename, "r") as file:
                content = json.load(file)
            return content

        except FileNotFoundError:  # Showing an error message box if the file doesn't exist
            return {}

        except json.JSONDecodeError:  # Showing an error message box if the file is empty or invalid
            return {}

    # This function is to check if the transactions on the file are valid
    def valid_transactions(self, transactions):
        revised_transactions = {}  # This variable is to hold all the eligible transactions
        warnings = []  # This variable is to hold warnings regarding invalid transactions

        if type(transactions) == dict:
            for key, value in transactions.items():
                valid_transactions = []  # This variable is to hold valid transactions on this type
                # Checking if the transaction type is empty
                if key == "":
                    warnings.append(f"Transaction category is empty : {value}")
                    continue

                for entry in value:
                    # Checking if the value is a list
                    if type(value) != list and type(entry) != dict:
                        warnings.append(f"Invalid format for {key}")

                    # Checking if the dictionary is in the correct format
                    elif len(entry.keys()) != 2 or "amount" not in entry.keys() or "date" not in entry.keys():
                        warnings.append(f"Invalid format for {key} : {entry}")

                    # Checking if the amount is valid
                    elif type(entry["amount"]) != float and type(entry["amount"]) != int:
                        warnings.append(f"Invalid amount for {key} : {entry}")

                    # Checking for date validity
                    elif len(entry["date"]) != 10:
                        warnings.append(f"Invalid date format for {key} : {entry}")

                    # Checking for the year validity
                    elif not (entry["date"][:4].isdigit()) or int(entry["date"][:4]) > 2024 or int(
                            entry["date"][:4]) < 2000:
                        warnings.append(f"Invalid year for {key}: {entry}")

                    # Checking for the month validity
                    elif not (entry["date"][5:7].isdigit()) or int(entry["date"][5:7]) > 12:
                        warnings.append(f"Invalid month for {key}: {entry}")

                    # Checking for the day validity
                    elif not (entry["date"][8:].isdigit()) or int(entry["date"][8:]) > 31:
                        warnings.append(f"Invalid day for {key}: {entry}")

                    elif entry["date"][4] != "-" or entry["date"][7] != "-":  # Checking for the format of the date
                        warnings.append(f"Invalid date format for {key}: {entry}")

                    # Checking for day validity if the month is February
                    elif int(entry["date"][5:7]) == 2:
                        year = int(entry["date"][:4])
                        leap_check = False  # Checking if the given year is leap year
                        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                            leap_check = True

                        # Checking if the day is valid for February on a leap year
                        if int(entry["date"][8:]) > 29 and leap_check:
                            warnings.append(f"Invalid day for February on a leap year - {key}: {entry}")

                        # Checking if the date is valid for february on non-leap year
                        elif int(entry["date"][8:]) > 28 and not leap_check:
                            warnings.append(f"Invalid day for a February on a non-leap year - {key}: {entry}")

                        else:
                            valid_transactions.append(entry)  # Adding the valid transaction

                    else:
                        valid_transactions.append(entry)  # Adding the valid transaction

                if valid_transactions:  # Adding the valid transactions of a category into the dictionary
                    revised_transactions[key] = valid_transactions

            if warnings:
                self.warnings_label.config(text="\n".join(warnings))

        else:
            messagebox.showwarning("Warning", "The transactions are not in the required format!")

        return revised_transactions

    def display_transactions(self, transactions):
        # Removing existing entries
        for entry in self.treeview.get_children(): # Getting all the existing entries in the treeview
            self.treeview.delete(entry)

        # Add transactions to the treeview
        if self.income_transactions or self.expense_transactions:
            #invalid_keys = []  # This variable is to hold transaction category for which transaction type is unknown
            for key, value in transactions.items():
                for transaction in value:
                    temp_list = [] # Creating a temporary list to add the values we want
                    if key in self.income_transactions:
                        temp_list.extend([(transaction["date"]), key+"⚪", transaction["amount"]]) # Adding values to the temporary list on column order
                    elif key in self.expense_transactions:
                        temp_list.extend([(transaction["date"]), key+"⚫", transaction["amount"]]) # Adding values to the temporary list on column order
                    else:
                        temp_list.extend([(transaction["date"]), key, transaction["amount"]])
                        if key not in self.unknown_keys:
                            existing_warning = self.warnings_label.cget("text")
                            if existing_warning: # This is to maintain order
                                modified_warning = existing_warning + f"\nTransaction type is unknown for {key}" # Modifying the warnings
                                self.warnings_label.config(text=modified_warning)
                            else:
                                self.warnings_label.config(text=f"Transaction type is unknown for {key}")
                            self.unknown_keys.append(key)

                    if temp_list:
                        # Adding the values of each transaction on the column order / Not adding under any parent
                        self.treeview.insert("", "end", values=temp_list)

        else:
            for key, value in transactions.items():
                for transaction in value:
                    temp_list = []  # Creating a temporary list to add the values we want
                    temp_list.extend([(transaction["date"]), key, transaction["amount"]])  # Adding values to the temporary list on column order
                    # Adding the values of each transaction on the column order / Not adding under any parent
                    self.treeview.insert("", "end", values=temp_list)

    # event parameter is required when trying to search by clicking ENTER on keyboard
    def search_transactions(self, event=None):
        user_search = self.search_entry.get() # Getting user's entry

        # This variable is to store the filtered transactions according to the user search
        filter_transactions = {}

        # Checking if user's search is related to "expense"
        if user_search.strip().lower() in "expense" and user_search != "":
            for key, value in self.transactions.items():
                if key in self.expense_transactions:
                    filter_transactions[key] = value

        # Checking if user's search is related to "income"
        elif user_search.strip().lower() in "income" and user_search != "":
            for key, value in self.transactions.items():
                if key in self.income_transactions:
                    filter_transactions[key] = value

        else:
            for key, value in self.transactions.items():
                # Checking if the user's search matches dictionary key / transaction type
                if user_search.strip().lower() in key.lower():
                    filter_transactions[key] = value # If so adding all the transactions under that transaction_type

                else:
                    # This variable is to hold all the transactions under the current transaction type that match user's search
                    temp_transactions = []
                    for transaction in value:
                        # Checking if user's search match with date or amount of any transactions under this transaction type
                        if user_search.strip() in transaction["date"] or user_search.strip() == str(transaction["amount"]) or user_search.strip() == str(int(transaction["amount"])):
                            temp_transactions.append(transaction)

                    # Checking if there are eligible transactions within the current key
                    if temp_transactions:
                        filter_transactions[key] = temp_transactions # adding the eligible transactions

        # checking if there are any eligible transactions to display according to the user's search
        if filter_transactions:
            self.display_transactions(filter_transactions) # Displaying the filtered transactions

        # Displaying a message box if there are no eligible transactions according to the user's search
        else:
            messagebox.showinfo("Message", "There are no transactions under this search!")

    # This function is to get the order to sort a column
    def sort_columns(self, col):
        # Getting the opposite value of the column to sort
        reverse = not (self.column_order[col])
        self.column_order[col] = reverse # Modifying the order on the dict

        # Calling the sort_by_column to sort the selected column
        self.sort_by_column(col, reverse)

    def sort_by_column(self, col, reverse):
        # This variable is to hold sorted items related data
        data_list = []
        for id in self.treeview.get_children(): # Getting the identifiers of all the rows
            value = self.treeview.set(id, col) # Getting the corresponding column value of the id row
            if col == "Amount": # Checking if the column is "Amount"
                value = float(value) # Changing the data type to float if the column is "Amount"
            temp_list = [value, id] # Making a value, id list
            data_list.append(temp_list)

        # Sorting the data list
        data_list.sort(reverse=reverse)

        # Rearranging the data according to the sort
        for index in range(len(data_list)):
            lst = data_list[index]
            self.treeview.move(lst[1], '', index)

def main():
    root = tk.Tk()
    app = FinanceTrackerGUI(root)
    app.display_transactions(app.transactions)
    root.mainloop()

if __name__ == "__main__":
    main()
