from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import messagebox
import json
import os
import uuid


# ==========================================
# ACCOUNT CLASS
# ==========================================

class Account(ABC):

    def __init__(self, account_number,
                 customer_id,
                 balance=0.0):

        self._account_number = account_number
        self._customer_id = customer_id
        self._balance = balance

    @property
    def account_number(self):
        return self._account_number

    @property
    def customer_id(self):
        return self._customer_id

    @property
    def balance(self):
        return self._balance

    @abstractmethod
    def deposit(self, amount):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass

    def display_details(self):

        return (
            f"Account Number : {self._account_number}\n"
            f"Customer ID    : {self._customer_id}\n"
            f"Balance        : ₹{self._balance:.2f}"
        )

    def to_dict(self):

        return {
            "account_number": self._account_number,
            "customer_id": self._customer_id,
            "balance": self._balance
        }


# ==========================================
# SAVINGS ACCOUNT
# ==========================================

class SavingsAccount(Account):

    def __init__(self,
                 account_number,
                 customer_id,
                 balance=0.0,
                 interest_rate=0.05):

        super().__init__(
            account_number,
            customer_id,
            balance
        )

        self._interest_rate = interest_rate

    def deposit(self, amount):

        if amount <= 0:
            return False

        self._balance += amount
        return True

    def withdraw(self, amount):

        if amount <= 0:
            return False

        if amount > self._balance:
            return False

        self._balance -= amount
        return True

    def apply_interest(self):

        self._balance += (
            self._balance *
            self._interest_rate
        )

    def display_details(self):

        return (
            super().display_details()
            + f"\nAccount Type   : Savings"
            + f"\nInterest Rate  : {self._interest_rate*100}%"
        )

    def to_dict(self):

        data = super().to_dict()

        data.update({
            "type": "savings",
            "interest_rate": self._interest_rate
        })

        return data


# ==========================================
# CHECKING ACCOUNT
# ==========================================

class CheckingAccount(Account):

    def __init__(self,
                 account_number,
                 customer_id,
                 balance=0.0,
                 overdraft_limit=1000):

        super().__init__(
            account_number,
            customer_id,
            balance
        )

        self._overdraft_limit = overdraft_limit

    def deposit(self, amount):

        if amount <= 0:
            return False

        self._balance += amount
        return True

    def withdraw(self, amount):

        if amount <= 0:
            return False

        if self._balance - amount < -self._overdraft_limit:
            return False

        self._balance -= amount
        return True

    def display_details(self):

        return (
            super().display_details()
            + "\nAccount Type   : Checking"
            + f"\nOverdraft Limit: ₹{self._overdraft_limit}"
        )

    def to_dict(self):

        data = super().to_dict()

        data.update({
            "type": "checking",
            "overdraft_limit": self._overdraft_limit
        })

        return data


# ==========================================
# CUSTOMER CLASS
# ==========================================

class Customer:

    def __init__(self,
                 customer_id,
                 name,
                 address):

        self._customer_id = customer_id
        self._name = name
        self._address = address
        self._accounts = []

    @property
    def customer_id(self):
        return self._customer_id

    @property
    def name(self):
        return self._name

    @property
    def address(self):
        return self._address

    @property
    def accounts(self):
        return self._accounts

    def add_account(self, account_no):

        if account_no not in self._accounts:
            self._accounts.append(account_no)

    def remove_account(self, account_no):

        if account_no in self._accounts:
            self._accounts.remove(account_no)

    def display_details(self):

        return (
            f"Customer ID : {self._customer_id}\n"
            f"Name        : {self._name}\n"
            f"Address     : {self._address}\n"
            f"Accounts    : {self._accounts}"
        )

    def to_dict(self):

        return {
            "customer_id": self._customer_id,
            "name": self._name,
            "address": self._address,
            "accounts": self._accounts
        }
# ==========================================
# BANK CLASS
# ==========================================

