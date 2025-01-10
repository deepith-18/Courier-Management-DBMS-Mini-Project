import tkinter as tk
from tkinter import messagebox as ms
from tkinter import ttk
import mysql.connector

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

        # Define tkinter variables
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

        # Style configuration
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 13), padding=10)
        self.style.configure('TLabel', font=('Arial', 15), padding=10)
        self.style.configure('TEntry', font=('Arial', 15), padding=10)

        # Call the method to create widgets
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
        self.pagination_label.pack(side=tk.LEFT, padx=5)
        tk.Button(self.pagination_frame, text="Previous", command=self.prev_page).pack(side=tk.LEFT, padx=5)
        tk.Button(self.pagination_frame, text="Next", command=self.next_page).pack(side=tk.LEFT, padx=5)

        self.update_pagination()

    def update_tree(self, rows):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in rows:
            self.tree.insert('', 'end', values=row)

    def search_user(self):
        search_query = self.search_var.get()
        db = mysql.connector.connect(
            host="Deepu-2004",
            user="deepith",
            password="what798",
            database="courier_management"
        )
        c = db.cursor()
        c.execute('SELECT * FROM user WHERE username LIKE %s OR mobile LIKE %s', (f'%{search_query}%', f'%{search_query}%'))
        rows = c.fetchall()
        self.update_tree(rows)
        db.close()

    def sort_tree(self, column, reverse):
        rows = [(self.tree.set(k, column), k) for k in self.tree.get_children('')]
        rows.sort(reverse=reverse)
        for index, (val, k) in enumerate(rows):
            self.tree.move(k, '', index)
        self.tree.heading(column, command=lambda: self.sort_tree(column, not reverse))

    def prev_page(self):
        self.current_page = max(self.current_page - 1, 1)
        self.update_user_data()

    def next_page(self):
        self.current_page += 1
        self.update_user_data()

    def update_pagination(self):
        self.pagination_label.config(text=f"Page {self.current_page}")

    def widgets(self):
        # Initialize the main window
        self.master.title("Courier Management System")
        self.master.geometry("800x600")

        # Header
        self.head = tk.Label(self.master, text='Login', font=('Arial', 40, 'bold'))
        self.head.pack(pady=20)

        # Frames
        self.logf = tk.Frame(self.master, padx=10, pady=10)
        self.crf = tk.Frame(self.master, padx=10, pady=10)
        self.mainf = tk.Frame(self.master, padx=10, pady=10)
        self.consi = tk.Frame(self.master, padx=10, pady=10)

        # Login Frame
        tk.Label(self.logf, text="Username:", font=('Arial', 15)).pack()
        tk.Entry(self.logf, textvariable=self.username, font=('Arial', 15)).pack()
        tk.Label(self.logf, text="Password:", font=('Arial', 15)).pack()
        tk.Entry(self.logf, textvariable=self.password, show="*", font=('Arial', 15)).pack()
        tk.Button(self.logf, text="Login", command=self.login).pack(pady=10)
        tk.Button(self.logf, text="Create Account", command=self.cr).pack(pady=10)

        # Create Account Frame
        tk.Label(self.crf, text="New Username:", font=('Arial', 15)).pack()
        tk.Entry(self.crf, textvariable=self.n_username, font=('Arial', 15)).pack()
        tk.Label(self.crf, text="New Password:", font=('Arial', 15)).pack()
        tk.Entry(self.crf, textvariable=self.n_password, show="*", font=('Arial', 15)).pack()
        tk.Label(self.crf, text="Mobile:", font=('Arial', 15)).pack()
        tk.Entry(self.crf, textvariable=self.n_mobile, font=('Arial', 15)).pack()
        tk.Button(self.crf, text="Create", command=self.new_user).pack(pady=10)
        tk.Button(self.crf, text="Back", command=self.log).pack(pady=10)

        # Main Menu Frame
        tk.Button(self.mainf, text="Show User Data", command=self.show_user_data).pack(pady=10)
        tk.Button(self.mainf, text="Track Consignment", command=self.consignment).pack(pady=10)
        tk.Button(self.mainf, text="Place Order", command=self.place_order).pack(pady=10)
        tk.Button(self.mainf, text="Log Out", command=self.log).pack(pady=10)

        # Set the initial frame
        self.logf.pack()

# Create the database and tables if they don't exist
create_db()

# Create and run the application
root = tk.Tk()
app = main(root)
root.mainloop()
