import psycopg2
import csv
import json
from config import DB_CONFIG


class PhoneBook:
    def __init__(self):
        # подключение к БД
        self.conn = psycopg2.connect(**DB_CONFIG)
        self.cur = self.conn.cursor()

    def get_or_create_group(self, group_name):
        # ищем группу
        self.cur.execute(
            "SELECT id FROM groups WHERE name = %s",
            (group_name,)
        )
        group = self.cur.fetchone()

        if group:
            return group[0]

        # если группы нет — создаем
        self.cur.execute(
            "INSERT INTO groups(name) VALUES (%s) RETURNING id",
            (group_name,)
        )
        return self.cur.fetchone()[0]

    def add_contact(self, data):
        # получаем id группы
        group_id = self.get_or_create_group(data["group"])

        # добавляем контакт
        self.cur.execute("""
            INSERT INTO phonebook
            (first_name, last_name, email, address, birthday, group_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            data["first_name"],
            data["last_name"],
            data["email"],
            data["address"],
            data["birthday"],
            group_id
        ))

        contact_id = self.cur.fetchone()[0]

        # добавляем номер телефона
        self.cur.execute("""
            INSERT INTO phones(contact_id, phone, type)
            VALUES (%s, %s, %s)
        """, (
            contact_id,
            data["phone"],
            data["type"]
        ))

        # сохраняем изменения
        self.conn.commit()

    def import_csv(self, filename):
        # читаем контакты из csv
        with open(filename, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                self.add_contact(row)

    def filter_by_group(self, group_name):
        # вывод контактов конкретной группы
        self.cur.execute("""
            SELECT p.first_name, p.last_name
            FROM phonebook p
            JOIN groups g ON p.group_id = g.id
            WHERE g.name = %s
        """, (group_name,))

        for row in self.cur.fetchall():
            print(row)

    def search_by_email(self, email):
        # поиск по email
        self.cur.execute("""
            SELECT * FROM phonebook
            WHERE email ILIKE %s
        """, (f"%{email}%",))

        for row in self.cur.fetchall():
            print(row)

    def sort_contacts(self, field):
        # разрешенные поля сортировки
        allowed = ["first_name", "birthday", "created_at"]

        if field not in allowed:
            print("Wrong field")
            return

        # сортировка контактов
        self.cur.execute(f"""
            SELECT * FROM phonebook
            ORDER BY {field}
        """)

        for row in self.cur.fetchall():
            print(row)

    def export_json(self, filename):
        # получаем все контакты
        self.cur.execute("""
            SELECT p.first_name,
                   p.last_name,
                   p.email,
                   p.birthday,
                   g.name,
                   ph.phone,
                   ph.type
            FROM phonebook p
            LEFT JOIN groups g ON p.group_id = g.id
            LEFT JOIN phones ph ON ph.contact_id = p.id
        """)

        rows = self.cur.fetchall()
        data = []

        # собираем данные в список словарей
        for row in rows:
            data.append({
                "first_name": row[0],
                "last_name": row[1],
                "email": row[2],
                "birthday": str(row[3]),
                "group": row[4],
                "phone": row[5],
                "type": row[6]
            })

        # сохраняем в json
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def import_json(self, filename):
        # читаем json
        with open(filename, encoding="utf-8") as file:
            data = json.load(file)

        for contact in data:
            # проверка на дубликат
            self.cur.execute("""
                SELECT id FROM phonebook
                WHERE first_name = %s AND last_name = %s
            """, (
                contact["first_name"],
                contact["last_name"]
            ))

            existing = self.cur.fetchone()

            if existing:
                action = input("Duplicate found (skip/overwrite): ")

                if action == "skip":
                    continue

                if action == "overwrite":
                    # удаляем старый контакт
                    self.cur.execute("""
                        DELETE FROM phonebook
                        WHERE id = %s
                    """, (existing[0],))

            self.add_contact(contact)

    def add_phone(self, name, phone, phone_type):
        # вызов процедуры добавления телефона
        self.cur.execute(
            "CALL add_phone(%s, %s, %s)",
            (name, phone, phone_type.lower())
        )
        self.conn.commit()

    def move_to_group(self, name, group):
        # перенос контакта в другую группу
        self.cur.execute(
            "CALL move_to_group(%s, %s)",
            (name, group)
        )
        self.conn.commit()

    def search_contacts(self, query):
        # поиск по имени, фамилии, email или телефону
        self.cur.execute(
            "SELECT * FROM search_contacts(%s)",
            (query,)
        )

        for row in self.cur.fetchall():
            print(row)

    def paginate(self, limit):
        # текущая страница
        page = 0

        while True:
            # вычисляем смещение
            offset = page * limit

            # получаем часть данных
            self.cur.execute(
                "SELECT * FROM get_contacts_paginated(%s, %s)",
                (limit, offset)
            )

            rows = self.cur.fetchall()

            for row in rows:
                print(row)

            # навигация по страницам
            cmd = input("next / prev / quit: ")

            if cmd == "next":
                page += 1
            elif cmd == "prev" and page > 0:
                page -= 1
            elif cmd == "quit":
                break


def menu():
    pb = PhoneBook()

    while True:
        print("""
1. Import CSV
2. Filter by group
3. Search by email
4. Sort contacts
5. Export JSON
6. Import JSON
7. Add phone
8. Move to group
9. Search contacts
10. Pagination
0. Exit
        """)

        choice = input("Choose: ")

        if choice == "1":
            pb.import_csv("contacts.csv")

        elif choice == "2":
            group = input("Group: ")
            pb.filter_by_group(group)

        elif choice == "3":
            email = input("Email: ")
            pb.search_by_email(email)

        elif choice == "4":
            field = input("Field: ")
            pb.sort_contacts(field)

        elif choice == "5":
            pb.export_json("contacts.json")

        elif choice == "6":
            pb.import_json("data_to_read.json")

        elif choice == "7":
            name = input("Name: ")
            phone = input("Phone: ")
            phone_type = input("Type: ")
            pb.add_phone(name, phone, phone_type)

        elif choice == "8":
            name = input("Name: ")
            group = input("Group: ")
            pb.move_to_group(name, group)

        elif choice == "9":
            query = input("Query: ")
            pb.search_contacts(query)

        elif choice == "10":
            pb.paginate(5)

        elif choice == "0":
            break


if __name__ == "__main__":
    menu()