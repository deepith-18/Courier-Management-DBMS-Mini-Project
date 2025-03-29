Requirements (Prerequisites)

Before you start, ensure you have the following installed on your computer:

    Python 3: Version 3.x is required. Tkinter (the GUI library) is usually included with standard Python 3 installations.

        Verify: Open terminal/command prompt: python --version or python3 --version

        Download: python.org

    MySQL Server: A running MySQL database server instance.

        Verify: Check if the MySQL service is running.

        Download/Install: Official MySQL website. Remember your access credentials (host, username, password).

    MySQL Connector for Python: The Python library to connect to MySQL. (Installation step below).

File Structure

Create a dedicated folder for your project. Inside that folder, place your Python script:

      
CourierManagementSystem/
|
└── main.py         # Your Python script file
└── README.md       # Optional: The readme file

    

IGNORE_WHEN_COPYING_START
Use code with caution.
IGNORE_WHEN_COPYING_END
Setup Steps

Step 1: Place the Code

    Make sure the main.py file (containing your Python code) is inside your project folder (e.g., CourierManagementSystem/).

Step 2: Install Required Python Library

    Open your terminal or command prompt.

    Navigate (cd) into your project folder:

          
    cd path/to/CourierManagementSystem

        

    IGNORE_WHEN_COPYING_START

Use code with caution.Bash
IGNORE_WHEN_COPYING_END

(Replace path/to/ with the actual path)

Install the MySQL connector library:

      
pip install mysql-connector-python

    

IGNORE_WHEN_COPYING_START

    Use code with caution.Bash
    IGNORE_WHEN_COPYING_END

    (Use pip3 if pip doesn't work for your Python 3 installation)

Step 3: Configure Database Connection (IMPORTANT!)

    Your Python script (main.py) needs your specific MySQL connection details.

    Open the main.py file in a text editor.

    Locate every instance where mysql.connector.connect(...) is called. It will look similar to this:

          
    # Example structure - FIND THIS PATTERN in your main.py
    db = mysql.connector.connect(
        host="PLACEHOLDER_HOST",      # <-- YOU MUST CHANGE THIS
        user="PLACEHOLDER_USER",      # <-- YOU MUST CHANGE THIS
        password="PLACEHOLDER_PASSWORD", # <-- YOU MUST CHANGE THIS
        # database="courier_management" # This might be present in some calls
    )

        

    IGNORE_WHEN_COPYING_START

    Use code with caution.Python
    IGNORE_WHEN_COPYING_END

    Modify the placeholder values in all these connection calls within your main.py file:

        Replace "PLACEHOLDER_HOST" with your MySQL server's hostname or IP address (e.g., "localhost", "127.0.0.1", or a network IP).

        Replace "PLACEHOLDER_USER" with your actual MySQL username (e.g., "root" or a specific user you created).

        Replace "PLACEHOLDER_PASSWORD" with the correct password for that MySQL user.

    Save the main.py file after making these changes everywhere the connection is established.

Step 4: Ensure MySQL Server is Running

    Make sure your MySQL database server is active and running before proceeding.

Step 5: Automatic Database/Table Creation

    The script is designed to automatically create the courier_management database and the user and orders tables the first time it successfully connects using the credentials you provided in Step 3. Ensure the MySQL user has the necessary permissions (CREATE DATABASE, CREATE TABLE).
Database Schema

The script creates the following tables in the courier_management database:

    user

        username VARCHAR(50) NOT NULL

        password VARCHAR(50) NOT NULL (Stores password in plain text - SECURITY RISK)

        mobile VARCHAR(15) NOT NULL

    orders

        id INT AUTO_INCREMENT PRIMARY KEY

        username VARCHAR(50)

        mobile VARCHAR(15)

        address TEXT

        date DATE

        product_id VARCHAR(50)

        product_name VARCHAR(100)

        quantity INT
Running the Application

    Open Terminal: Open your terminal or command prompt.

    Navigate to Project Directory: Use the cd command to go into the folder where main.py is saved.

          
    cd path/to/CourierManagementSystem

        

    IGNORE_WHEN_COPYING_START

Use code with caution.Bash
IGNORE_WHEN_COPYING_END

Run the Script: Execute the Python script:

      
python main.py

    

IGNORE_WHEN_COPYING_START
Use code with caution.Bash
IGNORE_WHEN_COPYING_END

(Or use python3 main.py if needed)

Interact: The "Courier Management System" window should appear. Use the GUI to register, log in, and manage orders.
