#Import required libraries
import json
#import date and time
from datetime import datetime

# Global list to store transactions
transactions = {}
filename = "transactions.json"
textfile="transactions.txt"
#index variable to store index of transaction to be updated
index=0


# File handling functions
#Function to load transactions from file
def load_transactions():
    try:
        with open("transactions.json", "r") as file:
            global transactions
            transactions = json.load(file)

    except FileNotFoundError:
        print("File not found ")

    # fixing the JSON structure in the family
    except json.decoder.JSONDecodeError:
        print(f"The file '{filename}' is empty or contains invalid JSON.")

#Function to save transactions to file
def save_transactions():
    with open(filename, "w") as file:
        json.dump(transactions, file,indent=3)
    with open("transactions.txt","w")as file:
        file.write(str(transactions))

#read bulk data
def read_bulk_transactions_from_file(textfile):
    global transactions
    try:
        with open(textfile,"r")as file:
            for line in file:
                lines=line.strip().split(",")
                if len(lines)!=4:
                    print("Invalid transaction format:",line.strip())
                    continue
                amount=float(lines[0].strip())
                category=lines[1].strip()
                transaction_type=lines[2].strip().lower()
                date=lines[3].strip()

                if transaction_type not in["income","expense"]:
                    print("Invalid transaction type:",line.strip())
                    continue

                try:
                    date=datetime.strptime(date,"%y.%m.%d").date()

                except ValueError:
                    print("invalid date format:",line.strip())
                    continue

                if category not in transactions:
                    transactions[category]=[]
                transactions[category].append({"amount":amount,"transaction_type":transaction_type,"date":str(date)})
        save_transactions()#calling save transaction function
    except FileNotFoundError:
        print("file not found")





# Feature implementations
#Function to add a new transaction
def add_transaction():
    global index
    # Initialize amount variable
    amount = None
    while True:
        # prompt user to enter the amount
        amount_str = input("Enter the amount: ")
        if amount_str.isdigit():
            amount = float(amount_str)
            break
        else:
            print("Invalid Value entry. Please try again.")
    # Initialize category variable
    category = None
    while True:
        category = input("Enter the category: ")
        if category and not category.isdigit():
            break
        print("Invalid category. Please try again.")
    # Initialize transaction_type variable
    transaction_type = None
    while True:
        transaction_type = input("Enter the transaction type (income/expense): ")
        if transaction_type.lower() in ['income', 'expense']:
            break
        print("Invalid transaction type. Please enter 'income' or 'expense'.")
    # Initialize date variable
    date = None
    while True:
        date_str = input("Enter the date (YYYY-MM-DD): ")
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            break
        except ValueError:
            print("Invalid date format. Please try again.")
    if category not in transactions:#check category not in transactions
        transactions[category]=[]

    transactions[category].append({"index":index,"amount":amount,"transaction_type":transaction_type,"date": str(date)})

    save_transactions()#calling save transaction function

    print("Transaction added successfully")
    index+=1
