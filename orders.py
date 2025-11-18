# Import & Setup
from setup import get_db_connection
db, cur = get_db_connection()

# Add data to tables
def add():
    print("\nEnter Order Details:")
    order_id = int(input("OrderID: "))
    client_name = input("Client Name: ")
    client_address = input("Client Address: ")
    phone_no = int(input("Client Phone No.: "))
    order_charge = float(input("Order Charge: "))
    order_date = input("Order Date(YYYY-MM-DD): ")
    medicines = input("Medicines(MedID separated by ','): ")
    med_count = input("Medicine Amount(with respect to above entry separated by ','): ")
    print('\nAdding to Database...')
    cur.execute(f"INSERT INTO Orders VALUES({order_id}, '{client_name}', '{client_address}', {phone_no}, {order_charge}, '{order_date}', '{medicines}', '{med_count}', False, '1970-01-01');")
    db.commit() 
    print(f"Order Added to Database.")

# Search through the tables in different modes for different filters
def search(search_mode: int, search_kw='', search_count=0):
    if search_mode == 0:
        print('Fetching Full Data...')
        cur.execute(f'SELECT * FROM Orders;')
    else:
        print(f'Fetching Data...')
        if search_mode == 1:
            cur.execute(f'SELECT * FROM Orders WHERE Name = "{search_kw}";')
        elif search_mode == 2:
            cur.execute(f'SELECT * FROM Orders WHERE Order_Date = "{search_kw}";')
        elif search_mode == 3:
            cur.execute(f'SELECT * FROM Orders WHERE Completed = {search_kw};')
        elif search_mode == 4:
            cur.execute(f'SELECT * FROM Orders WHERE Completion_Date = "{search_kw}";')
    if search_count == 0:
        return cur.fetchall()
    else:
        return cur.fetchmany(search_count)
    
# Edit existing data
def edit(table: str, item_id: int):
    cur.execute(f'SELECT * FROM Orders WHERE OrderID = {item_id};')
    data = cur.fetchone()
    print('\nEnter Details of Order to edit, leave blank to keep existing data:')
    client_name = input(f"Client Name[{data[1]}]: ")
    client_address = input(f"Client Address[{data[2]}]: ")
    phone_no = input(f"Client Phone No.[{data[3]}]: ")
    order_charge = input(f"Order Charge[{data[4]}]: ")
    order_date = input(f"Order Date[{data[5]}]: ")
    medicines = input(f"Medicines[{data[6]}]: ")
    med_count = input(f"Medicine Amount[{data[7]}]: ")
    completed = input(f"Order Completed[{data[8]}]: ")
    completion_date = input(f"Order Completion Date[{data[9]}]: ")
    edit_lst = [client_name, client_address, phone_no, order_charge, order_date, medicines, med_count, completed, completion_date]

    print('Editing Order Details...')
    q_str = f'UPDATE Orders SET'
    for i in edit_lst:
        if i != '':
            if edit_lst.index(i) == 0:
                q_str += f' Name = "{i}",'
            elif edit_lst.index(i) == 1:
                q_str += f' Address = "{i}",'
            elif edit_lst.index(i) == 2:
                q_str += f' Phone_No = {int(i)},'
            elif edit_lst.index(i) == 3:
                q_str += f' Order_Charge = {float(i)},'
            elif edit_lst.index(i) == 4:
                q_str += f' Order_Date = "{i}",'
            elif edit_lst.index(i) == 5:
                q_str += f' Medicines = "{i}",'
            elif edit_lst.index(i) == 6:
                q_str += f' Med_Count = "{i}",'
            elif edit_lst.index(i) == 7:
                q_str += f' Completed = {bool(int(i))},'
            elif edit_lst.index(i) == 8:
                q_str += f' Completion_Date = "{i}"'
    cur.execute(q_str.strip(',') + f' WHERE OrderID = {item_id};')
    db.commit()
    print('Done.')

# Delete unwanted data
def delete(item_id: int):
    print('\nDeleting Order Record...')
    cur.execute(f'DELETE FROM Orders WHERE OrderID = {item_id};')
    db.commit()
    print('Done.')

# Display the fetched data in a tabular form
def display(cursor_list: list, display_list: list):
    index_dict = {'OrderID':0, 'Name':1, 'Address':2, 'Phone_No':3, 'Order_Charge':4, 'Order_Date':5, 'Medicines':6, 'Med_Count':7, 'Completed':8, 'Completion_Date':9}
    
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

def order_menu():
    while True:
            print("""\n~~~~~~~~~~~~Orders Menu~~~~~~~~~~~
1. Show Order History
2. Order Search
3. Update Order Details
4. Place New Orders
5. Delete Order Record
6. Exit""")
            choice = input('\nSelect Option or Exit Menu [1/2/3/4/5/6]: ')
            display_lst = ['OrderID', 'Name', 'Address', 'Phone_No', 'Order_Charge', 'Order_Date', 'Medicines', 'Med_Count', 'Completed', 'Completion_Date']

            if choice == '1':
                print("Showing All Data...")
                data = search(0)
                count = len(data)
                display(data, display_lst)
                print(f'\nDisplaying {count} Rows.')
                print('Done.')
            elif choice == '2' or choice == '3' or choice == '5':
                print("""Search On The Basis Of:
1. Client Name
2. Order Date
3. Completed
4. Completion Date
5. Not Completed""")
                s_choice = input('Choose [1/2/3/4/5]: ')
                s_count = int(input('How many results should be gathered(0 for all): '))
                keyword = ''
                result = []

                if s_choice == '1':
                    keyword = input('Search: ')
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
                    keyword = 1
                    result = search(3, keyword, s_count)
                    count = len(result)
                    display(result, display_lst)
                    print(f'\nDisplaying {count} Records.')
                elif s_choice == '4':
                    keyword = input('Search[YYYY-MM-DD]: ')
                    result = search(4, keyword, s_count)
                    count = len(result)
                    display(result, display_lst)
                    print(f'\nDisplaying {count} Records.')
                elif s_choice == '5':
                    keyword = 0
                    result = search(3, keyword, s_count)
                    count = len(result)
                    display(result, display_lst)
                    print(f'\nDisplaying {count} Records.')
                if choice == '2':
                    m_choice = int(input(f'Choose To Learn More[1-{count} or 0 to Exit]: '))
                    if m_choice == 0:
                        pass
                    else:
                        order = result[m_choice-1]
                        completed = ''
                        if int(order[8]) == 0:
                            completed = 'No'
                        elif int(order[8]) == 1:
                            completed = 'Yes'
                        print(f"""\nMore Info on OrderID: {order[0]}
Client Name: {order[1]}
Client Address: {order[2]}
Client Phone No.: {order[3]}
Order Charge: {order[4]}
Order Date: {order[5]}
Medicines Order: {order[6]}
No. of Medicines(w.r.t Medicine Order): {order[7]}
Completed: {completed}
Completion Date: {order[9]}""")
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
                add()
            elif choice == '6':
                print('\nGoing to Main Menu...\n')
                break