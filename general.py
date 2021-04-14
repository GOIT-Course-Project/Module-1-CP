from os import error, name, supports_bytes_environ
import re


import phone_book as pb
import notes_book as nb

# tuple with commands words
EXIT_COMMANDS = ("good bye", "close", "exit", "bye")
FIND_COMMANDS = ("find",)
EDIT_COMMANDS = ("edit",)
BIRTHDAY_COMMANDS = ("birthday",)
SELECT_COMMANDS = ("select",)
ADD_COMMANDS = ("add", "+")
DELETE_COMMANDS = ("delete", "del", "-",)
GREETING_COMMANDS = ("hello", "alloha",)
SHOW_ALL_COMMANDS = ("show all", "show")
HELP_COMMANDS = ("help",)
CURRENT_MODES = {'1': 'PhoneBook mode',
                 '2': 'Notes mode', '3': 'Clear folder mode'}
CURRENT_MODE = ''
CURRENT_RECORD = None
CURRENT_ID = None


# function helpers

def loadAB():
    if not pb.load_addressBook():
        ab = pb.AddressBook()
    else:
        ab = pb.load_addressBook()

    return ab


def load_obj_record(rec):

    if CURRENT_MODE == '1':
        return pb.Record(pb.Name(rec['name']), pb.Email(rec['email']), pb.Address(rec['address']), pb.Birthday(rec['birthday']), *(pb.Phone(i) for i in rec['phones']))
    elif CURRENT_MODE == '2':
        return nb.NoteRecord(nb.Note(rec['Note']), nb.Teg(rec['Teg']))


def loadNB():
    if not nb.load_notesBook():
        notesB = nb.NotesBook()
    else:
        notesB = nb.load_notesBook()
    return notesB


def input_name():
    while True:
        result = input('Contact name (required): ')
        if len(result) >= 3:
            return pb.Name(result)
        else:
            print("Name must have 3 or more characters!!")


def input_phone():
    while True:
        try:
            phone = pb.Phone(input('Contact phone (required): '))
            break
        except ValueError as e:
            print(e)
    return phone


def input_birthday():
    while True:
        try:
            birthday = pb.Birthday(
                input('Contact birthday "MM-DD" format (optional): '))
            break
        except ValueError as e:
            print(e)
    return birthday


def input_email():
    while True:
        try:
            email = pb.Email(input('Contact email (optional): '))
            break
        except ValueError as e:
            print(e)
    return email


def input_address():
    return pb.Address(input('New address: '))


def input_note():
    while True:
        try:
            note = nb.Note(input('Type your notes (required): '))
            break
        except ValueError as e:
            print(e)
    return note


def input_teg():
    while True:
        try:
            teg = nb.Teg(input('Type Teg for your notes (optional): '))
            break
        except ValueError as e:
            print(e)
    return teg


def add_contact(*args):

    ab = loadAB()

    name = input_name()

    address = pb.Address(input('Contact address (optional): '))

    phone = input_phone()

    birthday = input_birthday()

    email = input_email()

    record = pb.Record(name, address, phone, birthday, email)
    confirm = input(
        f'Add record {record} to address book (y/n)?: ')
    if confirm.lower() == 'y':
        ab.add_record(record)
        pb.save_addressBook(ab)


def delete_ab_record(id):
    if not id:
        return (f'Soryy, for deleting type id record after command')
    else:
        ab = loadAB()
        ab.delete_record(int(id))
        pb.save_addressBook(ab)


def delete_nb_record(id):
    if not id:
        return (f'Soryy, for deleting type id record after command')
    else:
        noteB = loadNB()
        noteB.delete_record(int(id))
        nb.save_notesBook(noteB)


def add_notes(*args):
    notesB = loadNB()

    note = input_note()

    teg = input_teg()

    record = nb.NoteRecord(note, teg)

    confirm = input(
        f'Add notes {record.noterecors} to NotessBook (y/n)?: ')
    if confirm.lower() == 'y':
        notesB.add_record(record)
        nb.save_notesBook(notesB)