class Bank:

    def __init__(self):

        self.customers = {}
        self.accounts = {}

        self.customer_file = "/Users/prachiraghav/customers.json"
        self.account_file = "/Users/prachiraghav/accounts.json"

        self.load_data()

    # =====================================
    # LOAD DATA
    # =====================================

    def load_data(self):

        if os.path.exists(self.customer_file):

            try:

                with open(
                        self.customer_file,
                        "r") as file:

                    customer_data = json.load(file)

                    for data in customer_data:

                        customer = Customer(
                            data["customer_id"],
                            data["name"],
                            data["address"]
                        )

                        customer._accounts = \
                            data["accounts"]

                        self.customers[
                            customer.customer_id
                        ] = customer

            except:
                pass

        if os.path.exists(self.account_file):

            try:

                with open(
                        self.account_file,
                        "r") as file:

                    account_data = json.load(file)

                    for data in account_data:

                        if data["type"] == "savings":

                            account = SavingsAccount(
                                data["account_number"],
                                data["customer_id"],
                                data["balance"],
                                data["interest_rate"]
                            )

                        else:

                            account = CheckingAccount(
                                data["account_number"],
                                data["customer_id"],
                                data["balance"],
                                data["overdraft_limit"]
                            )

                        self.accounts[
                            account.account_number
                        ] = account

            except:
                pass

    # =====================================
    # SAVE DATA
    # =====================================

    def save_data(self):

        customer_list = []

        for customer in self.customers.values():

            customer_list.append(
                customer.to_dict()
            )

        account_list = []

        for account in self.accounts.values():

            account_list.append(
                account.to_dict()
            )

        with open(
                self.customer_file,
                "w") as file:

            json.dump(
                customer_list,
                file,
                indent=4
            )

        with open(
                self.account_file,
                "w") as file:

            json.dump(
                account_list,
                file,
                indent=4
            )

    # =====================================
    # ADD CUSTOMER
    # =====================================

    def add_customer(self,
                     customer):

        if customer.customer_id \
                in self.customers:

            return False

        self.customers[
            customer.customer_id
        ] = customer

        self.save_data()

        return True

    # =====================================
    # CREATE ACCOUNT
    # =====================================

    def create_account(self,
                       customer_id,
                       account_type,
                       balance=0.0,
                       interest_rate=0.05,
                       overdraft_limit=1000):

        if customer_id \
                not in self.customers:

            return None

        account_number = \
            str(uuid.uuid4())[:8]

        if account_type == "savings":

            account = SavingsAccount(
                account_number,
                customer_id,
                balance,
                interest_rate
            )

        else:

            account = CheckingAccount(
                account_number,
                customer_id,
                balance,
                overdraft_limit
            )

        self.accounts[
            account_number
        ] = account

        self.customers[
            customer_id
        ].add_account(
            account_number
        )

        self.save_data()

        return account

    # =====================================
    # DEPOSIT
    # =====================================

    def deposit(self,
                account_no,
                amount):

        account = self.accounts.get(
            account_no
        )

        if account is None:
            return False

        result = account.deposit(
            amount
        )

        if result:
            self.save_data()

        return result

    # =====================================
    # WITHDRAW
    # =====================================

    def withdraw(self,
                 account_no,
                 amount):

        account = self.accounts.get(
            account_no
        )

        if account is None:
            return False

        result = account.withdraw(
            amount
        )

        if result:
            self.save_data()

        return result

    # =====================================
    # TRANSFER
    # =====================================

    def transfer_funds(self,
                       sender_acc,
                       receiver_acc,
                       amount):

        sender = self.accounts.get(
            sender_acc
        )

        receiver = self.accounts.get(
            receiver_acc
        )

        if sender is None:
            return False

        if receiver is None:
            return False

        if sender.withdraw(amount):

            receiver.deposit(amount)

            self.save_data()

            return True

        return False

    # =====================================
    # APPLY INTEREST
    # =====================================

    def apply_interest(self):

        for account in self.accounts.values():

            if isinstance(
                    account,
                    SavingsAccount):

                account.apply_interest()

        self.save_data()

    # =====================================
    # VIEW CUSTOMERS
    # =====================================

    def get_all_customers(self):

        return list(
            self.customers.values()
        )

    # =====================================
    # VIEW ACCOUNTS
    # =====================================

    def get_all_accounts(self):

        return list(
            self.accounts.values()
        )

    # =====================================
    # SEARCH ACCOUNT
    # =====================================

    def search_account(
            self,
            account_number):

        return self.accounts.get(
            account_number
        )

    # =====================================
    # DELETE ACCOUNT
    # =====================================

    def delete_account(
            self,
            account_number):

        account = self.accounts.get(
            account_number
        )

        if account is None:
            return False

        customer = self.customers[
            account.customer_id
        ]

        customer.remove_account(
            account_number
        )

        del self.accounts[
            account_number
        ]

        self.save_data()

        return True
