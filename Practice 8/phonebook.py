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

    # ---------- FUNCTIONS ----------

    def search_pattern(self, pattern):
        self.cur.execute("SELECT * FROM search_pattern(%s)", (pattern,))
        return self.cur.fetchall()

    def get_paginated(self, limit, offset):
        self.cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
        return self.cur.fetchall()

    # ---------- PROCEDURES ----------

    def insert_or_update(self, first_name, last_name, phone, email, address):
        self.cur.execute(
            "CALL insert_or_update_user(%s, %s, %s, %s, %s)",
            (first_name, last_name, phone, email, address)
        )
        self.conn.commit()

    def insert_many(self, names, phones):
        self.cur.execute("CALL insert_many_users(%s, %s)", (names, phones))
        self.conn.commit()

    def delete_user(self, value):
        self.cur.execute("CALL delete_user(%s)", (value,))
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()


def menu(db):
    while True:
        print("\n1. Поиск (pattern)")
        print("2. Пагинация")
        print("3. Insert / Update")
        print("4. Массовая вставка")
        print("5. Удалить")
        print("0. Выход")

        choice = input("Выбор: ")

        if choice == "1":
            pattern = input("Введи текст: ")
            results = db.search_pattern(pattern)
            for r in results:
                print(r)

        elif choice == "2":
            limit = int(input("LIMIT: "))
            offset = int(input("OFFSET: "))
            results = db.get_paginated(limit, offset)
            for r in results:
                print(r)

        elif choice == "3":
            fn = input("Имя: ")
            ln = input("Фамилия: ")
            phone = input("Телефон: ")
            email = input("Email: ")
            address = input("Адрес: ")

            db.insert_or_update(fn, ln, phone, email, address)

        elif choice == "4":
            names = ["Ali", "John", "BadUser"]
            phones = ["7771234567", "1234567890", "abc123"]

            db.insert_many(names, phones)

        elif choice == "5":
            value = input("Имя или телефон: ")
            db.delete_user(value)

        elif choice == "0":
            db.close()
            break


if __name__ == "__main__":
    db = PhoneBookDB()
    db.create_table()
    menu(db)