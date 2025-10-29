
class Book:
    def __init__(self, book_id, title, author, status="Available"):
        self.bookID = book_id
        self.title = title
        self.author = author
        self.status = status
        self.next = None



class BookList:
    def __init__(self):
        self.head = None

    def insert_book(self, book_id, title, author):
        temp = self.head
        while temp:
            if temp.bookID == book_id:
                print(f"Book ID {book_id} already exists! Insertion cancelled.")
                return
            temp = temp.next

        new_book = Book(book_id, title, author)
        if not self.head:
            self.head = new_book
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_book
        print(f'Book "{title}" added successfully!')

    def delete_book(self, book_id):
        temp = self.head
        prev = None
        while temp:
            if temp.bookID == book_id:
                if prev:
                    prev.next = temp.next
                else:
                    self.head = temp.next
                print(f"Book ID {book_id} deleted successfully.")
                return
            prev = temp
            temp = temp.next
        print("Book not found.")

    def search_book(self, book_id):
        temp = self.head
        while temp:
            if temp.bookID == book_id:
                return temp
            temp = temp.next
        return None

    def display_books(self):
        if not self.head:
            print("No books available in the library.")
            return
        print("\nCurrent Books in Library:")
        print("----------------------------------------------")
        temp = self.head
        while temp:
            print(f"ID: {temp.bookID} | Title: {temp.title} | Author: {temp.author} | Status: {temp.status}")
            temp = temp.next
        print("----------------------------------------------")



class Transaction:
    def __init__(self, book_id, action, prev_status):
        self.bookID = book_id
        self.action = action
        self.prev_status = prev_status


class TransactionStack:
    def __init__(self):
        self.transactions = []

    def push(self, t):
        self.transactions.append(t)

    def pop(self):
        if not self.transactions:
            return None
        return self.transactions.pop()

    def display(self):
        if not self.transactions:
            print("No transactions yet.")
            return
        print("\nTransaction History:")
        for t in reversed(self.transactions):
            print(f"Book ID {t.bookID} -> {t.action} (prev status={t.prev_status})")



class LibrarySystem:
    def __init__(self):
        self.book_list = BookList()
        self.transaction_stack = TransactionStack()

    def insert_book(self):
        try:
            book_id = int(input("Enter Book ID: "))
        except:
            print("Invalid input!")
            return
        title = input("Enter Title: ")
        author = input("Enter Author: ")
        self.book_list.insert_book(book_id, title, author)

    def delete_book(self):
        try:
            book_id = int(input("Enter Book ID to delete: "))
        except:
            print("Invalid input!")
            return
        self.book_list.delete_book(book_id)

    def search_book(self):
        try:
            book_id = int(input("Enter Book ID to search: "))
        except:
            print("Invalid input!")
            return
        b = self.book_list.search_book(book_id)
        if b:
            print(f"\nFOUND -> ID:{b.bookID} | Title:{b.title} | Author:{b.author} | Status:{b.status}\n")
        else:
            print("Book not found.")

    def issue_book(self):
        try:
            book_id = int(input("Enter Book ID to issue: "))
        except:
            print("Invalid input!")
            return
        book = self.book_list.search_book(book_id)
        if not book:
            print("Book not found.")
            return
        if book.status == "Issued":
            print("Book already issued.")
            return
        prev = book.status
        book.status = "Issued"
        self.transaction_stack.push(Transaction(book_id, "issue", prev))
        print(f"Book ID {book_id} issued.")

    def return_book(self):
        try:
            book_id = int(input("Enter Book ID to return: "))
        except:
            print("Invalid input!")
            return
        book = self.book_list.search_book(book_id)
        if not book:
            print("Book not found.")
            return
        if book.status == "Available":
            print("Book is already available.")
            return
        prev = book.status
        book.status = "Available"
        self.transaction_stack.push(Transaction(book_id, "return", prev))
        print(f"Book ID {book_id} returned.")

    def undo_transaction(self):
        t = self.transaction_stack.pop()
        if not t:
            print("No transactions to undo.")
            return
        book = self.book_list.search_book(t.bookID)
        if not book:
            print("Book record not found for undo.")
            return
        book.status = t.prev_status
        print(f"UNDO DONE → Book ID {t.bookID} status restored to {t.prev_status}")

    def view_transactions(self):
        self.transaction_stack.display()

    def display_books(self):
        self.book_list.display_books()

    def menu(self):
        while True:
            print("\n==== Library Book Management System ====")
            print("1. Insert Book")
            print("2. Delete Book")
            print("3. Search Book")
            print("4. Issue Book")
            print("5. Return Book")
            print("6. Undo Last Transaction")
            print("7. View Transactions")
            print("8. Display All Books")
            print("9. Exit")
            ch = input("Enter choice: ")

            if ch == '1': self.insert_book()
            elif ch == '2': self.delete_book()
            elif ch == '3': self.search_book()
            elif ch == '4': self.issue_book()
            elif ch == '5': self.return_book()
            elif ch == '6': self.undo_transaction()
            elif ch == '7': self.view_transactions()
            elif ch == '8': self.display_books()
            elif ch == '9':
                print("Goodbye!"); break
            else: print("Invalid choice!")



if __name__ == "__main__":
    LibrarySystem().menu()
