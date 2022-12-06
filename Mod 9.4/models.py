import json


class Books:
    def __init__(self):
        try:
            with open("books.json", "r") as f:
                self.books = json.load(f)
        except FileNotFoundError:
            self.books = []

    def all(self):
        return self.books

    def get(self, id):
        book = [book for book in self.all() if book['id'] == id]
        if book:
            return book[0]
        return []

    def save_all(self):
        with open("books.json", "w") as f:
            json.dump(self.books, f)

    def create(self, data):
        self.books.append(data)
        self.save_all()

    def get_2(self, id):
        return self.books[id]

    def update_2(self, id, data):
        data.pop('csrf_token')
        self.books[id] = data
        self.save_all()

    def update(self, id, data):
        book=self.get(id)
        if book:
            index = self.books.index(book)
            self.books[index]=data
            self.save_all()
            return True
        return False

    def delete(self, id):
        book = self.get(id)
        if book:
            self.books.remove(book)
            self.save_all()
            return True
        return False

        
books = Books()