# Import and Setup
from setup import get_db_connection
db, cur = get_db_connection()

# Add data to tables
def add(item_count=1):
        for i in range(item_count):
            if item_count == 1:
                print("\nEnter Details of the Medicine:")
            else:
                print(f"\nEnter Details of Medicine {i+1}:")
            med_id = int(input("MedID: "))
            med_name = input("Medicine Name: ")
            med_type = input("Medicine Type: ")
            company = input("Manufacturing Company: ")
            description = input("Description: ")
            side_effects = input("Side-Effects(separated by ','): ")
            price = float(input("Medicine Price: "))
            available = bool(int(input("Medicine Available(1 = yes, 0 = no): ")))
            latest_date = input("Newest Batch Date(YYYY-MM-DD): ")
            if latest_date == '':
                latest_date = '1970-01-01'
            print('\nAdding to Database...')
            cur.execute(f"INSERT INTO Medicines VALUES({med_id}, '{med_name}', '{med_type}', '{company}', '{description}', '{side_effects}', {price}, {available}, '{latest_date}');")
        db.commit()
        print(f"{item_count} Medicines Added to Database.")

# Search through the tables in different modes for different filters
def search(search_mode: int, search_kw='', search_count=0):
    if search_mode == 0:
        print('Fetching Full Data...')
        cur.execute(f'SELECT * FROM Medicines;')
    else:
        print(f'Fetching Data...')
        if search_mode == 1:
            cur.execute(f'SELECT * FROM Medicines WHERE Name = "{search_kw}";')
        elif search_mode == 2:
            cur.execute(f'SELECT * FROM Medicines WHERE Type = "{search_kw}";')
        elif search_mode == 3:
            cur.execute(f'SELECT * FROM Medicines WHERE Manufacture_Company = "{search_kw}";')
        elif search_mode == 4:
            cur.execute(f'SELECT * FROM Medicines WHERE Available = {search_kw};')
        elif search_mode == 5:
            cur.execute(f'SELECT * FROM Medicines ORDER BY Latest_Batch_Date DESC;')
    if search_count == 0:
        return cur.fetchall()
    else:
        return cur.fetchmany(search_count)
    
# Edit existing data
def edit(item_id: int):
    cur.execute(f'SELECT * FROM Medicines WHERE MedID = {item_id};')
    data = cur.fetchone()
    print('\nEnter Details of Medicine to edit, leave blank to keep existing data:')
    med_name = input(f"Medicine Name[{data[1]}]: ")
    med_type = input(f"Medicine Type[{data[2]}]: ")
    company = input(f"Manufacturing Company[{data[3]}]: ")
    description = input(f"Description[{data[4]}]: ")
    side_effects = input(f"Side-Effects[{data[5]}]: ")
    price = input(f"Medicine Price[{data[6]}]: ")
    available = input(f"Medicine Available[{data[7]}]: ")
    latest_date = input(f"Newest Batch Date[{data[8]}]: ")
    edit_lst = [med_name, med_type, company, description, side_effects, price, available, latest_date]
    
    print('Editing Medicine Record...')
    q_str = f'UPDATE Medicines SET'
    for i in edit_lst:
        if i != '':
            if edit_lst.index(i) == 0:
                q_str += f" Name = '{i}',"
            elif edit_lst.index(i) == 1:
                q_str += f" Type = '{i}',"
            elif edit_lst.index(i) == 2:
                q_str += f" Manufacture_Company = '{i}',"
            elif edit_lst.index(i) == 3:
                q_str += f" Description = '{i}',"
            elif edit_lst.index(i) == 4:
                q_str += f" Side_Effects = '{i}',"
            elif edit_lst.index(i) == 5:
                q_str += f" Price = {float(i)},"
            elif edit_lst.index(i) == 6:
                q_str += f" Available = {bool(int(i))},"
            elif edit_lst.index(i) == 7:
                q_str += f" Latest_Batch_Date = '{i}'"
    cur.execute(q_str.strip(',') + f' WHERE MedID = {item_id};')
    db.commit()
    print('Done.')

# Delete unwanted data
def delete(item_id: int):
    print('\nDeleting Medicine Record...')
    cur.execute(f'DELETE FROM Medicines WHERE MedID = {item_id};')
    db.commit()
    print('Done.')

# Display the fetched data in a tabular form
def display(cursor_list: list, display_list: list):
    index_dict = {'MedID':0, 'Name':1, 'Type':2, 'Manufacture_Company':3, 'Description':4, 'Side_Effects':5, 'Price':6, 'Available':7, 'Latest_Batch_Date':8}
    
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

def medicine_menu():
    while True:
            print("""\n~~~~~~~~~~Medicines Menu~~~~~~~~~~
1. Show All Medicines
2. Search For Medicines
3. Update A Medicine Record
4. Add New Medicines
5. Delete A Medicine Record
6. Exit""")
            choice = input('\nSelect Option or Exit Menu [1/2/3/4/5/6]: ')
            display_lst = ['MedID', 'Name', 'Type', 'Manufacture_Company', 'Description', 'Side_Effects', 'Price', 'Available', 'Latest_Batch_Date']

            if choice == '1':
                print("Showing All Data...")
                data = search(0)
                count = len(data)
                display(data, display_lst)
                print(f'\nDisplaying {count} Rows.')
                print('Done.')
            elif choice == '2' or choice == '3' or choice == '5':
                print("""Search On The Basis Of:
1. Name
2. Type
3. Company
4. Available
5. Newly Available
6. Not Available""")
                s_choice = input('Choose [1/2/3/4/5/6]: ')
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
                    keyword = input('Search: ')
                    result = search(2, keyword, s_count)
                    count = len(result)
                    display(result, display_lst)
                    print(f'\nDisplaying {count} Records.')  
                elif s_choice == '3':
                    keyword = input('Search: ')
                    result = search(3, keyword, s_count)
                    count = len(result)
                    display(result, display_lst)
                    print(f'\nDisplaying {count} Records.')  
                elif s_choice == '4':
                    keyword = 1
                    result = search(4, keyword, s_count)
                    count = len(result)
                    display(result, display_lst)
                    print(f'\nDisplaying {count} Records.')   
                elif s_choice == '5':
                    result = search(5, search_count=s_count)
                    count = len(result)
                    display(result, display_lst)
                    print(f'\nDisplaying {count} Records.')  
                elif s_choice == '6':
                    keyword = 0
                    result = search(4, keyword, s_count)
                    count = len(result)
                    display(result, display_lst)
                    print(f'\nDisplaying {count} Records.')

                if choice == '2':
                    m_choice = int(input(f'Choose To Learn More[1-{count} or 0 to Exit]: '))
                    if m_choice == 0:
                        pass
                    else:
                        medicine = result[m_choice-1]
                        available = ''
                        if int(medicine[7]) == 0:
                            available = 'No'
                        elif int(medicine[7]) == 1:
                            available = 'Yes'
                        print(f"""\nMore Info on MedID: {medicine[0]}
Name: {medicine[1]}
Type: {medicine[2]}
Side Effects: {medicine[5]}
Manufactured By: {medicine[3]}
Description: {medicine[4]}
Price: {medicine[6]}
Available: {available}
Latest Stock Date: {medicine[8]}""")
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
                n = int(input('\nHow many medicines to add? '))
                add(n)
            elif choice == '6':
                print('\nGoing to Main Menu...\n')
                break