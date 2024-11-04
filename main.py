import psycopg2
from config import user, password, db_name, host

tables = {}


def connect_to_db():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            database=db_name,
            password=password
        )
        cursor = connection.cursor()
    except Exception as e:
        print("[INFO] THE DATABASE is not opened", e)
    finally:
        print("[INFO] THE DATABASE is opened succesfully")
        return connection, cursor


def add_an_entry(coonection, cursor):
    name = input("enter name: ")
    phone = input("enter phone: ")
    email = input("enter email: ")
    try:
        cursor.execute(
            f"""INSERT INTO contact (name, phone, email)
            VALUES ('{name}', '{phone}', '{email}');"""
        )
        coonection.commit()
    except Exception as e:
        print("[ERROR] Could not add an entry:", e)
        raise e


def delete_an_entry(coonection, cursor):
    id = input("enter id to delete an entry:")
    find_an_entry(coonection, cursor, id)
    try:
        cursor.execute(
            f"""DELETE FROM contact WHERE id={id}"""
        )
        coonection.commit()
    except Exception as e:
        print("[INFO] No entry found with that ID.")
        raise e


def find_an_entry(coonection, cursor, id=None):
    if not id:
        id = int(input("enter id to find an entry:"))
    try:
        cursor.execute(
            f"""SELECT * FROM contact WHERE id={id};"""
        )
        coonection.commit()
        print(cursor.fetchone())
    except Exception as e:
        print("[ERROR] Could not find entry:", e)
        raise e


def update_an_entry(coonection, cursor):
    try:
        id = int(input("enter id to find an entry:"))
        name = input("enter name:")
        find_an_entry(coonection, cursor, id)
        cursor.execute(
            f"""UPDATE contact SET name = '{name}' WHERE id={id};"""
        )
        coonection.commit()
        find_an_entry(coonection, cursor, id)
    except Exception as e:
        print("[ERROR] Could not update entry:", e)


def select_entries(connection, cursor):
    try:
        cursor.execute("SELECT * FROM contact;")
        entries = cursor.fetchall()
        print(entries)
    except Exception as e:
        print("[ERROR] Could not select entries:", e)


def menu_of_database():
    print("click 1 to add an entry")
    print("click 2 to delete an entry")
    print("click 3 to find an entry")
    print("click 4 to update an entry")
    print("click 5 to sellect all entries")
    print("click 6 to exit")
    return int(input())


def exit_from_db(coonection, cursor):
    coonection.close()
    cursor.close()
    print("[INFO] DB is closed succesfully")


def main():
    coonection, cursor = connect_to_db()
    while True:
        numder = menu_of_database()

        match numder:
            case 1: add_an_entry(coonection, cursor)
            case 2: delete_an_entry(coonection, cursor)
            case 3: find_an_entry(coonection, cursor)
            case 4: update_an_entry(coonection, cursor)
            case 5: select_entries(coonection, cursor)
            case 6: break
    exit_from_db(coonection, cursor)


if __name__ == "__main__":
    main()
