# Imports
import mariadb as con
import pickle
import os

# Setup
# Create credentials for MySQL connection
if not os.path.isfile('./credentials.dat'):
    f = open('credentials.dat', 'wb+')
    print("Credentials File Not Found... Creating New File...")
    username = input("Enter MariaDB User: ")
    password = input("Enter Password: ")
    credentials = (username, password)
    pickle.dump(credentials, f)
    f.close()
    print("Credentials Creating Completed. Exiting...")
    print("Rerun Application to Continue.")
    exit(0)

# Create MySQL connection
print("Initializing SQL Connection...")
f = open('credentials.dat', 'rb')
credentials = pickle.load(f)
try:
    db = con.connect(
        host="localhost",
        user=credentials[0],
        password=credentials[1]
    )
except con.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
f.close()
cur = db.cursor()

def get_db_connection():
    return db, cur

def initialize_db(db, cur):
    print('Initializing Database and Tables...')
    cur.execute('CREATE DATABASE IF NOT EXISTS MediCheck;')
    db.database = 'MediCheck'
    cur.execute('CREATE TABLE IF NOT EXISTS Medicines(MedID INTEGER PRIMARY KEY, Name VARCHAR(50) NOT NULL, Type VARCHAR(50) NOT NULL, Manufacture_Company VARCHAR(50) NOT NULL, Description VARCHAR(300), Side_Effects VARCHAR(300) NOT NULL, Price DECIMAL(6,2) NOT NULL, Available BOOLEAN NOT NULL, Latest_Batch_Date DATE);')
    cur.execute('CREATE TABLE IF NOT EXISTS Stocks(StockID INTEGER PRIMARY KEY, MedID INTEGER NOT NULL, Box_Count INTEGER NOT NULL, Arrival_Date DATE NOT NULL, Manufacture_Date DATE NOT NULL, Expiration_Date DATE NOT NULL, Price DECIMAL(7,2) NOT NULL, Shelf_No CHAR(4) NOT NULL, Finished BOOLEAN NOT NULL, FOREIGN KEY (MedID) REFERENCES Medicines(MedID) ON DELETE CASCADE);')
    cur.execute('CREATE TABLE IF NOT EXISTS Orders(OrderID INTEGER PRIMARY KEY, Name VARCHAR(50) NOT NULL, Address VARCHAR(150) NOT NULL, Phone_No INTEGER NOT NULL, Order_Charge DECIMAL(7,2) NOT NULL, Order_Date DATE NOT NULL, Medicines VARCHAR(100) NOT NULL, Med_Count VARCHAR(100) NOT NULL, Completed BOOLEAN NOT NULL, Completion_Date DATE);')
    print("Initialization Completed. Starting Application...\n")

def setup_db():
    db, cur = get_db_connection()
    initialize_db(db, cur)
