import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import os

class DrugStoreDB:
    def __init__(self, db_name="drugstore.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Initialize the database and create tables if they don't exist"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Create Customer table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Customer (
                cid TEXT PRIMARY KEY,
                cname TEXT,
                caddress TEXT,
                ctel TEXT,
                cillness TEXT
            )
        ''')
        
        # Create Employee table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Employee (
                eid TEXT PRIMARY KEY,
                ename TEXT,
                eaddress TEXT,
                etel TEXT,
                esalary REAL
            )
        ''')
        
        # Create Drug table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Drug (
                did TEXT PRIMARY KEY,
                dname TEXT,
                dtype TEXT,
                eprice REAL,
                eemployee TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)

# Global database instance
db = DrugStoreDB()

def on_select():
    print(v_gender.get())

def GetValue(event):
    """Fixed function to get selected values from treeview"""
    try:
        # Get the selected item
        selection = event.widget.selection()
        if not selection:
            return
        
        item = event.widget.item(selection[0])
        values = item['values']
        
        # Clear all entry fields first
        clear_entries()
        
        # Check which treeview was clicked and populate accordingly
        if len(values) == 5:
            if 'cid' in str(values[0]) or isinstance(values[0], str):
                # Customer data
                e1.insert(0, values[0])  # cid
                e2.insert(0, values[1])  # cname
                e3.insert(0, values[2])  # caddress
                e4.insert(0, values[3])  # ctel
                e5.insert(0, values[4])  # cillness
                v_gender.set('m')  # Set to customer
            elif 'eid' in str(values[0]) or 'did' in str(values[0]):
                if 'eid' in str(values[0]):
                    # Employee data
                    e1.insert(0, values[0])  # eid
                    e2.insert(0, values[1])  # ename
                    e3.insert(0, values[2])  # eaddress
                    e4.insert(0, values[3])  # etel
                    e5.insert(0, values[4])  # esalary
                    v_gender.set('f')  # Set to employee
                else:
                    # Drug data
                    e6.insert(0, values[0])  # did
                    e7.insert(0, values[1])  # dname
                    e8.insert(0, values[2])  # dtype
                    e9.insert(0, values[3])  # eprice
                    e10.insert(0, values[4])  # eemployee
    except Exception as e:
        print(f"Error in GetValue: {e}")

def clear_entries():
    """Clear all entry fields"""
    for entry in [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10]:
        entry.delete(0, END)

def ADD():
    """Add customer or employee based on selection"""
    selected_type = v_gender.get()
    
    if selected_type == 'm':  # Customer
        cid = e1.get().strip()
        cname = e2.get().strip()
        caddress = e3.get().strip()
        ctel = e4.get().strip()
        cillness = e5.get().strip()
        
        if not all([cid, cname, caddress, ctel, cillness]):
            messagebox.showerror("Error", "Please fill all customer fields")
            return
        
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Customer(cid, cname, caddress, ctel, cillness) VALUES (?, ?, ?, ?, ?)",
                (cid, cname, caddress, ctel, cillness)
            )
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Information", "Customer data saved successfully")
            clear_entries()
            refresh_customer_list()
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Customer ID already exists")
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")
    
    elif selected_type == 'f':  # Employee
        eid = e1.get().strip()
        ename = e2.get().strip()
        eaddress = e3.get().strip()
        etel = e4.get().strip()
        esalary = e5.get().strip()
        
        if not all([eid, ename, eaddress, etel, esalary]):
            messagebox.showerror("Error", "Please fill all employee fields")
            return
        
        try:
            esalary_float = float(esalary)
        except ValueError:
            messagebox.showerror("Error", "Salary must be a number")
            return
        
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Employee(eid, ename, eaddress, etel, esalary) VALUES (?, ?, ?, ?, ?)",
                (eid, ename, eaddress, etel, esalary_float)
            )
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Information", "Employee data saved successfully")
            clear_entries()
            refresh_employee_list()
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Employee ID already exists")
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")
    else:
        messagebox.showerror("Error", "Please select Customer or Employee")

