class LibraryError(Exception):
    pass

class BookNotFoundError(LibraryError):
    pass

class BookNotAvailableError(LibraryError):
    pass

class LimitExceededError(LibraryError):
    pass

class Book:
    def __init__(self, isbn, title, author, year, is_available=True):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        self.is_available = is_available

    def __str__(self):
        return f"{self.title} - {self.author} ({self.year})"

    def __repr__(self):
        return f"Book(isbn={self.isbn!r}, title={self.title!r})"

class Member:
    MAX_BOOKS = 3

    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
        self.borrowed_books = []

    def can_borrow(self):
        return True if len(self.borrowed_books) < self.MAX_BOOKS else False

    def __str__(self):
        return f"{self.name} (books: {len(self.borrowed_books)}/{self.MAX_BOOKS})"

class Library:
    def __init__(self, name):
        self.name = name
        self.books = {}
        self.members = {}

    def add_book(self, book):
        self.books[book.isbn] = book

    def add_member(self, member):
        self.members[member.member_id] = member

    def lend_book(self, isbn, member_id):
        if member_id not in self.members:
            raise LibraryError(f"Member {member_id} not available")

        if isbn not in self.books:
            raise BookNotFoundError(f"Book {isbn} not found")

        book = self.books[isbn]

        if  not book.is_available:
            raise BookNotAvailableError(f"Book {isbn} not available")

        member = self.members[member_id]

        if  not member.can_borrow():
            raise LimitExceededError(f"{member.name} has reached the limit of {Member.MAX_BOOKS}")
        book.is_available = False
        member.borrowed_books.append(book)
        return f"{member.name} borrowed «{book}"

    def return_book(self, isbn, member_id):
        if member_id not in self.members:
            raise LibraryError(f"Member {member_id} not available")

        if isbn not in self.books:
            raise BookNotFoundError(f"Book {isbn} not found")

        book = self.books[isbn]
        member = self.members[member_id]

        if book not in member.borrowed_books:
            raise LibraryError(f"Member {member.name} hasn't borrowed {book}")

        book.is_available = True
        member.borrowed_books.remove(book)
        return f"{member.name} has returned {book}"

