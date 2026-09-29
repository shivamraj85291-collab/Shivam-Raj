import mysql.connector as sql
import sys

# Replace "hotel_db" with your actual database name if it is different
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "hero",
    "database": "hotel_db"
}

def create_table():
    con = sql.connect(**DB_CONFIG)
    cur = con.cursor()
    # Fixed missing column name and added check_in/check_out columns to match your INSERT statement
    query = """
    CREATE TABLE IF NOT EXISTS ENTRY (
        id INT PRIMARY KEY,
        Name VARCHAR(50),
        Address VARCHAR(100),
        City VARCHAR(30),
        Contact_no VARCHAR(10),
        Room VARCHAR(4),
        check_in DATE,
        check_out DATE,
        Priority_customer CHAR(1)
    )
    """
    cur.execute(query)
    con.commit()
    con.close()
    print("Table created or verified successfully.")

def insert():
    con = sql.connect(**DB_CONFIG)
    cur = con.cursor()
    
    check_in = input("Enter Check-In date (YYYY-MM-DD): ")
    check_out = input("Enter Check-Out date (YYYY-MM-DD): ")

    while True:
        try:
            id = int(input("Enter ID: "))
            break
        except ValueError:
            print("ID must be numeric")

    while True:
        name = input("Enter Name: ")
        # .replace(" ", "") allows names with spaces to pass the isalpha() check
        if name.replace(" ", "").isalpha():
            break
        print("Only alphabets allowed")

    address = input("Enter Address: ")

    while True:
        city = input("Enter City: ")
        if city.replace(" ", "").isalpha():
            break
        print("Only alphabets allowed")

    while True:
        contact = input("Enter Contact No: ")
        if contact.isdigit() and len(contact) == 10:
            break
        print("Invalid contact number. Must be exactly 10 digits.")
        
    while True:
        room = input("Enter Room No: ")
        if room.isdigit() and len(room) <= 4:
            break
        print("Please enter 1 to 4 digit room number only.")
        
    while True:
        Priority_customer = input("Priority Customer (Y/N): ").upper()
        if Priority_customer in ('Y', 'N'):
            break
        print("Please enter exactly Y or N.")

    # Fixed syntax error (double commas) and mapped 9 values correctly
    cur.execute(
        "INSERT INTO ENTRY VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        (id, name, address, city, contact, room, check_in, check_out, Priority_customer)
    )
    
    con.commit()
    print("Booking inserted successfully.")
    con.close()

def Delete_Booking():
    while True:
        try:
            n = int(input("Enter the ID to delete: "))
        except ValueError:
            print("ID must be an integer.")
            continue
            
        con = sql.connect(**DB_CONFIG)
        cur = con.cursor()
        cur.execute("SELECT id FROM ENTRY")
        ids = cur.fetchall()
        id_list = [i[0] for i in ids]

        if n in id_list:
            cur.execute("DELETE FROM ENTRY WHERE id = %s", (n,))
            con.commit()
            print("Record deleted successfully")
            con.close()
            break
        else:
            print("ID not found. Try again.")
            con.close()

def Search():
    while True:
        try:
            n = int(input("Enter the ID to search: "))
        except ValueError:
            print("ID must be an integer.")
            continue
            
        con = sql.connect(**DB_CONFIG)
        cur = con.cursor()
        cur.execute("SELECT id FROM ENTRY")
        ids = cur.fetchall()
        id_list = [i[0] for i in ids]

        if n in id_list:
            cur.execute("SELECT * FROM ENTRY WHERE id = %s", (n,))
            # Added fetchone() and print() to actually display the data
            record = cur.fetchone()
            print("\n--- Booking Details ---")
            print(f"ID: {record[0]}\nName: {record[1]}\nAddress: {record[2]}\nCity: {record[3]}")
            print(f"Contact: {record[4]}\nRoom: {record[5]}\nCheck-in: {record[6]}")
            print(f"Check-out: {record[7]}\nPriority: {record[8]}")
            break
        else:
            print("ID not found. Try again.")
        con.close()

def View_All_Bookings():
    con = sql.connect(**DB_CONFIG)
    cur = con.cursor()
    cur.execute("SELECT * FROM ENTRY")
    # Added fetchall() and loop to actually display the records
    records = cur.fetchall()
    
    if not records:
        print("No bookings found.")
    else:
        print("\n--- All Bookings ---")
        for row in records:
            print(row)
            
    con.close()

def Update_Bookings():
    con = sql.connect(**DB_CONFIG)
    cur = con.cursor()
    
    cur.execute("SELECT id FROM ENTRY")
    ids = cur.fetchall()
    id_list = [i[0] for i in ids]

    while True:
        try:
            n = int(input("Enter the ID to update: "))
        except ValueError:
            print("Invalid ID.")
            continue

        if n in id_list:
            print("\nWhat do you want to update?")
            print("1. Name")
            print("2. Address")
            print("3. City")
            print("4. Contact_no")
            print("5. Priority_customer")
            print("6. Check_in date")
            print("7. Check_out date")

            ch = int(input("Enter choice: "))

            if ch == 1:
                u = input("Enter new Name: ")
                cur.execute("UPDATE ENTRY SET Name = %s WHERE id = %s", (u, n))
            elif ch == 2:
                u = input("Enter new Address: ")
                cur.execute("UPDATE ENTRY SET Address = %s WHERE id = %s", (u, n))
            elif ch == 3:
                u = input("Enter new City: ")
                cur.execute("UPDATE ENTRY SET City = %s WHERE id = %s", (u, n))
            elif ch == 4:
                u = input("Enter new Contact No: ")
                cur.execute("UPDATE ENTRY SET Contact_no = %s WHERE id = %s", (u, n))
            elif ch == 5:
                while True:
                    u = input("Priority customer (Y/N): ").upper()
                    if u in ('Y', 'N'):
                        break
                cur.execute("UPDATE ENTRY SET Priority_customer = %s WHERE id = %s", (u, n))
            elif ch == 6:
                 u = input("Enter new Check-In date (YYYY-MM-DD): ")
                 cur.execute("UPDATE ENTRY SET check_in = %s WHERE id = %s", (u, n))
            elif ch == 7:
                 u = input("Enter new Check-Out date (YYYY-MM-DD): ")
                 cur.execute("UPDATE ENTRY SET check_out = %s WHERE id = %s", (u, n))
            else:
                print("Invalid choice")
                continue
            
            con.commit()
            print("Record updated successfully")
            break
        else:
            print("ID not found. Try again.")

    con.close()

def menu():
    while True:
        print("\n------ HOTEL MANAGEMENT MENU ------")
        print("1. Create Table")
        print("2. Insert Booking")
        print("3. View All Bookings")
        print("4. Search Booking")
        print("5. Update Booking")
        print("6. Delete Booking")
        print("7. Exit")

        try:
            ch = int(input("Enter your choice: "))
        except ValueError:
            print("Please enter a number.")
            continue

        if ch == 1:
            create_table()
        elif ch == 2:
            insert()
        elif ch == 3:
            View_All_Bookings()
        elif ch == 4:
            Search()
        elif ch == 5:
            Update_Bookings()
        elif ch == 6:
            Delete_Booking()
        elif ch == 7:
            print("Thank you. Exiting program.")
            sys.exit()
        else:
            print("Invalid choice. Try again.")

# Added execution block to actually run the program
if __name__ == "__main__":
    menu()