def update():
    """Update customer or employee based on selection"""
    selected_type = v_gender.get()
    
    if selected_type == 'm':  # Customer
        cid = e1.get().strip()
        cname = e2.get().strip()
        caddress = e3.get().strip()
        ctel = e4.get().strip()
        cillness = e5.get().strip()
        
        if not cid:
            messagebox.showerror("Error", "Customer ID is required for update")
            return
        
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Customer SET cname=?, caddress=?, ctel=?, cillness=? WHERE cid=?",
                (cname, caddress, ctel, cillness, cid)
            )
            
            if cursor.rowcount == 0:
                messagebox.showerror("Error", "Customer ID not found")
            else:
                conn.commit()
                messagebox.showinfo("Information", "Customer data updated successfully")
                clear_entries()
                refresh_customer_list()
            
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")
    
    elif selected_type == 'f':  # Employee
        eid = e1.get().strip()
        ename = e2.get().strip()
        eaddress = e3.get().strip()
        etel = e4.get().strip()
        esalary = e5.get().strip()
        
        if not eid:
            messagebox.showerror("Error", "Employee ID is required for update")
            return
        
        try:
            esalary_float = float(esalary) if esalary else 0.0
        except ValueError:
            messagebox.showerror("Error", "Salary must be a number")
            return
        
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Employee SET ename=?, eaddress=?, etel=?, esalary=? WHERE eid=?",
                (ename, eaddress, etel, esalary_float, eid)
            )
            
            if cursor.rowcount == 0:
                messagebox.showerror("Error", "Employee ID not found")
            else:
                conn.commit()
                messagebox.showinfo("Information", "Employee data updated successfully")
                clear_entries()
                refresh_employee_list()
            
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")

def delete():
    """Delete customer or employee based on selection"""
    selected_type = v_gender.get()
    
    if selected_type == 'm':  # Customer
        cid = e1.get().strip()
        
        if not cid:
            messagebox.showerror("Error", "Customer ID is required for delete")
            return
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete customer {cid}?"):
            try:
                conn = db.get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Customer WHERE cid=?", (cid,))
                
                if cursor.rowcount == 0:
                    messagebox.showerror("Error", "Customer ID not found")
                else:
                    conn.commit()
                    messagebox.showinfo("Information", "Customer deleted successfully")
                    clear_entries()
                    refresh_customer_list()
                
                conn.close()
                
            except Exception as e:
                messagebox.showerror("Error", f"Database error: {e}")
    
    elif selected_type == 'f':  # Employee
        eid = e1.get().strip()
        
        if not eid:
            messagebox.showerror("Error", "Employee ID is required for delete")
            return
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete employee {eid}?"):
            try:
                conn = db.get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Employee WHERE eid=?", (eid,))
                
                if cursor.rowcount == 0:
                    messagebox.showerror("Error", "Employee ID not found")
                else:
                    conn.commit()
                    messagebox.showinfo("Information", "Employee deleted successfully")
                    clear_entries()
                    refresh_employee_list()
                
                conn.close()
                
            except Exception as e:
                messagebox.showerror("Error", f"Database error: {e}")

def refresh_customer_list():
    """Refresh the customer treeview"""
    for item in customer_tree.get_children():
        customer_tree.delete(item)
    show()

def refresh_employee_list():
    """Refresh the employee treeview"""
    for item in employee_tree.get_children():
        employee_tree.delete(item)
    show2()

def refresh_drug_list():
    """Refresh the drug treeview"""
    for item in drug_tree.get_children():
        drug_tree.delete(item)
    show3()

def show():
    """Display customer data"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT cid, cname, caddress, ctel, cillness FROM Customer")
        records = cursor.fetchall()
        
        for record in records:
            customer_tree.insert("", "end", values=record)
        
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Database error: {e}")

def show2():
    """Display employee data"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT eid, ename, eaddress, etel, esalary FROM Employee")
        records = cursor.fetchall()
        
        for record in records:
            employee_tree.insert("", "end", values=record)
        
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Database error: {e}")

