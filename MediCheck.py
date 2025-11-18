# Imports
from setup import setup_db, get_db_connection
from medicines import medicine_menu
from stocks import stock_menu
from orders import order_menu

db, cur = get_db_connection()
setup_db()

# Main Menu of the application
print('WELCOME TO MEDICHECK!'.center(110,' '))
while True:
    print("""~~~~~~~~~~~~~~~Menu~~~~~~~~~~~~~~~
1. Medicines
2. Stocks
3. Orders
4. Exit""")
    tab = input('\nSelect Tab or Exit [1/2/3/4]: ')

    if tab == "1":
        medicine_menu()
    elif tab == "2":
        stock_menu()
    elif tab == "3":
        order_menu()
    elif tab == "4":
        print('\nExiting Application...')
        break
    else:
        print("\nPlease Enter Correct Option!\n")

# Closing
db.close()
