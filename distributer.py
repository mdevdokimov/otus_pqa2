import csv
import json
from pathlib import Path
# from typing import List, Dict, Union

BASE_DIR = Path(__file__).resolve().parent

class FileWorker:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = ""

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        print(f"файл {self.filename} открыт")
        return self.file

    def __exit__(self, exc_type, exc, tb):
        self.file.close()

        if exc_type is not None:
            print(f"Ошибка при выходе из файла: {exc_type}")

        return True


def json_read(filename):
    file_path = BASE_DIR / "tmpdata" / filename
    with FileWorker(file_path, "r") as f:
        return json.load(f)

def json_write(filename, data):
    file_path = BASE_DIR / "tmpdata" / filename
    with FileWorker(file_path, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def csv_read(filename):
    file_path = BASE_DIR / "tmpdata" / filename
    with FileWorker(file_path, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)


if __name__ == "__main__":

    books = csv_read("books.csv")
    # print(books)
    # book = [{'Title': 'Fundamentals of Wavelets', 'Author': 'Goswami, Jaideva', 'Genre': 'signal_processing', 'Pages': '228', 'Publisher': 'Wiley'}]
    users = json_read("users.json")
    need_keys = {"name", "gender", "address", "age"}
    new_users = []
    for user in users:
        # print(user)
        cl_user = {key: user[key] for key in need_keys if key in user}
        cl_user["books"] = []
        new_users.append(cl_user)

    for index, book in enumerate(books):
        new_users[index % len(new_users)]["books"].append(book)

    json_write("result.json", new_users)
    print(new_users)