def show3():
    """Display drug data"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT did, dname, dtype, eprice, eemployee FROM Drug")
        records = cursor.fetchall()
        
        for record in records:
            drug_tree.insert("", "end", values=record)
        
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Database error: {e}")

def add_drug():
    """Add drug data"""
    did = e6.get().strip()
    dname = e7.get().strip()
    dtype = e8.get().strip()
    eprice = e9.get().strip()
    eemployee = e10.get().strip()
    
    if not all([did, dname, dtype, eprice, eemployee]):
        messagebox.showerror("Error", "Please fill all drug fields")
        return
    
    try:
        eprice_float = float(eprice)
    except ValueError:
        messagebox.showerror("Error", "Price must be a number")
        return
    
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Drug(did, dname, dtype, eprice, eemployee) VALUES (?, ?, ?, ?, ?)",
            (did, dname, dtype, eprice_float, eemployee)
        )
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Information", "Drug data saved successfully")
        clear_entries()
        refresh_drug_list()
        
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Drug ID already exists")
    except Exception as e:
        messagebox.showerror("Error", f"Database error: {e}")

def update_drug():
    """Update drug data"""
    did = e6.get().strip()
    dname = e7.get().strip()
    dtype = e8.get().strip()
    eprice = e9.get().strip()
    eemployee = e10.get().strip()
    
    if not did:
        messagebox.showerror("Error", "Drug ID is required for update")
        return
    
    try:
        eprice_float = float(eprice) if eprice else 0.0
    except ValueError:
        messagebox.showerror("Error", "Price must be a number")
        return
    
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Drug SET dname=?, dtype=?, eprice=?, eemployee=? WHERE did=?",
            (dname, dtype, eprice_float, eemployee, did)
        )
        
        if cursor.rowcount == 0:
            messagebox.showerror("Error", "Drug ID not found")
        else:
            conn.commit()
            messagebox.showinfo("Information", "Drug data updated successfully")
            clear_entries()
            refresh_drug_list()
        
        conn.close()
        
    except Exception as e:
        messagebox.showerror("Error", f"Database error: {e}")

def delete_drug():
    """Delete drug data"""
    did = e6.get().strip()
    
    if not did:
        messagebox.showerror("Error", "Drug ID is required for delete")
        return
    
    if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete drug {did}?"):
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Drug WHERE did=?", (did,))
            
            if cursor.rowcount == 0:
                messagebox.showerror("Error", "Drug ID not found")
            else:
                conn.commit()
                messagebox.showinfo("Information", "Drug deleted successfully")
                clear_entries()
                refresh_drug_list()
            
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")

# Create main window
root = Tk()
root.configure(background="gray30")
root.geometry("1400x800")
root.title("DrugStore Management System")
root.option_add("*Font", 'consolas 12')

# Variable for radio button selection
v_gender = StringVar()
v_gender.set('m')  # Default to customer

# Radio buttons
Radiobutton(root, text="Customer", value="m", fg='DarkOrange1', bg='gray3',
           variable=v_gender, indicatoron=True).place(x=140, y=480)
Radiobutton(root, text='Employee', value="f", fg='DarkOrange1', bg='gray3',
           variable=v_gender, indicatoron=True).place(x=260, y=480)

# Labels and Entry fields for Customer/Employee
tk.Label(root, text="DrugStore Management System", fg='green2', bg='gray3', 
         font=(None, 24)).place(x=400, y=10)

tk.Label(root, text="Customer/Employee Section", fg='yellow', bg='gray3', 
         font=(None, 14)).place(x=80, y=60)

tk.Label(root, text="ID:", fg='green2', bg='gray3').place(x=80, y=100)
tk.Label(root, text="Name:", fg='green2', bg='gray3').place(x=80, y=130)
tk.Label(root, text="Address:", fg='green2', bg='gray3').place(x=80, y=160)
tk.Label(root, text="Tel:", fg='green2', bg='gray3').place(x=80, y=190)
tk.Label(root, text="Illness/Salary:", fg='green2', bg='gray3').place(x=80, y=220)

# Entry fields for Customer/Employee
e1 = Entry(root, width=25)
e1.place(x=180, y=100)
e2 = Entry(root, width=25)
e2.place(x=180, y=130)
e3 = Entry(root, width=25)
e3.place(x=180, y=160)
e4 = Entry(root, width=25)
e4.place(x=180, y=190)
e5 = Entry(root, width=25)
e5.place(x=180, y=220)

# Labels and Entry fields for Drug
tk.Label(root, text="Drug Section", fg='yellow', bg='gray3', 
         font=(None, 14)).place(x=450, y=60)

tk.Label(root, text="Drug ID:", fg='green2', bg='gray3').place(x=450, y=100)
tk.Label(root, text="Drug Name:", fg='green2', bg='gray3').place(x=450, y=130)
tk.Label(root, text="Drug Type:", fg='green2', bg='gray3').place(x=450, y=160)
tk.Label(root, text="Price:", fg='green2', bg='gray3').place(x=450, y=190)
tk.Label(root, text="Employee:", fg='green2', bg='gray3').place(x=450, y=220)

# Entry fields for Drug
e6 = Entry(root, width=25)
e6.place(x=550, y=100)
e7 = Entry(root, width=25)
e7.place(x=550, y=130)
e8 = Entry(root, width=25)
e8.place(x=550, y=160)
e9 = Entry(root, width=25)
e9.place(x=550, y=190)
e10 = Entry(root, width=25)
e10.place(x=550, y=220)

# Buttons for Customer/Employee
Button(root, text="ADD", command=ADD, height=2, width=8, 
       fg='white', bg='green').place(x=80, y=250)
Button(root, text="UPDATE", command=update, height=2, width=8, 
       fg='white', bg='blue').place(x=160, y=250)
Button(root, text="DELETE", command=delete, height=2, width=8, 
       fg='white', bg='red').place(x=240, y=250)

# Buttons for Drug
Button(root, text="ADD", command=add_drug, height=2, width=8, 
       fg='white', bg='green').place(x=450, y=250)
Button(root, text="UPDATE", command=update_drug, height=2, width=8, 
       fg='white', bg='blue').place(x=530, y=250)
Button(root, text="DELETE", command=delete_drug, height=2, width=8, 
       fg='white', bg='red').place(x=610, y=250)

# Clear button
Button(root, text="CLEAR", command=clear_entries, height=2, width=8, 
       fg='white', bg='orange').place(x=320, y=250)

# Treeview for Customer
tk.Label(root, text="Customers", fg='yellow', bg='gray3', 
         font=(None, 12)).place(x=50, y=320)
customer_cols = ('ID', 'Name', 'Address', 'Tel', 'Illness')
customer_tree = ttk.Treeview(root, columns=customer_cols, show='headings', height=8)

for col in customer_cols:
    customer_tree.heading(col, text=col)
    customer_tree.column(col, width=100)

customer_tree.place(x=50, y=350)
customer_tree.bind('<Double-Button-1>', GetValue)

# Treeview for Employee
tk.Label(root, text="Employees", fg='yellow', bg='gray3', 
         font=(None, 12)).place(x=50, y=540)
employee_cols = ('ID', 'Name', 'Address', 'Tel', 'Salary')
employee_tree = ttk.Treeview(root, columns=employee_cols, show='headings', height=8)

for col in employee_cols:
    employee_tree.heading(col, text=col)
    employee_tree.column(col, width=100)

employee_tree.place(x=50, y=570)
employee_tree.bind('<Double-Button-1>', GetValue)

# Treeview for Drug
tk.Label(root, text="Drugs", fg='yellow', bg='gray3', 
         font=(None, 12)).place(x=800, y=320)
drug_cols = ('ID', 'Name', 'Type', 'Price', 'Employee')
drug_tree = ttk.Treeview(root, columns=drug_cols, show='headings', height=15)

for col in drug_cols:
    drug_tree.heading(col, text=col)
    drug_tree.column(col, width=100)

drug_tree.place(x=800, y=350)
drug_tree.bind('<Double-Button-1>', GetValue)

# Load initial data
show()
show2()
show3()

root.mainloop()