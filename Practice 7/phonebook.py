import csv
from connect import get_connection


class PhoneBookDB:
    def __init__(self):
        self.conn = get_connection()
        self.cur = self.conn.cursor()

    def create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS phonebook (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                phone VARCHAR(20) UNIQUE NOT NULL,
                email VARCHAR(100),
                address TEXT
            );
        """)
        self.conn.commit()

    def insert_from_csv(self, filename):
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                try:
                    self.cur.execute("""
                        INSERT INTO phonebook (first_name, last_name, phone, email, address)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (
                        row['first_name'],
                        row['last_name'],
                        row['phone'],
                        row['email'],
                        row['address']
                    ))
                except Exception as e:
                    print(f"Ошибка при вставке {row}: {e}")

        self.conn.commit()

    def insert_contact(self):
        first_name = input("Имя: ")
        last_name = input("Фамилия: ")
        phone = input("Телефон: ")
        email = input("Email: ")
        address = input("Адрес: ")

        try:
            self.cur.execute("""
                INSERT INTO phonebook (first_name, last_name, phone, email, address)
                VALUES (%s, %s, %s, %s, %s)
            """, (first_name, last_name, phone, email, address))

            self.conn.commit()
        except Exception as e:
            print("Ошибка:", e)

    def update_contact(self):
        phone = input("Введите телефон контакта: ")

        new_first_name = input("Новое имя: ")
        new_last_name = input("Новая фамилия: ")
        new_phone = input("Новый телефон: ")
        new_email = input("Новый email: ")
        new_address = input("Новый адрес: ")

        if new_first_name:
            self.cur.execute("UPDATE phonebook SET first_name=%s WHERE phone=%s", (new_first_name, phone))

        if new_last_name:
            self.cur.execute("UPDATE phonebook SET last_name=%s WHERE phone=%s", (new_last_name, phone))

        if new_phone:
            self.cur.execute("UPDATE phonebook SET phone=%s WHERE phone=%s", (new_phone, phone))

        if new_email:
            self.cur.execute("UPDATE phonebook SET email=%s WHERE phone=%s", (new_email, phone))

        if new_address:
            self.cur.execute("UPDATE phonebook SET address=%s WHERE phone=%s", (new_address, phone))

        self.conn.commit()

    def search_by_name(self, name):
        self.cur.execute("""
            SELECT * FROM phonebook
            WHERE first_name ILIKE %s OR last_name ILIKE %s
        """, (f"%{name}%", f"%{name}%"))

        results = self.cur.fetchall()
        for row in results:
            print(row)

    def search_by_phone_prefix(self, prefix):
        self.cur.execute("""
            SELECT * FROM phonebook
            WHERE phone LIKE %s
        """, (f"{prefix}%",))

        results = self.cur.fetchall()
        for row in results:
            print(row)

    def delete_contact(self):
        choice = input("Удалить по (1) телефону или (2) имени? ")

        if choice == "1":
            phone = input("Телефон: ")
            self.cur.execute("DELETE FROM phonebook WHERE phone=%s", (phone,))
        else:
            name = input("Имя: ")
            self.cur.execute("""
                DELETE FROM phonebook
                WHERE first_name=%s OR last_name=%s
            """, (name, name))

        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()



def menu(db):
    while True:
        print("\n1. Загрузить CSV")
        print("2. Добавить контакт")
        print("3. Обновить контакт")
        print("4. Поиск по имени")
        print("5. Поиск по префиксу телефона")
        print("6. Удалить контакт")
        print("0. Выход")

        choice = input("Выбор: ")

        if choice == "1":
            db.insert_from_csv("contacts.csv")
        elif choice == "2":
            db.insert_contact()
        elif choice == "3":
            db.update_contact()
        elif choice == "4":
            name = input("Имя или фамилия: ")
            db.search_by_name(name)
        elif choice == "5":
            prefix = input("Префикс: ")
            db.search_by_phone_prefix(prefix)
        elif choice == "6":
            db.delete_contact()
        elif choice == "0":
            db.close()
            break


if __name__ == "__main__":
    db = PhoneBookDB()
    db.create_table()
    menu(db)