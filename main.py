import csv
from enum import unique
from pprint import pprint
import re

# 1. Загрузка данных
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# 2. Обработка ФИО
for row in contacts_list[1:]:
    full_name = " ".join(row[:3]).split()
    while len(full_name) < 3:
        full_name.append('')
    row[0], row[1], row[2] = full_name[0], full_name[1], full_name[2]

# 3. Обработка телефонов
for row in contacts_list[1:]:
    phone = row[5]
    if phone:
        # Приводим основной номер к формату +7(999)999-99-99
        phone = re.sub(r"(\+7|8)\s*\(?(\d{3})\)?[\s\-]*(\d{3})[\s\-]*(\d{2})[\s\-]*(\d{2})", r"+7(\2)\3-\4-\5", phone)
        # Обрабатываем добавочный номер, убирая все пробелы и скобки вокруг него
        phone = re.sub(r"\s*\(?доб\.\s*(\d+)\)?", r" доб.\1", phone)
        row[5] = phone

# 4. Объединение дублей по ФИ (firstname + lastname)
unique_contacts = {}
for row in contacts_list[1:]:
    key = (row[0], row[1])  # Фамилия + Имя
    if key not in unique_contacts:
        unique_contacts[key] = row
    else:
        # Заполняем пустые поля из дубля
        existing = unique_contacts[key]
        for i in range(len(row)):
            if not existing[i] and row[i]:
                existing[i] = row[i]

# 5. Собираем результат
result = [contacts_list[0]]  # заголовок
result.extend(unique_contacts.values())

# 6. Сохранение
with open("phonebook.csv", "w", encoding="utf-8-sig", newline="") as f:
    datawriter = csv.writer(f, delimiter=",")
    datawriter.writerows(result)

print("Готово! Результат сохранён в phonebook.csv")



