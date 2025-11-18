# Import & Setup
from setup import get_db_connection
db, cur = get_db_connection()

# Add data to tables
def add(item_count=1):
    for i in range(item_count):
        if item_count == 1:
            print("\nEnter Details of the Stock:")
        else:
            print(f"\nEnter Details of Stock {i+1}:")
        stock_id = int(input("StockID: "))
        med_id = int(input("MedID of Stock Medicine: "))
        box_count = int(input("No. of Boxes: "))
        arrival_date = input("Arrival Date(YYYY-MM-DD): ")
        manufacture_date = input("Manufacture Date(YYYY-MM-DD): ")
        expiration_date = input("Expiration Date(YYYY-MM-DD): ")
        stock_price = float(input('Stock Price: '))
        shelf_no = input("Shelf No of Stock(Ex-A124): ")
        print('\nAdding to Database...')
        cur.execute(f"INSERT INTO Stocks VALUES({stock_id}, {med_id}, {box_count}, '{arrival_date}', '{manufacture_date}', '{expiration_date}', {stock_price}, '{shelf_no}', False);")
    db.commit()
    print(f"{item_count} Stocks Added to Database.")

# Search through the tables in different modes for different filters
def search(search_mode: int, search_kw='', search_count=0):
    if search_mode == 0:
        print('Fetching Full Data...')
        cur.execute(f'SELECT * FROM Stocks;')
    else:
        print(f'Fetching Data...')
        if search_mode == 1:
            cur.execute(f'SELECT * FROM Stocks WHERE MedID = {search_kw};')
        elif search_mode == 2:
            cur.execute(f'SELECT * FROM Stocks WHERE Arrival_Date = "{search_kw}";')
        elif search_mode == 3:
            cur.execute(f'SELECT * FROM Stocks WHERE Expiration_Date = "{search_kw}" AND Finished = 0;')
        elif search_mode == 4:
            cur.execute(f'SELECT * FROM Stocks WHERE Shelf_No = "{search_kw}";')
        elif search_mode == 5:
            cur.execute(f'SELECT * FROM Stocks WHERE Finished = {search_kw};')
    if search_count == 0:
        return cur.fetchall()
    else:
        return cur.fetchmany(search_count)
    
# Edit existing data
def edit(item_id: int):
    cur.execute(f'SELECT * FROM Stocks WHERE StockID = {item_id};')
    data = cur.fetchone()
    print('\nEnter Details of Stock to edit, leave blank to keep existing data:')
    med_id = input(f"MedID of Stock Medicine[{data[1]}]: ")
    box_count = input(f"No. of Boxes[{data[2]}]: ")
    arrival_date = input(f"Arrival Date[{data[3]}]: ")
    manufacture_date = input(f"Manufacture Date[{data[4]}]: ")
    expiration_date = input(f"Expiration Date[{data[5]}]: ")
    stock_price = input(f'Stock Price[{data[6]}]: ')
    shelf_no = input(f"Shelf No of Stock[{data[7]}]: ")
    finished = input(f"Stock Finished[{data[8]}]: ")
    edit_lst = [med_id, box_count, arrival_date, manufacture_date, expiration_date, stock_price, shelf_no, finished]

    print('Editing Stock Record...')
    q_str = f'UPDATE Stocks SET'
    for i in edit_lst:
        if i != '':
            if edit_lst.index(i) == 0:
                q_str += f' MedID = {int(i)},'
            elif edit_lst.index(i) == 1:
                q_str += f' Box_Count = {int(i)},'
            elif edit_lst.index(i) == 2:
                q_str += f' Arrival_Date = "{i}",'
            elif edit_lst.index(i) == 3:
                q_str += f' Manufacture_Date = "{i}",'
            elif edit_lst.index(i) == 4:
                q_str += f' Expiration_Date = "{i}",'
            elif edit_lst.index(i) == 5:
                q_str += f' Price = {float(i)},'
            elif edit_lst.index(i) == 6:
                q_str += f' Shelf_No = "{i}",'
            elif edit_lst.index(i) == 7:
                q_str += f' Finished = {bool(int(i))}'
    cur.execute(q_str.strip(',') + f' WHERE StockID = {item_id};')
    db.commit()
    print('Done.')

# Delete unwanted data
def delete(item_id: int):
    print('\nDeleting Stocks Record...')
    cur.execute(f'DELETE FROM Stocks WHERE StockID = {item_id};')
    db.commit()
    print('Done.')

