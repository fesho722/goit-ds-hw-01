import pickle
from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if not self.validate_phone(value):
            raise ValueError("Invalid phone number format")

    @staticmethod
    def validate_phone(phone):
        return len(phone) == 10 and phone.isdigit()


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)  # Виклик методу __init__ батьківського класу
        try:
            self.value = datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Невірний формат дати. Використовуйте ДД.ММ.РРРР")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                break

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                break

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name}, phones: {'; '.join(str(p) for p in self.phones)}, birthday: {self.birthday}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.today()
        next_week = today + timedelta(days=7)
        upcoming_birthdays = []
        for record in self.data.values():
            if record.birthday is not None:
                if today <= record.birthday.value < next_week:
                    upcoming_birthdays.append(record)
        return upcoming_birthdays


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter user name."
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Give me name and phone please."
    return inner


@input_error
def add_contact(args, book):
    if len(args) != 2:
        raise ValueError
    name, phone = args
    book.add_record(Record(name))
    book.data[name].add_phone(phone)
    return "Contact added."


@input_error
def change_contact(args, book):
    if len(args) != 2:
        raise IndexError
    name, phone = args
    if name in book.data:
        book.data[name].add_phone(phone)
        return "Contact updated."
    else:
        raise KeyError


@input_error
def show_phone(args, book):
    if len(args) != 1:
        raise ValueError
    name = args[0]
    if name in book.data:
        return book.data[name].phones[0].value
    else:
        raise KeyError


@input_error
def show_all(book):
    if not book.data:
        return "No contacts found."
    else:
        return "\n".join([f"{record.name}: {record.phones[0].value}" for record in book.data.values()])


@input_error
def add_birthday(args, book):
    if len(args) != 2:
        raise ValueError
    name, birthday = args
    if name in book.data:
        book.data[name].add_birthday(birthday)
        return "Birthday added to contact."
    else:
        raise KeyError


@input_error
def show_birthday(args, book):
    if len(args) != 1:
        raise ValueError
    name = args[0]
    if name in book.data:
        if book.data[name].birthday:
            return str(book.data[name].birthday.value)
        else:
            return "Birthday not set for this contact."
    else:
        raise KeyError


@input_error
def birthdays(args, book):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        return "\n".join([f"{record.name}: {record.birthday.value.strftime('%d.%m.%Y')}" for record in upcoming_birthdays])
    else:
        return "No upcoming birthdays."


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f, protocol=pickle.HIGHEST_PROTOCOL)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


def main():
    book = load_data()

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