# =====================================
# CREATE BANK OBJECT
# =====================================

bank = Bank()


# =====================================
# GUI FUNCTIONS
# =====================================

def add_customer_gui():

    customer_id = entry_cid.get().strip()
    name = entry_name.get().strip()
    address = entry_address.get().strip()

    if customer_id == "" or name == "":
        messagebox.showerror(
            "Error",
            "Enter Customer Details"
        )
        return

    customer = Customer(
        customer_id,
        name,
        address
    )

    if bank.add_customer(customer):

        messagebox.showinfo(
            "Success",
            "Customer Added Successfully"
        )

        entry_cid.delete(0, tk.END)
        entry_name.delete(0, tk.END)
        entry_address.delete(0, tk.END)

    else:

        messagebox.showerror(
            "Error",
            "Customer Already Exists"
        )
def search_account_gui():

    account_no = entry_search_acc.get().strip()

    account = bank.search_account(
        account_no
    )

    output.delete(
        "1.0",
        tk.END
    )

    if account:

        output.insert(
            tk.END,
            account.display_details()
        )

    else:

        output.insert(
            tk.END,
            "Account Not Found"
        )
def delete_account_gui():

    account_no = entry_search_acc.get().strip()

    if bank.delete_account(
            account_no):

        messagebox.showinfo(
            "Success",
            "Account Deleted Successfully"
        )

    else:

        messagebox.showerror(
            "Error",
            "Account Not Found"
        )

def create_savings_gui():

    try:

        customer_id = entry_acc_customer.get()

        balance = float(
            entry_balance.get()
        )

        rate = float(
            entry_interest.get()
        )

        account = bank.create_account(
            customer_id,
            "savings",
            balance,
            rate
        )

        if account:

            messagebox.showinfo(
                "Success",
                f"Account Created\n\n"
                f"Account No : "
                f"{account.account_number}"
            )

        else:

            messagebox.showerror(
                "Error",
                "Customer Not Found"
            )

    except:

        messagebox.showerror(
            "Error",
            "Invalid Input"
        )


def create_checking_gui():

    try:

        customer_id = entry_acc_customer.get()

        balance = float(
            entry_balance.get()
        )

        overdraft = float(
            entry_overdraft.get()
        )

        account = bank.create_account(
            customer_id,
            "checking",
            balance,
            0.05,
            overdraft
        )

        if account:

            messagebox.showinfo(
                "Success",
                f"Account Created\n\n"
                f"Account No : "
                f"{account.account_number}"
            )

        else:

            messagebox.showerror(
                "Error",
                "Customer Not Found"
            )

    except:

        messagebox.showerror(
            "Error",
            "Invalid Input"
        )


def deposit_gui():

    try:

        account_no = entry_dep_acc.get()

        amount = float(
            entry_dep_amount.get()
        )

        if bank.deposit(
                account_no,
                amount):

            messagebox.showinfo(
                "Success",
                "Deposit Successful"
            )

        else:

            messagebox.showerror(
                "Error",
                "Account Not Found"
            )

    except:

        messagebox.showerror(
            "Error",
            "Invalid Amount"
        )


def withdraw_gui():

    try:

        account_no = entry_with_acc.get()

        amount = float(
            entry_with_amount.get()
        )

        if bank.withdraw(
                account_no,
                amount):

            messagebox.showinfo(
                "Success",
                "Withdrawal Successful"
            )

        else:

            messagebox.showerror(
                "Error",
                "Insufficient Balance"
            )

    except:

        messagebox.showerror(
            "Error",
            "Invalid Amount"
        )


def transfer_gui():

    try:

        sender = entry_from.get()
        receiver = entry_to.get()

        amount = float(
            entry_transfer_amount.get()
        )

        if bank.transfer_funds(
                sender,
                receiver,
                amount):

            messagebox.showinfo(
                "Success",
                "Transfer Successful"
            )

        else:

            messagebox.showerror(
                "Error",
                "Transfer Failed"
            )

    except:

        messagebox.showerror(
            "Error",
            "Invalid Input"
        )