# Display the fetched data in a tabular form
def display(cursor_list: list, display_list: list):
    index_dict = {'StockID':0, 'MedID':1, 'Box_Count':2, 'Arrival_Date':3, 'Manufacture_Date':4, 'Expiration_Date':5, 'Price':6, 'Shelf_No':7, 'Finished':8}
    
    print('Displaying Fetched Data...')
    for i in display_list:
        print(f'| {i} |', end='')
    print('\n')
    for i in cursor_list:
        for j in display_list:
            if len(str(i[index_dict[j]])) > 15:
                print(f'| {str(i[index_dict[j]])[:15]}... |', end='')
            else:
                print(f'| {i[index_dict[j]]} |', end='')
        print('\n')

def stock_menu():
    while True:
            print("""\n~~~~~~~~~~~Stocks Menu~~~~~~~~~~~
1. Show Medicine Stock History
2. Search For Stocks
3. Update A Medicine Stock Record
4. Add Newly Received Stocks
5. Delete A Stock Record
6. Exit""")
            choice = input('\nSelect Option or Exit Menu [1/2/3/4/5/6]: ')
            display_lst = ['StockID', 'MedID', 'Box_Count', 'Arrival_Date', 'Manufacture_Date', 'Expiration_Date', 'Price', 'Shelf_No', 'Finished']

            if choice == '1':
                print("Showing All Data...")
                data = search(0)
                count = len(data)
                display(data, display_lst)
                print(f'\nDisplaying {count} Rows.')
                print('Done.')
            elif choice == '2' or choice == '3' or choice == '5':
                print("""Search On The Basis Of:
1. Medicine
2. Arrival Date
3. Expiration Date
4. Shelf No.
5. Finished
6. Not Finished""")
                s_choice = input('Choose [1/2/3/4/5/6]: ')
                s_count = int(input('How many results should be gathered(0 for all): '))
                keyword = ''
                result = []

                if s_choice == '1':
                    keyword = int(input('Search: '))
                    result = search(1, keyword, s_count)
                    count = len(result)
                    display(result, display_lst)
                    print(f'\nDisplay {count} Records.')
                elif s_choice == '2':
                    keyword = input('Search[YYYY-MM-DD]: ')
                    result = search(2, keyword, s_count)
                    count = len(result)
                    display(result, display_lst)
                    print(f'\nDisplaying {count} Records.')
                elif s_choice == '3':
                    keyword = input('Search[YYYY-MM-DD]: ')
                    result = search(3, keyword, s_count)
                    count = len(result)
                    display(result, display_lst)
                    print(f'\nDisplaying {count} Records.')
                elif s_choice == '4':
                    keyword = input('Search[Ex-A123]: ')
                    result = search(4, keyword, s_count)
                    count = len(result)
                    display(result, display_lst)
                    print(f'\nDisplaying {count} Records.')
                elif s_choice == '5':
                    keyword = 1
                    result = search(5, keyword, s_count)
                    count = len(result)
                    display(result, display_lst)
                    print(f'\nDisplaying {count} Records.')
                elif s_choice == '6':
                    keyword = 0
                    result = search(5, keyword, s_count)
                    count = len(result)
                    display(result, display_lst)
                    print(f'\nDisplaying {count} Records.')

                if choice == '2':
                    m_choice = int(input(f'Choose To Learn More[1-{count} or 0 to Exit]: '))
                    if m_choice == 0:
                        pass
                    else:
                        stock = result[m_choice-1]
                        finished = ''
                        if int(stock[8]) == 0:
                            finished = 'No'
                        elif int(stock[8]) == 1:
                            finished = 'Yes'
                        print(f"""\nMore Info on StockID: {stock[0]}
MedID: {stock[1]}
No. Of Boxes: {stock[2]}
Arrival Date: {stock[3]}
Manufacture Date: {stock[4]}
Expiration Date: {stock[5]}
Price: {stock[6]}
Shelf No.: {stock[7]}
Finished: {finished}""")
                elif choice == '3':
                    m_choice = int(input(f'Choose To Edit[1-{count} or 0 to Exit]: '))
                    if m_choice == 0:
                        pass
                    else:
                        edit(result[m_choice-1][0])
                elif choice == '5':
                    m_choice = int(input(f'Choose To Delete[1-{count} or 0 to Exit]: '))
                    if m_choice == 0:
                        pass
                    else:
                        delete(result[m_choice-1][0])                    
            elif choice == '4':
                n = int(input('\nHow many stocks to add? '))
                add(n)
            elif choice == '6':
                print('\nGoing to Main Menu...\n')
                break