def update_ab(record):
    global CURRENT_RECORD, CURRENT_ID
    delete_ab_record(CURRENT_ID)
    ab = loadAB()
    ab.add_record(record)
    pb.save_addressBook(ab)
    CURRENT_ID = None
    CURRENT_RECORD = None


def update_nb(record):
    global CURRENT_RECORD, CURRENT_ID
    delete_nb_record(CURRENT_ID)
    noteB = loadNB()
    noteB.add_record(record)
    nb.save_notesBook(noteB)
    CURRENT_ID = None
    CURRENT_RECORD = None


def phone_add(*args):
    if CURRENT_MODE == '1' and CURRENT_RECORD:
        phone = input_phone()
        CURRENT_RECORD.add_phone(phone)
        update_ab(CURRENT_RECORD)

# commands functions


def add_command(*args):
    if CURRENT_MODE == '1' and not CURRENT_RECORD:
        add_contact()
    elif CURRENT_MODE == '1' and CURRENT_RECORD and args[0] == 'phone':
        phone_add()
    if CURRENT_MODE == '2':
        add_notes()


def birthday_command(*args):
    result = []

    if CURRENT_MODE == '1':
        ab = loadAB()
        for key, rec in ab.data.items():

            if not args[0] == '':
                if not args[0].isdigit():
                    return print(f'Parametr must be a digits')
                if load_obj_record(rec).days_to_birthday() <= int(args[0]):
                    result.append(ab[key])
            else:
                result.append(
                    f'id - {key} | name - {rec["name"]} | birthday - {rec["birthday"]}')
    if len(result) == 0:
        result.append(
            f'You are a happy man \N{grinning face with smiling eyes}')

    for i in result:
        print(i)


def greeting_command(*args):
    print(f'in greeting_command')


def show_all_command(*args):
    if CURRENT_MODE == '1' and not CURRENT_RECORD:
        ab = loadAB()
        print(ab)
    else:
        print(CURRENT_RECORD)

    if CURRENT_MODE == '2':
        if not nb.load_notesBook():
            noteB = nb.NotesBook()
        else:
            noteB = nb.load_notesBook()
        print(noteB)


def select_command(*args):
    global CURRENT_RECORD, CURRENT_ID
    if CURRENT_MODE == '1':
        ab = loadAB()
        CURRENT_ID = args[0]
        try:
            CURRENT_RECORD = load_obj_record(ab.data[int(CURRENT_ID)])
        except KeyError as e:
            print(f'Sorry, PhoneBook has no record with id {e}')
        # pb.Record(pb.Name(ab[int(args[0])]['name']), pb.Email(ab[int(args[0])]['email']), pb.Address(
        #     ab[int(args[0])]['address']), pb.Birthday(ab[int(args[0])]['birthday']), *(pb.Phone(i) for i in ab[int(args[0])]['phones']))
    elif CURRENT_MODE == '2':
        noteB = loadNB()
        CURRENT_ID = args[0]
        CURRENT_RECORD = load_obj_record(noteB.data[int(CURRENT_ID)])


def edit_command(*args):

    if CURRENT_MODE == '1' and CURRENT_RECORD and args[0].lower() == 'phone':
        new_phone = input_phone()
        CURRENT_RECORD.delete_phone(int(args[0]))
        CURRENT_RECORD.add_phone(new_phone)
        update_ab(CURRENT_RECORD)

    elif CURRENT_MODE == '1' and CURRENT_RECORD and args[0].lower() == 'name':
        CURRENT_RECORD.records['name'] = input_name()
        update_ab(CURRENT_RECORD)

    elif CURRENT_MODE == '1' and CURRENT_RECORD and args[0].lower() == 'birthday':
        CURRENT_RECORD.records['birthday'] = input_birthday().value
        update_ab(CURRENT_RECORD)

    elif CURRENT_MODE == '1' and CURRENT_RECORD and args[0].lower() == 'email':
        CURRENT_RECORD.records['email'] = input_email().value
        update_ab(CURRENT_RECORD)

    elif CURRENT_MODE == '1' and CURRENT_RECORD and args[0].lower() == 'address':
        CURRENT_RECORD.records['address'] = input_address().value
        update_ab(CURRENT_RECORD)

    elif CURRENT_MODE == '2' and CURRENT_RECORD and args[0].lower() == 'note':
        CURRENT_RECORD.edit_note(input_note())
        update_nb(CURRENT_RECORD)

    elif CURRENT_MODE == '2' and CURRENT_RECORD and args[0].lower() == 'teg':
        CURRENT_RECORD.edit_teg(input_teg())
        update_nb(CURRENT_RECORD)