def view_customers():

    output.delete(
        "1.0",
        tk.END
    )

    customers = bank.get_all_customers()

    if len(customers) == 0:

        output.insert(
            tk.END,
            "No Customers Found"
        )

        return

    for customer in customers:

        details = (
            f"Customer ID : {customer.customer_id}\n"
            f"Name        : {customer.name}\n"
            f"Address     : {customer.address}\n\n"
        )

        if len(customer.accounts) == 0:

            details += "No Accounts Found\n"

        else:

            details += "Accounts:\n"

            for acc_no in customer.accounts:

                account = bank.search_account(acc_no)

                if account:

                    details += (
                        f"\nAccount Number : {account.account_number}\n"
                        f"Available Balance : ₹{account.balance:.2f}\n"
                    )

        details += "\n" + "=" * 60 + "\n"

        output.insert(
            tk.END,
            details
        )

def view_accounts():

    output.delete(
        "1.0",
        tk.END
    )

    accounts = bank.get_all_accounts()

    if len(accounts) == 0:

        output.insert(
            tk.END,
            "No Accounts Found"
        )

        return

    for account in accounts:

        output.insert(
            tk.END,
            account.display_details()
        )

        output.insert(
            tk.END,
            "\n" + "="*60 + "\n"
        )


def apply_interest_gui():

    bank.apply_interest()

    messagebox.showinfo(
        "Success",
        "Interest Applied Successfully"
    )
# =====================================
# GUI WINDOW
# =====================================

root = tk.Tk()

root.title(
    "Banking Management System"
)

root.geometry(
    "1200x800"
)

root.configure(
    bg="#1E3A5F"
)

heading = tk.Label(
    root,
    text="🏦 BANKING MANAGEMENT SYSTEM",
    font=("Arial", 22, "bold"),
    bg="#1E3A5F",
    fg="white"
)

heading.pack(
    pady=10
)

# =====================================
# CUSTOMER FRAME
# =====================================

frame_customer = tk.LabelFrame(
    root,
    text="Customer Details",
    padx=10,
    pady=10
)

frame_customer.pack(
    fill="x",
    padx=10,
    pady=5
)

tk.Label(
    frame_customer,
    text="Customer ID"
).grid(row=0, column=0)

entry_cid = tk.Entry(
    frame_customer,
    width=25
)

entry_cid.grid(
    row=0,
    column=1
)

tk.Label(
    frame_customer,
    text="Name"
).grid(row=1, column=0)

entry_name = tk.Entry(
    frame_customer,
    width=25
)

entry_name.grid(
    row=1,
    column=1
)

tk.Label(
    frame_customer,
    text="Address"
).grid(row=2, column=0)

entry_address = tk.Entry(
    frame_customer,
    width=25
)

entry_address.grid(
    row=2,
    column=1
)

tk.Button(
    frame_customer,
    text="Add Customer",
    bg="lightgreen",
    command=add_customer_gui
).grid(
    row=3,
    column=1,
    pady=5
)

# =====================================
# ACCOUNT FRAME
# =====================================

frame_account = tk.LabelFrame(
    root,
    text="Create Account",
    padx=10,
    pady=10
)

frame_account.pack(
    fill="x",
    padx=10,
    pady=5
)

tk.Label(
    frame_account,
    text="Customer ID"
).grid(row=0, column=0)

entry_acc_customer = tk.Entry(
    frame_account
)

entry_acc_customer.grid(
    row=0,
    column=1
)

tk.Label(
    frame_account,
    text="Initial Balance"
).grid(row=1, column=0)

entry_balance = tk.Entry(
    frame_account
)

entry_balance.grid(
    row=1,
    column=1
)

tk.Label(
    frame_account,
    text="Interest Rate"
).grid(row=2, column=0)

entry_interest = tk.Entry(
    frame_account
)

entry_interest.insert(
    0,
    "0.05"
)

entry_interest.grid(
    row=2,
    column=1
)

tk.Label(
    frame_account,
    text="Overdraft Limit"
).grid(row=3, column=0)

entry_overdraft = tk.Entry(
    frame_account
)

entry_overdraft.insert(
    0,
    "1000"
)

entry_overdraft.grid(
    row=3,
    column=1
)

tk.Button(
    frame_account,
    text="Create Savings",
    bg="lightblue",
    command=create_savings_gui
).grid(
    row=4,
    column=0,
    pady=5
)