#Function to view transaction in GUI
def view_transactions():
    import tkinter as tk
    from tkinter import ttk
    from tkinter.constants import W
    import json
    filename = "transactions.json"
    from datetime import datetime

    class FinanceTrackerGUI:
        def __init__(self, root):
            self.root = root
            self.root.title("Personal Finance Tracker")
            self.root.geometry("700x500")
            self.create_widgets(self.root)
            self.transactions = self.load_transactions("transactions.json")

        #creating widgets for GUI
        def create_widgets(self, root):
            self.myFrame = tk.Frame(root)
            self.myFrame.pack()
            # Label
            self.myLabel = tk.Label(self.root, text="Welcome to the Financial tracker", font=20)
            self.myLabel.pack()

            # Entry and search button
            self.myEntry = tk.Entry(self.root, font=("Helvetica", 15))
            self.myEntry.pack(padx=20, pady=10)
            self.myButton = tk.Button(self.root, text="Search", command=self.search_transactions)
            self.myButton.pack(padx=10, pady=10)

            # Frame for the treeview
            self.tree_Frame = tk.Frame(self.root)
            self.tree_Frame.pack(pady=20)
            #Scrollbar for treeview
            self.tree_Scroll = tk.Scrollbar(self.root)
            self.tree_Scroll.pack(side=tk.RIGHT, fill=tk.Y)

            self.myTree = ttk.Treeview(self.root, yscrollcommand=self.tree_Scroll.set)
            self.tree_Scroll.config(command=self.myTree.yview)

            #Define table column
            self.myTree['columns'] = ("Transaction_id", "Category", "Amount", "Transaction_Type", "Date")

            #Creating columns
            self.myTree.column("#0", width=0, minwidth=0)
            self.myTree.column("Transaction_id", anchor=W, width=120)
            self.myTree.column("Category", anchor=W, width=120)
            self.myTree.column("Amount", anchor=W, width=120)
            self.myTree.column("Transaction_Type", anchor=W, width=120)
            self.myTree.column("Date", anchor=W, width=120)


            #Creating Headings of the columns
            self.myTree.heading('#0', text="Label", anchor=tk.CENTER )
            self.myTree.heading("Transaction_id", text="Transaction_id", anchor=tk.CENTER ,command=lambda :self.sort_by_column("Transaction_id", False))
            self.myTree.heading("Category", text="Category", anchor=tk.CENTER,command=lambda : self.sort_by_column("Category", False))
            self.myTree.heading("Amount", text="Amount", anchor=tk.CENTER,command=lambda : self.sort_by_column("Amount", False))
            self.myTree.heading("Transaction_Type", text="Transaction_Type", anchor=tk.CENTER,command=lambda : self.sort_by_column("Transaction_Type", False))
            self.myTree.heading("Date", text="Date", anchor=tk.CENTER,command=lambda : self.sort_by_column("Date", False))

            self.myTree.pack(padx=10, pady=10)

        # File handling functions
        # Function to load transactions from file
        def load_transactions(self, filename):
            try:
                with open(filename, "r") as file:
                    transactions = json.load(file)
                    return transactions
            except FileNotFoundError:
                # Handle the case where the file does not exist
                print("File not found:", filename)
                return {}
            except json.JSONDecodeError:
                # Handle the case where the file is not valid JSON
                print("Invalid JSON format in file:", filename)
                return {}

        def display_transactions(self, transactions):
            # Clear existing rows
            for item in self.myTree.get_children():
                self.myTree.delete(item)

            # Populate the table with transactions
            transaction_id = 1
            for category, transactions_list in transactions.items():
                for transaction_data in transactions_list:
                    # Check if 'transaction_type' key is present in transaction_data
                    if 'transaction_type' in transaction_data:
                        transaction_type = transaction_data["transaction_type"]
                    else:
                        transaction_type = "N/A"  # Set a default value if key is missing

                    self.myTree.insert("", "end", values=(
                        transaction_id, category, transaction_data["amount"], transaction_type,
                        transaction_data["date"]))
                    transaction_id += 1

        def search_transactions(self):
            search_term = self.myEntry.get().lower()  # Get search term from entry field and convert to lowercase

            if not search_term:
                self.display_transactions(self.transactions)  # Display all transactions if search term is empty
                return

            filtered_transactions = {}
            for category, transactions_list in self.transactions.items():
                filtered_list = []
                for transaction_data in transactions_list:
                    # Search by category, transaction type, amount, and date (case-insensitive)
                    if (search_term in category.lower() or
                            search_term in transaction_data.get("transaction_type", "").lower() or
                            str(transaction_data["amount"]).lower().find(search_term) != -1 or
                            search_term in transaction_data["date"].lower()):
                        filtered_list.append(transaction_data)
                if filtered_list:
                    filtered_transactions[category] = filtered_list

            self.display_transactions(filtered_transactions)  # Display filtered transactions

        def sort_by_column(self, col, descending):
            # Get all items in the treeview
            items = [(self.myTree.set(item, col), item) for item in self.myTree.get_children('')]

            # Sort the items based on the column value
            items.sort(reverse=descending)

            # Reorder the items in the treeview based on the sorted list
            for index, (value, item) in enumerate(items):
                self.myTree.move(item, '', index)

            # Change the heading command to update the sorting when the column header is clicked
            self.myTree.heading(col, command=lambda: self.sort_by_column(col, not descending))

        def exit_program(self):
            self.root.destroy()

    def main():
        root = tk.Tk()
        app = FinanceTrackerGUI(root)
        app.display_transactions(app.transactions)

        quitButton = tk.Button(root, text="Exit", command=app.exit_program ,width= 8)
        quitButton.pack(side=tk.BOTTOM)

        root.mainloop()

    if __name__ == "__main__":
        main()