def help_command(*args):
    if CURRENT_MODE == '1':
        print(f"""In {CURRENT_MODES[CURRENT_MODE]}.\n
            You can see all records in your AddressBook - just type "Show" command \n
            You can add, delete or edit record in your AddressBook\n
            For adding type "add" or "+" \n
            For deleting type "del" or "-" and specify the id record \n
            Before editing you must select record, type "select" and specify the id \n """)
    else:
        print(f"""I can work in different mode.\n
            1. First - {CURRENT_MODES['1']} \n
            2. Second - {CURRENT_MODES['2']} \n
            3. Third - {CURRENT_MODES['3']}\n
            in each mode you can call command 'help' for more information""")


def delete_command(*args):
    if CURRENT_MODE == '1' and not CURRENT_RECORD and args[0].isdigit():
        delete_ab_record(args[0])
    elif CURRENT_MODE == '1' and CURRENT_RECORD and args[0] == 'phone':
        CURRENT_RECORD.delete_phone(int(args[1]))
        update_ab(CURRENT_RECORD)
    elif CURRENT_MODE == '2' and not CURRENT_RECORD and args[0].isdigit():
        delete_nb_record(args[0])


def find_command(*args):
    if CURRENT_MODE == '1':
        ab = loadAB()
        try:
            for value in ab.find(args[0]):
                print(value)
        except ValueError as e:
            print(e)

    if CURRENT_MODE == '2':
        noteB = loadNB()
        try:
            for value in noteB.find_note(args[0]):
                print(value)
        except ValueError as e:
            print(e)


def exit_command(*args):
    global CURRENT_RECORD
    CURRENT_RECORD = None
    return('exit')


COMMANDS = {ADD_COMMANDS: add_command, GREETING_COMMANDS: greeting_command, SHOW_ALL_COMMANDS: show_all_command,
            EXIT_COMMANDS: exit_command, HELP_COMMANDS: help_command, DELETE_COMMANDS: delete_command,
            SELECT_COMMANDS: select_command, EDIT_COMMANDS: edit_command, FIND_COMMANDS: find_command, BIRTHDAY_COMMANDS: birthday_command}


# general function


def non_command():
    return 'Sorry, i don`t know this command'


def parse_data(command, list):
    for i in list:
        if command.startswith(i):
            data = command.replace(i, '').strip()
            return data.split(' ')


def parse_command(command):
    for i in COMMANDS.keys():
        com = command.lower()
        if com.startswith(i):
            data = parse_data(command, i)
            return COMMANDS[i](*data)
    return non_command()


def work_mode(*args):
    global CURRENT_MODE
    if args[0] in CURRENT_MODES.keys():
        print(f'We are in {CURRENT_MODES[args[0]]}')
        CURRENT_MODE = args[0]
        while True:
            result = parse_command(
                input(f'({CURRENT_MODES[args[0]]} {"" if not CURRENT_RECORD else str(CURRENT_RECORD) }) type command: '))
            if result == 'exit':
                print("Good Bye!")
                CURRENT_MODE = ''
                break
    else:
        pass


if __name__ == '__main__':
    print('Hi! I\'m your personal helper (PH). For more information type "help"')
    while True:
        result = input('PH says - please, select a workmode or "exit":')
        if result in ('1', '2', '3'):
            work_mode(result)
        else:
            result = parse_command(result)
        if result == 'exit':
            print("Good Bye!")
            break
    print(result)
