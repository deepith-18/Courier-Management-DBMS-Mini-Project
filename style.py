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
        self.product_status = tk.StringVar(value='Pending')

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
            self.track()
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
        find_user = ('SELECT * FROM user WHERE mobile = %s')
        c.execute(find_user, (self.mobile11.get(),))
        result = c.fetchall()
        if result:
            self.track()
            self.crff.pack_forget()
            self.head['text'] = self.username.get() + '\n Your Product Details'
            self.consi.pack()
        else:
            ms.showerror('Oops!', 'Mobile Number Not Found.')
        db.close()

    def track1(self):
        self.consi.pack_forget()
        self.head['text'] = self.username.get() + '\n Track your Product'
        self.crff.pack()

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

    def track(self):
        self.logf.pack_forget()
        self.head['text'] = self.username.get() + '\n Track your Product'
        self.crff.pack()

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
        self.update_pagination(filtered_rows)

    def sort_tree(self, col, reverse):
        rows = [(self.tree.set(item, col), item) for item in self.tree.get_children('')]
        rows.sort(reverse=reverse)
        for index, (val, item) in enumerate(rows):
            self.tree.move(item, '', index)
        self.tree.heading(col, command=lambda: self.sort_tree(col, not reverse))

    def update_tree(self, rows):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in rows:
            self.tree.insert('', 'end', values=row)

    def update_pagination(self, rows=None):
        if rows is None:
            rows = self.rows
        start_index = self.current_page * self.rows_per_page
        end_index = start_index + self.rows_per_page
        self.update_tree(rows[start_index:end_index])
        self.pagination_label.config(text=f"Page {self.current_page + 1} of {len(rows) // self.rows_per_page + 1}")

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_pagination()

    def next_page(self):
        if (self.current_page + 1) * self.rows_per_page < len(self.rows):
            self.current_page += 1
            self.update_pagination()

    def update_user(self):
        db = mysql.connector.connect(
            host="Deepu-2004",
            user="deepith",
            password="what798",
            database="courier_management"
        )
        c = db.cursor()
        if self.n_username.get() and self.n_password.get() and self.n_mobile.get():
            update_user = 'UPDATE user SET password=%s, mobile=%s WHERE username=%s'
            c.execute(update_user, (self.n_password.get(), self.n_mobile.get(), self.n_username.get()))
            db.commit()
            ms.showinfo('Success!', 'User Details Updated!')
            self.log()
        else:
            ms.showerror('Error!', 'Please Enter the details.')
        db.close()

    def delete_user(self):
        db = mysql.connector.connect(
            host="Deepu-2004",
            user="deepith",
            password="what798",
            database="courier_management"
        )
        c = db.cursor()
        if self.n_username.get():
            delete_user = 'DELETE FROM user WHERE username=%s'
            c.execute(delete_user, (self.n_username.get(),))
            db.commit()
            ms.showinfo('Success!', 'User Deleted!')
            self.log()
        else:
            ms.showerror('Error!', 'Please Enter the Username.')
        db.close()

    def go_home(self):
        self.crff.pack_forget()
        self.consi.pack_forget()
        self.log()
        
    def widgets(self):
        self.master.configure(bg='#f0f0f0')
        self.head = tk.Label(self.master, text='Login', font=('Arial', 35, 'bold'), pady=10, bg='#ffd700')
        self.head.pack(fill=tk.X)

        self.logf = tk.Frame(self.master, padx=10, pady=10, bg='#f0f0f0')
        tk.Label(self.logf, text='Username: ', font=('Arial', 20, 'bold'), bg='#f0f0f0').grid(sticky=tk.W)
        ttk.Entry(self.logf, textvariable=self.username, style='TEntry', width=30).grid(row=0, column=1)
        tk.Label(self.logf, text='Password: ', font=('Arial', 20, 'bold'), bg='#f0f0f0').grid(sticky=tk.W)
        ttk.Entry(self.logf, textvariable=self.password, style='TEntry', width=30, show='*').grid(row=1, column=1)
        ttk.Button(self.logf, text='Login', command=self.login).grid(row=2, column=0)
        ttk.Button(self.logf, text='Create Account', command=self.cr).grid(row=2, column=1)
        ttk.Button(self.logf, text='Show User Data', command=self.show_user_data).grid(row=3, columnspan=2)
        self.logf.pack()

        self.crf = tk.Frame(self.master, padx=10, pady=10, bg='#f0f0f0')
        tk.Label(self.crf, text='Username: ', font=('Arial', 15, 'bold'), bg='#f0f0f0').grid(sticky=tk.W)
        ttk.Entry(self.crf, textvariable=self.n_username, style='TEntry', width=30).grid(row=0, column=1)
        tk.Label(self.crf, text='Password: ', font=('Arial', 15, 'bold'), bg='#f0f0f0').grid(sticky=tk.W)
        ttk.Entry(self.crf, textvariable=self.n_password, style='TEntry', width=30, show='*').grid(row=1, column=1)
        tk.Label(self.crf, text='Mobile No.: ', font=('Arial', 15, 'bold'), bg='#f0f0f0').grid(sticky=tk.W)
        ttk.Entry(self.crf, textvariable=self.n_mobile, style='TEntry', width=30).grid(row=2, column=1)
        ttk.Button(self.crf, text='Create Account', command=self.new_user).grid(row=3, columnspan=2)
        ttk.Button(self.crf, text='Update Account', command=self.update_user).grid(row=4, column=0)
        ttk.Button(self.crf, text='Delete Account', command=self.delete_user).grid(row=4, column=1)
        ttk.Button(self.crf, text='Go to Login', command=self.log).grid(row=5, columnspan=2)
        ttk.Button(self.crf, text='Home', command=self.go_home).grid(row=6, columnspan=2)

        self.crff = tk.Frame(self.master, padx=10, pady=10, bg='#f0f0f0')
        tk.Label(self.crff, text='Consignment No: ', font=('Arial', 15, 'bold'), bg='#f0f0f0').grid(sticky=tk.W)
        ttk.Entry(self.crff, style='TEntry', width=30).grid(row=0, column=1)
        tk.Label(self.crff, text='Mobile no:', font=('Arial', 15, 'bold'), bg='#f0f0f0').grid(sticky=tk.W)
        ttk.Entry(self.crff, textvariable=self.mobile11, style='TEntry', width=30).grid(row=1, column=1)
        ttk.Button(self.crff, text='Track', command=self.consignment).grid(row=2, columnspan=2)
        ttk.Button(self.crff, text='Home', command=self.go_home).grid(row=3, columnspan=2)

        self.consi = tk.Frame(self.master, padx=10, pady=10, bg='#f0f0f0')
        tk.Label(self.consi, text='Product ID:', font=('Arial', 15, 'bold'), bg='#f0f0f0').grid(sticky=tk.W)
        tk.Label(self.consi, text=random.randint(565154, 99994216), font=('Arial', 13, 'bold'), bg='#f0f0f0').grid(row=0, column=1)
        L = ['Bag', 'Colgate', 'Shoe', 'Redmi 2', 'Jeans', 'Parrot', 'Mac', 'iPad', 'Pen', 'Book', 'Shirt']
        f = random.randint(0, 10)
        tk.Label(self.consi, text='Product name: ', font=('Arial', 15, 'bold'), bg='#f0f0f0').grid(sticky=tk.W)
        tk.Label(self.consi, text=L[f], font=('Arial', 13, 'bold'), bg='#f0f0f0').grid(row=1, column=1)
        tk.Label(self.consi, text='Product Status: ', font=('Arial', 15, 'bold'), bg='#f0f0f0').grid(sticky=tk.W)
        tk.Label(self.consi, textvariable=self.product_status, font=('Arial', 13, 'bold'), bg='#f0f0f0').grid(row=2, column=1)
        tk.Label(self.consi, font=('Arial', 13, 'bold'), text='Thanks for Exploring!', bg='#f0f0f0').grid(row=3, columnspan=2)
        tk.Label(self.consi, text='Comments:', font=('Arial', 13, 'bold'), bg='#f0f0f0').grid(row=4, column=0, padx=5, sticky='sw')
        ttk.Entry(self.consi, style='TEntry', width=30).grid(row=4, column=1)
        ttk.Button(self.consi, text='Back', command=self.track1).grid(row=5, column=0)
        ttk.Button(self.consi, text='Home', command=self.go_home).grid(row=5, column=1)

if __name__ == '__main__':
    create_db()
    root = tk.Tk()
    root.title('Track Consignment')
    root.geometry('800x750+300+300')
    app = main(root)
    root.mainloop()
