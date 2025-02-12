import tkinter as tk
import datetime
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
     today = datetime.date.today().isoformat()
     db = mysql.connector.connect(
        host="Deepu-2004",
        user="deepith",
        password="what798",
        database="courier_management"
     )
     c = db.cursor()
     insert = 'INSERT INTO orders(username, mobile, address, date, product_id, product_name, quantity) VALUES(%s, %s, %s, %s, %s, %s, %s)'
     c.execute(insert, (self.place_username.get(), self.place_mobile.get(), self.place_address.get(), today, self.place_product_id.get(), self.place_product_name.get(), self.place_quantity.get()))
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

    def search_user(self):
        query = self.search_var.get().lower()
        filtered_rows = [row for row in self.rows if query in row[0].lower() or query in row[1].lower() or query in row[2].lower()]
        self.update_tree(filtered_rows)
        self.current_page = 0
        self.update_pagination()

    def sort_tree(self, col, reverse):
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        data.sort(reverse=reverse)
        for index, (_, child) in enumerate(data):
            self.tree.move(child, '', index)
        self.tree.heading(col, command=lambda: self.sort_tree(col, not reverse))

    def update_tree(self, rows):
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert('', tk.END, values=row)

    def update_pagination(self):
        start_index = self.current_page * self.rows_per_page
        end_index = start_index + self.rows_per_page
        paginated_rows = self.rows[start_index:end_index]
        self.update_tree(paginated_rows)
        self.pagination_label.config(text=f"Showing {start_index + 1} to {end_index} of {len(self.rows)} entries")

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_pagination()

    def next_page(self):
        if (self.current_page + 1) * self.rows_per_page < len(self.rows):
            self.current_page += 1
            self.update_pagination()

    def place(self):
     self.head['text'] = self.username.get() + '\n Place Order'
     self.mainf.pack_forget()
     self.placef.pack()
     ttk.Button(self.placef, text='Home', command=self.go_home).grid(row=8, columnspan=2, pady=10)



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

     self.orders_window = tk.Toplevel(self.master)
     self.orders_window.title('Orders')
     self.orders_window.geometry('800x600')

     columns = ('ID', 'Username', 'Mobile', 'Address', 'Date', 'Product ID', 'Product Name', 'Quantity')
     tree = ttk.Treeview(self.orders_window, columns=columns, show='headings')
     for col in columns:
         tree.heading(col, text=col)
     tree.pack(fill=tk.BOTH, expand=True)

     for row in rows:
        tree.insert('', tk.END, values=row)

     ttk.Button(self.orders_window, text='Home', command=self.go_home).pack(pady=10)

     db.close()


    def track(self):
     self.mainf.pack_forget()
     self.head['text'] = self.username.get() + '\n Tracking Consignment'
     self.crff.pack()
     ttk.Button(self.crff, text='Home', command=self.go_home).grid(row=2, columnspan=2, pady=10)



    def widgets(self):
        self.head = tk.Label(self.master, text='Login', font=('Arial', 35), pady=10, bg='#ffd700')
        self.head.pack(fill=tk.X)
        self.logf = tk.Frame(self.master, padx=10, pady=10)
        tk.Label(self.logf, text='Username: ', font=('Arial', 20), pady=5, padx=5).grid(sticky=tk.W)
        tk.Entry(self.logf, textvariable=self.username, font=('Arial', 15)).grid(row=0, column=1)
        tk.Label(self.logf, text='Password: ', font=('Arial', 20), pady=5, padx=5).grid(sticky=tk.W)
        tk.Entry(self.logf, textvariable=self.password, font=('Arial', 15), show='*').grid(row=1, column=1)
        ttk.Button(self.logf, text=' Login ', command=self.login).grid(row=2, columnspan=2, pady=10)
        tk.Label(self.logf, text='New User? Create Account', font=('Arial', 12)).grid(row=3, columnspan=2)
        ttk.Button(self.logf, text=' Create Account ', command=self.cr).grid(row=4, columnspan=2, pady=10)
        self.logf.pack()

        self.crf = tk.Frame(self.master, padx=10, pady=10)
        tk.Label(self.crf, text='Username: ', font=('Arial', 20), pady=5, padx=5).grid(sticky=tk.W)
        tk.Entry(self.crf, textvariable=self.n_username, font=('Arial', 15)).grid(row=0, column=1)
        tk.Label(self.crf, text='Password: ', font=('Arial', 20), pady=5, padx=5).grid(sticky=tk.W)
        tk.Entry(self.crf, textvariable=self.n_password, font=('Arial', 15), show='*').grid(row=1, column=1)
        tk.Label(self.crf, text='Mobile No: ', font=('Arial', 20), pady=5, padx=5).grid(sticky=tk.W)
        tk.Entry(self.crf, textvariable=self.n_mobile, font=('Arial', 15)).grid(row=2, column=1)
        ttk.Button(self.crf, text='Create Account', command=self.new_user).grid(row=3, columnspan=2, pady=10)
        tk.Label(self.crf, text='Already a User? Go to Login', font=('Arial', 12)).grid(row=4, columnspan=2)
        ttk.Button(self.crf, text=' Login ', command=self.log).grid(row=5, columnspan=2, pady=10)

        self.mainf = tk.Frame(self.master, padx=10, pady=10)
        ttk.Button(self.mainf, text='Place Order', command=self.place).pack(pady=10)
        ttk.Button(self.mainf, text='Track Consignment', command=self.track).pack(pady=10)
        ttk.Button(self.mainf, text='Show Orders', command=self.show_orders).pack(pady=10)
        ttk.Button(self.mainf, text='Show Users Data', command=self.show_user_data).pack(pady=10)

        self.placef = tk.Frame(self.master, padx=10, pady=10)
        tk.Label(self.placef, text='Username: ', font=('Arial', 20), pady=5, padx=5).grid(sticky=tk.W)
        tk.Entry(self.placef, textvariable=self.place_username, font=('Arial', 15)).grid(row=0, column=1)
        tk.Label(self.placef, text='Mobile No: ', font=('Arial', 20), pady=5, padx=5).grid(sticky=tk.W)
        tk.Entry(self.placef, textvariable=self.place_mobile, font=('Arial', 15)).grid(row=1, column=1)
        tk.Label(self.placef, text='Address: ', font=('Arial', 20), pady=5, padx=5).grid(sticky=tk.W)
        tk.Entry(self.placef, textvariable=self.place_address, font=('Arial', 15)).grid(row=2, column=1)
        tk.Label(self.placef, text='Date: ', font=('Arial', 20), pady=5, padx=5).grid(sticky=tk.W)
        tk.Entry(self.placef, textvariable=self.place_date, font=('Arial', 15)).grid(row=3, column=1)
        tk.Label(self.placef, text='Product ID: ', font=('Arial', 20), pady=5, padx=5).grid(sticky=tk.W)
        tk.Entry(self.placef, textvariable=self.place_product_id, font=('Arial', 15)).grid(row=4, column=1)
        tk.Label(self.placef, text='Product Name: ', font=('Arial', 20), pady=5, padx=5).grid(sticky=tk.W)
        tk.Entry(self.placef, textvariable=self.place_product_name, font=('Arial', 15)).grid(row=5, column=1)
        tk.Label(self.placef, text='Quantity: ', font=('Arial', 20), pady=5, padx=5).grid(sticky=tk.W)
        tk.Entry(self.placef, textvariable=self.place_quantity, font=('Arial', 15)).grid(row=6, column=1)
        ttk.Button(self.placef, text='Submit', command=self.place_order).grid(row=7, columnspan=2, pady=10)

        self.consi = tk.Frame(self.master, padx=10, pady=10)

        self.crff = tk.Frame(self.master, padx=10, pady=10)
        tk.Label(self.crff, text='Enter Your Mobile No: ', font=('Arial', 20), pady=5, padx=5).grid(sticky=tk.W)
        tk.Entry(self.crff, textvariable=self.mobile11, font=('Arial', 15)).grid(row=0, column=1)
        ttk.Button(self.crff, text='Submit', command=self.consignment).grid(row=1, columnspan=2, pady=10)

    def go_home(self):
     self.consi.pack_forget()  # Hide the consignment frame
     self.placef.pack_forget()  # Hide the place order frame
     self.crff.pack_forget()   # Hide the consignment tracking frame
     self.orders_window.destroy() if hasattr(self, 'orders_window') else None  # Close the orders window if open
     self.user_data_window.destroy() if hasattr(self, 'user_data_window') else None  # Close the user data window if open
     self.head['text'] = self.username.get() + '\n Main Menu'
     self.mainf.pack()  # Show the main menu frame



if __name__ == '__main__':
    root = tk.Tk()
    root.title('Courier Management System')
    root.geometry('800x600')
    create_db()
    app = main(root)
    root.mainloop()