#Function to update a transaction
def update_transaction():
    global transactions, index
    # calling Function(reason for callin function therse user to see the available transactions and select which one they want to update)
    view_terminal()#calling view transaction function
    if not transactions:
        return ()
    # creates an infinite loop
    while True:
        try:  # prompts the user to enter an index for a transaction to update. The input is converted to an integer and stored in the index variable, with 1 subtracted from it. This likely aims to adjust for 0-based indexing

            index = int(input("Enter index of transaction to update: "))-1
            if index >= 0 and index < len(transactions):
                amount = float(input("Enter new amount: "))
                category = input("Enter new category:  ")
                transaction_type = input("Enter new type: (income/expense): ")
                date = input("Enter new date: (YYYY-MM-DD): ")

                transactions[category][index]["amount"] = amount
                transactions[category][index]["transaction_type"] = transaction_type
                transactions[category][index]["date"] = str(date)

                print("Transaction updated successfully!")
                break
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except IndexError:
            print("Please try again. Index Error.")

    save_transactions()#calling save transaction function



#Function to delete transaction
def delete_transaction():
    global transactions
    if not transactions:
        print("No transactions to delete.")
        return

    # Display available categories to choose from
    print("Available categories:")
    for category in transactions.keys():
        print(category)


    # Ask the user to choose a category
    category = input("Enter the category of the transaction you want to delete: ")

    # Check if the category exists in transactions
    if category not in transactions:
        print("Invalid category. Transaction not found.")
        return

    # Check if the index is within the range of the transactions list for the chosen category
    if index >= 0 and index < len(transactions[category]):
        del transactions[category][index]
        print("Transaction deleted successfully!")
    else:
        print("Invalid index! No transaction found at the specified index.")

    save_transactions()  # Save transaction to the file


def search_transactions(self):
    search_term = self.myEntry.get().lower()  # take search term form the entry and convert into the lowercase


    if not search_term:
        self.display_transactions(self.transactions)  # Display all transactions if search term is empty
        return

    filtered_transactions = {}
    for category, transactions_list in self.transactions.items():
        filtered_list = []
        for transaction_data in transactions_list:
            # Search by category, transaction type, amount, and date (case-insensitive)
            if (search_term in category.lower() or
                    search_term in transaction_data.get("transaction_type", "").lower() or
                    str(transaction_data["amount"]).lower().find(search_term) != -1 or
                    search_term in transaction_data["date"].lower()):
                filtered_list.append(transaction_data)
        if filtered_list:
            filtered_transactions[category] = filtered_list

    self.display_transactions(filtered_transactions)  # Display filtered transactions
#show transactions in the terminal
def view_terminal():
    global index
    # Check if transactions exist
    if not transactions:
        print("No transactions found.")
        return
    index = 1
    # Iterate through categories and transactions
    for category, transaction_list in transactions.items():  # Renamed variable to transaction_list
        print(f"\nCategory: {category}")
        for transaction in transaction_list:  # Iterate through the list of transactions
            # Format and display transaction details
            print(f"\tIndex: {index}")
            print(f"\tAmount: {transaction['amount']:.2f}")
            print(f"\tType: {transaction['transaction_type']}")
            print(f"\tDate: {transaction['date']}")
            index += 1  # Increment index for each transaction

#display the summary of all transactions
def display_summary(transactions):
    if isinstance(transactions, dict):
        try:
            #sum of the all total incomes
            Total_Income = sum(
                transaction["amount"] for transaction_list in transactions.values() for transaction in
                transaction_list if transaction["transaction_type"] == 'income')
            #sum of the all total expenses
            Total_Expenses = sum(
                transaction["amount"] for transaction_list in transactions.values() for transaction in
                transaction_list if transaction["transaction_type"] == 'expense')

            print(f" Total Income: {Total_Income:,.2f}{' ' * (51 - len(str(Total_Income)))}      ")
            print(f"Total Expenses: {Total_Expenses:,.2f}{' ' * (55 - len(str(Total_Expenses)))}")
            print(f" Net Balance:{Total_Income - Total_Expenses}{' ' * (59 - len(str(Total_Expenses)))}")


            if Total_Income > Total_Expenses:#check if total income higher than total expense
                print(f"\nYou have saved {Total_Income-Total_Expenses}.Keep it up")
            elif Total_Income < Total_Expenses:
                print("\nIt seems your expenses outweigh your income. Time to review your spending habits.")
            else:
                print("\nYour income matches your expenses. It's always good to maintain balance.")
        except IndexError:
            print("Error: Transaction list format is incorrect.")


    # Placeholder for summary display logic
#Main menu function to handle user input and calls to other functions
def main_menu():
    load_transactions()
    save_transactions()

    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Display Summary")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_transaction()
        elif choice == '2':
            view_transactions()
        elif choice == '3':
            update_transaction()
        elif choice == '4':
            delete_transaction()
        elif choice == '5':
            display_summary(transactions)
        elif choice == '6':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

#Entry point of the program
if __name__ == "__main__":
    main_menu()