tk.Button(
    frame_account,
    text="Create Checking",
    bg="lightyellow",
    command=create_checking_gui
).grid(
    row=4,
    column=1,
    pady=5
)

# =====================================
# DEPOSIT FRAME
# =====================================

frame_deposit = tk.LabelFrame(
    root,
    text="Deposit Money"
)

frame_deposit.pack(
    fill="x",
    padx=10,
    pady=5
)

tk.Label(
    frame_deposit,
    text="Account No"
).grid(row=0, column=0)

entry_dep_acc = tk.Entry(
    frame_deposit
)

entry_dep_acc.grid(
    row=0,
    column=1
)

tk.Label(
    frame_deposit,
    text="Amount"
).grid(row=1, column=0)

entry_dep_amount = tk.Entry(
    frame_deposit
)

entry_dep_amount.grid(
    row=1,
    column=1
)

tk.Button(
    frame_deposit,
    text="Deposit",
    bg="lightgreen",
    command=deposit_gui
).grid(
    row=2,
    column=1
)

# =====================================
# WITHDRAW FRAME
# =====================================

frame_withdraw = tk.LabelFrame(
    root,
    text="Withdraw Money"
)

frame_withdraw.pack(
    fill="x",
    padx=10,
    pady=5
)

tk.Label(
    frame_withdraw,
    text="Account No"
).grid(row=0, column=0)

entry_with_acc = tk.Entry(
    frame_withdraw
)

entry_with_acc.grid(
    row=0,
    column=1
)

tk.Label(
    frame_withdraw,
    text="Amount"
).grid(row=1, column=0)

entry_with_amount = tk.Entry(
    frame_withdraw
)

entry_with_amount.grid(
    row=1,
    column=1
)

tk.Button(
    frame_withdraw,
    text="Withdraw",
    bg="salmon",
    command=withdraw_gui
).grid(
    row=2,
    column=1
)

# =====================================
# TRANSFER FRAME
# =====================================

frame_transfer = tk.LabelFrame(
    root,
    text="Transfer Funds"
)

frame_transfer.pack(
    fill="x",
    padx=10,
    pady=5
)

tk.Label(
    frame_transfer,
    text="From Account"
).grid(row=0, column=0)

entry_from = tk.Entry(
    frame_transfer
)

entry_from.grid(
    row=0,
    column=1
)

tk.Label(
    frame_transfer,
    text="To Account"
).grid(row=1, column=0)

entry_to = tk.Entry(
    frame_transfer
)

entry_to.grid(
    row=1,
    column=1
)

tk.Label(
    frame_transfer,
    text="Amount"
).grid(row=2, column=0)

entry_transfer_amount = tk.Entry(
    frame_transfer
)

entry_transfer_amount.grid(
    row=2,
    column=1
)

tk.Button(
    frame_transfer,
    text="Transfer",
    bg="orange",
    command=transfer_gui
).grid(
    row=3,
    column=1
)

# =====================================
# ACTION BUTTONS
# =====================================

action_frame = tk.Frame(
    root,
    bg="#EAF4FC"
)

action_frame.pack(
    pady=10
)

tk.Button(
    action_frame,
    text="View Customers",
    width=20,
    command=view_customers
).grid(row=0, column=0, padx=5)

tk.Button(
    action_frame,
    text="View Accounts",
    width=20,
    command=view_accounts
).grid(row=0, column=1, padx=5)

tk.Button(
    action_frame,
    text="Apply Interest",
    width=20,
    command=apply_interest_gui
).grid(row=0, column=2, padx=5)

tk.Label(
    action_frame,
    text="Account No"
).grid(
    row=0,
    column=3,
    padx=5
)

entry_search_acc = tk.Entry(
    action_frame,
    width=15
)

entry_search_acc.grid(
    row=0,
    column=4,
    padx=5
)

tk.Button(
    action_frame,
    text="Search Account",
    command=search_account_gui
).grid(
    row=0,
    column=5,
    padx=5
)

tk.Button(
    action_frame,
    text="Delete Account",
    command=delete_account_gui
).grid(
    row=0,
    column=6,
    padx=5
)

# =====================================
# OUTPUT BOX
# =====================================

output = tk.Text(
    root,
    width=130,
    height=18,
    font=("Consolas", 10)
)

output.pack(
    padx=10,
    pady=10
)

# =====================================
# RUN PROGRAM
# =====================================

root.mainloop()
