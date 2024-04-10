import csv
import os
import datetime


class Note:
    def __init__(self, id, title, body, timestamp):
        self.id = id
        self.title = title
        self.body = body
        self.timestamp = timestamp

    def to_csv(self):
        return f"{self.id};{self.title};{self.body};{self.timestamp}"

    @classmethod
    def from_csv(cls, csv_string):
        id, title, body, timestamp = csv_string.strip().split(";")
        return cls(int(id), title, body, datetime.datetime.fromisoformat(timestamp))

    def __str__(self):
        return f"ID: {self.id}\nTitle: {self.title}\nBody: {self.body}\nTimestamp: {self.timestamp}"


class NotesApp:
    def __init__(self, filename):
        self.filename = filename
        self.notes = []
        self.load_notes()

    def load_notes(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                reader = csv.reader(file, delimiter=";")
                for row in reader:
                    note = Note.from_csv(";".join(row))
                    self.notes.append(note)

    def save_notes(self):
        with open(self.filename, "w") as file:
            writer = csv.writer(file, delimiter=";")
            for note in self.notes:
                writer.writerow(note.to_csv().split(";"))

    def filter_notes_by_date(self, date):
        return [note for note in self.notes if note.timestamp.date() == date]

    def show_notes(self):
        for note in self.notes:
            print(note)

    def add_note(self, title, body):
        id = len(self.notes) + 1
        timestamp = datetime.datetime.now()
        self.notes.append(Note(id, title, body, timestamp))
        self.save_notes()

    def edit_note(self, id, title, body):
        for note in self.notes:
            if note.id == id:
                note.title = title
                note.body = body
                note.timestamp = datetime.datetime.now()
                break
        self.save_notes()

    def delete_note(self, id):
        self.notes = [note for note in self.notes if note.id != id]
        self.save_notes()

    def run(self):
        while True:
            print("\n1. Show all notes")
            print("2. Show notes filtered by date")
            print("3. Add a new note")
            print("4. Edit a note")
            print("5. Delete a note")
            print("6. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.show_notes()
            elif choice == "2":
                date_str = input("Enter date (YYYY-MM-DD): ")
                try:
                    date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                    filtered_notes = self.filter_notes_by_date(date)
                    for note in filtered_notes:
                        print(note)
                except ValueError:
                    print("Invalid date format. Please use YYYY-MM-DD.")
            elif choice == "3":
                title = input("Enter note title: ")
                body = input("Enter note body: ")
                self.add_note(title, body)
                print("Note added successfully.")
            elif choice == "4":
                id = int(input("Enter note ID to edit: "))
                title = input("Enter new title: ")
                body = input("Enter new body: ")
                self.edit_note(id, title, body)
                print("Note edited successfully.")
            elif choice == "5":
                id = int(input("Enter note ID to delete: "))
                self.delete_note(id)
                print("Note deleted successfully.")
            elif choice == "6":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    app = NotesApp("notes.csv")
    app.run()
