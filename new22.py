import tkinter as tk
from tkinter import messagebox as ms
from tkinter import ttk
import mysql.connector
import random

# Database connection
def create_db():
    db = mysql.connector.connect(
        host="Deepu-2004",
        user="deepith",       # replace with your MySQL username
        password="what798"    # replace with your MySQL password
    )
    c = db.cursor()
    c.execute("CREATE DATABASE IF NOT EXISTS courier_management")
    c.execute("USE courier_management")
    c.execute('''CREATE TABLE IF NOT EXISTS user (
        username VARCHAR(50) NOT NULL,
        password VARCHAR(50) NOT NULL,
        mobile VARCHAR(15) NOT NULL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50),
        mobile VARCHAR(15),
        address TEXT,
        date DATE,
        product_id VARCHAR(50),
        product_name VARCHAR(100),
        quantity INT
    )''')
    db.commit()
    db.close()

class main:
    def __init__(self, master):
        self.master = master

        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.n_username = tk.StringVar()
        self.n_password = tk.StringVar()
        self.n_mobile = tk.StringVar()
        self.mobile11 = tk.StringVar()
        self.place_username = tk.StringVar()
        self.place_mobile = tk.StringVar()
        self.place_address = tk.StringVar()
        self.place_date = tk.StringVar()
        self.place_product_id = tk.StringVar()
        self.place_product_name = tk.StringVar()
        self.place_quantity = tk.StringVar()

        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 13), padding=10)
        self.style.configure('TLabel', font=('Arial', 15), padding=10)
        self.style.configure('TEntry', font=('Arial', 15), padding=10)
        
        self.widgets()

    def login(self):
        db = mysql.connector.connect(
            host="Deepu-2004",
            user="deepith",
            password="what798",
            database="courier_management"
        )
        c = db.cursor()
        find_user = ('SELECT * FROM user WHERE username = %s and password = %s')
        c.execute(find_user, (self.username.get(), self.password.get()))
        result = c.fetchall()

        if result:
            self.main_menu()
        else:
            ms.showerror('Oops!', 'Username Not Found.')
        db.close()

    def new_user(self):
        db = mysql.connector.connect(
            host="Deepu-2004",
            user="deepith",
            password="what798",
            database="courier_management"
        )
        c = db.cursor()
        if self.n_username.get() and self.n_password.get() and self.n_mobile.get():
            find_user = ('SELECT * FROM user WHERE username = %s')
            c.execute(find_user, (self.n_username.get(),))
            if c.fetchall():
                ms.showerror('Error!', 'Username Taken Try a Different One.')
            else:
                insert = 'INSERT INTO user(username, password, mobile) VALUES(%s, %s, %s)'
                c.execute(insert, (self.n_username.get(), self.n_password.get(), self.n_mobile.get()))
                db.commit()
                ms.showinfo('Success!', 'Account Created!')
                self.log()
        else:
            ms.showerror('Error!', 'Please Enter the details.')
        db.close()

    def consignment(self):
        db = mysql.connector.connect(
            host="Deepu-2004",
            user="deepith",
            password="what798",
            database="courier_management"
        )
        c = db.cursor()
        find_order = ('SELECT * FROM orders WHERE mobile = %s ORDER BY id DESC LIMIT 1')
        c.execute(find_order, (self.mobile11.get(),))
        result = c.fetchall()
        if result:
            order = result[0]
            self.track()
            self.crff.pack_forget()
            self.head['text'] = self.username.get() + '\n Your Product Details'
            self.consi.pack()
            # Update the consignment frame with order details
            for widget in self.consi.winfo_children():
                widget.destroy()
            tk.Label(self.consi, text='Tracking Consignment', font=('Arial', 35, 'bold'), pady=10, bg='#ffd700').pack(fill=tk.X)
            tk.Label(self.consi, text=f'Product ID: {order[5]}', font=('Arial', 20, 'bold'), bg='#f0f0f0').pack(fill=tk.X)
            tk.Label(self.consi, text=f'Product Name: {order[6]}', font=('Arial', 20, 'bold'), bg='#f0f0f0').pack(fill=tk.X)
            tk.Label(self.consi, text=f'Quantity: {order[7]}', font=('Arial', 20, 'bold'), bg='#f0f0f0').pack(fill=tk.X)
            tk.Label(self.consi, text=f'Address: {order[3]}', font=('Arial', 20, 'bold'), bg='#f0f0f0').pack(fill=tk.X)
            tk.Label(self.consi, text=f'Date: {order[4]}', font=('Arial', 20, 'bold'), bg='#f0f0f0').pack(fill=tk.X)
            ttk.Button(self.consi, text='Home', command=self.go_home).pack(pady=10)
        else:
            ms.showerror('Oops!', 'Mobile Number Not Found.')
        db.close()

    def place_order(self):
        db = mysql.connector.connect(
            host="Deepu-2004",
            user="deepith",
            password="what798",
            database="courier_management"
        )
        c = db.cursor()
        insert = 'INSERT INTO orders(username, mobile, address, date, product_id, product_name, quantity) VALUES(%s, %s, %s, %s, %s, %s, %s)'
        c.execute(insert, (self.place_username.get(), self.place_mobile.get(), self.place_address.get(), self.place_date.get(), self.place_product_id.get(), self.place_product_name.get(), self.place_quantity.get()))
        db.commit()
        ms.showinfo('Success!', 'Order Placed!')
        db.close()
    
    def log(self):
        self.username.set('')
        self.password.set('')
        self.crf.pack_forget()
        self.head['text'] = 'Login'
        self.logf.pack()

    def cr(self):
        self.n_username.set('')
        self.n_password.set('')
        self.logf.pack_forget()
        self.head['text'] = 'Create Account'
        self.crf.pack()

    def main_menu(self):
        self.logf.pack_forget()
        self.head['text'] = self.username.get() + '\n Main Menu'
        self.mainf.pack()

    def show_user_data(self):
        db = mysql.connector.connect(
            host="Deepu-2004",
            user="deepith",
            password="what798",
            database="courier_management"
        )
        c = db.cursor()
        c.execute('SELECT * FROM user')
        rows = c.fetchall()

        self.user_data_window = tk.Toplevel(self.master)
        self.user_data_window.title('User Data')
        self.user_data_window.geometry('800x600')

        self.search_var = tk.StringVar()

        search_frame = tk.Frame(self.user_data_window, padx=10, pady=10)
        search_frame.pack(fill=tk.X)
        tk.Label(search_frame, text="Search: ", font=('Arial', 12)).pack(side=tk.LEFT)
        tk.Entry(search_frame, textvariable=self.search_var, font=('Arial', 12)).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Search", command=self.search_user, font=('Arial', 12)).pack(side=tk.LEFT)

        columns = ('Username', 'Password', 'Mobile')
        self.tree = ttk.Treeview(self.user_data_window, columns=columns, show='headings')
        self.tree.heading('Username', text='Username', command=lambda: self.sort_tree('Username', False))
        self.tree.heading('Password', text='Password', command=lambda: self.sort_tree('Password', False))
        self.tree.heading('Mobile', text='Mobile', command=lambda: self.sort_tree('Mobile', False))
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.update_tree(rows)

        self.pagination_frame = tk.Frame(self.user_data_window)
        self.pagination_frame.pack(fill=tk.X)
        self.pagination_label = tk.Label(self.pagination_frame, text="")
        self.pagination_label.pack(side=tk.LEFT)
        tk.Button(self.pagination_frame, text="Previous", command=self.previous_page).pack(side=tk.LEFT)
        tk.Button(self.pagination_frame, text="Next", command=self.next_page).pack(side=tk.LEFT)

        self.rows = rows
        self.current_page = 0
        self.rows_per_page = 10

        self.update_pagination()

        db.close()

    def show_orders(self):
        db = mysql.connector.connect(
            host="Deepu-2004",
            user="deepith",
            password="what798",
            database="courier_management"
        )
        c = db.cursor()
        c.execute('SELECT * FROM orders')
        rows = c.fetchall()

        self.order_data_window = tk.Toplevel(self.master)
        self.order_data_window.title('Order Data')
        self.order_data_window.geometry('800x600')

        columns = ('ID', 'Username', 'Mobile', 'Address', 'Date', 'Product ID', 'Product Name', 'Quantity')
        self.tree = ttk.Treeview(self.order_data_window, columns=columns, show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Username', text='Username')
        self.tree.heading('Mobile', text='Mobile')
        self.tree.heading('Address', text='Address')
        self.tree.heading('Date', text='Date')
        self.tree.heading('Product ID', text='Product ID')
        self.tree.heading('Product Name', text='Product Name')
        self.tree.heading('Quantity', text='Quantity')
        self.tree.pack(fill=tk.BOTH, expand=True)

        for row in rows:
            self.tree.insert('', tk.END, values=row)

        db.close()

    def go_home(self):
        self.consi.pack_forget()
        self.main_menu()

    def widgets(self):
        self.head = tk.Label(self.master, text='LOGIN', font=('Arial', 35), pady=10)
        self.head.pack()

        self.logf = tk.Frame(self.master, padx=10, pady=10)
        tk.Label(self.logf, text='Username: ', font=('Arial', 20), bd=15).grid(row=0, sticky=tk.W)
        tk.Entry(self.logf, textvariable=self.username, font=('Arial', 15)).grid(row=0, column=1)
        tk.Label(self.logf, text='Password: ', font=('Arial', 20), bd=15).grid(row=1, sticky=tk.W)
        tk.Entry(self.logf, textvariable=self.password, font=('Arial', 15), show='*').grid(row=1, column=1)
        tk.Button(self.logf, text='Login', command=self.login, font=('Arial', 15), padx=5, pady=5).grid(row=2, column=1)
        tk.Button(self.logf, text='Create Account', command=self.cr, font=('Arial', 15), padx=5, pady=5).grid(row=2, column=0)
        self.logf.pack()

        self.crf = tk.Frame(self.master, padx=10, pady=10)
        tk.Label(self.crf, text='Username: ', font=('Arial', 20), bd=15).grid(row=0, sticky=tk.W)
        tk.Entry(self.crf, textvariable=self.n_username, font=('Arial', 15)).grid(row=0, column=1)
        tk.Label(self.crf, text='Password: ', font=('Arial', 20), bd=15).grid(row=1, sticky=tk.W)
        tk.Entry(self.crf, textvariable=self.n_password, font=('Arial', 15), show='*').grid(row=1, column=1)
        tk.Label(self.crf, text='Mobile: ', font=('Arial', 20), bd=15).grid(row=2, sticky=tk.W)
        tk.Entry(self.crf, textvariable=self.n_mobile, font=('Arial', 15)).grid(row=2, column=1)
        tk.Button(self.crf, text='Create Account', command=self.new_user, font=('Arial', 15), padx=5, pady=5).grid(row=3, column=1)
        tk.Button(self.crf, text='Go to Login', command=self.log, font=('Arial', 15), padx=5, pady=5).grid(row=3, column=0)
        
        self.mainf = tk.Frame(self.master, padx=10, pady=10)
        tk.Button(self.mainf, text='Place Courier', command=self.order, font=('Arial', 15), width=20, pady=10).grid(row=0)
        tk.Button(self.mainf, text='Track Order', command=self.tracking, font=('Arial', 15), width=20, pady=10).grid(row=1)
        tk.Button(self.mainf, text='Show Orders', command=self.show_orders, font=('Arial', 15), width=20, pady=10).grid(row=2)
        tk.Button(self.mainf, text='Feedback', command=self.feedback, font=('Arial', 15), width=20, pady=10).grid(row=3)
        tk.Button(self.mainf, text='Logout', command=self.logout, font=('Arial', 15), width=20, pady=10).grid(row=4)
        self.mainf.pack_forget()

        self.consi = tk.Frame(self.master, padx=10, pady=10)

        self.crff = tk.Frame(self.master, padx=10, pady=10)
        tk.Label(self.crff, text='Enter Mobile Number: ', font=('Arial', 20), bd=15).grid(row=0, sticky=tk.W)
        tk.Entry(self.crff, textvariable=self.mobile11, font=('Arial', 15)).grid(row=0, column=1)
        tk.Button(self.crff, text='Search', command=self.consignment, font=('Arial', 15), padx=5, pady=5).grid(row=1, column=1)
        tk.Button(self.crff, text='Back', command=self.main_menu, font=('Arial', 15), padx=5, pady=5).grid(row=1, column=0)
        
        self.crff.pack_forget()
        
        self.orff = tk.Frame(self.master, padx=10, pady=10)
        tk.Label(self.orff, text='Username: ', font=('Arial', 20), bd=15).grid(row=0, sticky=tk.W)
        tk.Entry(self.orff, textvariable=self.place_username, font=('Arial', 15)).grid(row=0, column=1)
        tk.Label(self.orff, text='Mobile: ', font=('Arial', 20), bd=15).grid(row=1, sticky=tk.W)
        tk.Entry(self.orff, textvariable=self.place_mobile, font=('Arial', 15)).grid(row=1, column=1)
        tk.Label(self.orff, text='Address: ', font=('Arial', 20), bd=15).grid(row=2, sticky=tk.W)
        tk.Entry(self.orff, textvariable=self.place_address, font=('Arial', 15)).grid(row=2, column=1)
        tk.Label(self.orff, text='Date: ', font=('Arial', 20), bd=15).grid(row=3, sticky=tk.W)
        tk.Entry(self.orff, textvariable=self.place_date, font=('Arial', 15)).grid(row=3, column=1)
        tk.Label(self.orff, text='Product ID: ', font=('Arial', 20), bd=15).grid(row=4, sticky=tk.W)
        tk.Entry(self.orff, textvariable=self.place_product_id, font=('Arial', 15)).grid(row=4, column=1)
        tk.Label(self.orff, text='Product Name: ', font=('Arial', 20), bd=15).grid(row=5, sticky=tk.W)
        tk.Entry(self.orff, textvariable=self.place_product_name, font=('Arial', 15)).grid(row=5, column=1)
        tk.Label(self.orff, text='Quantity: ', font=('Arial', 20), bd=15).grid(row=6, sticky=tk.W)
        tk.Entry(self.orff, textvariable=self.place_quantity, font=('Arial', 15)).grid(row=6, column=1)
        tk.Button(self.orff, text='Place Order', command=self.place_order, font=('Arial', 15), padx=5, pady=5).grid(row=7, column=1)
        tk.Button(self.orff, text='Back', command=self.go_back, font=('Arial', 15), padx=5, pady=5).grid(row=7, column=0)

    def order(self):
        self.mainf.pack_forget()
        self.head['text'] = self.username.get() + '\n Place Courier'
        self.orff.pack()

    def tracking(self):
        self.mainf.pack_forget()
        self.head['text'] = self.username.get() + '\n Track Order'
        self.crff.pack()

    def go_back(self):
        self.orff.pack_forget()
        self.main_menu()

    def logout(self):
        self.mainf.pack_forget()
        self.head['text'] = 'LOGIN'
        self.logf.pack()

    def feedback(self):
        self.mainf.pack_forget()
        self.head['text'] = self.username.get() + '\n Feedback'
        # Add your feedback form code here
        self.mainf.pack()

root = tk.Tk()
root.geometry('500x500')
create_db()
main(root)
root.mainloop()
