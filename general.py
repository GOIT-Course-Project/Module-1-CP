from os import error


import phone_book as pb
import notes_book as nb

# tuple with commands words
EXIT_COMMANDS = ("good bye", "close", "exit", "bye")
ADD_COMMANDS = ("add", "+")
DELTE_COMMANDS = ("-", "del", "delete")
GREETING_COMMANDS = ("hello", "alloha",)
SHOW_PHONE_COMMANDS = ("pbone", "pb")
SHOW_ALL_COMMANDS = ("show all", "show")
HELP_COMMANDS = ("help",)
CURRENT_MODES = {'1': 'PhoneBook mode',
                 '2': 'Notes mode', '3': 'Clear folder mode'}
CURRENT_MODE = ''

# command helpers


def loadAB():
    if not pb.load_addressBook():
        ab = pb.AddressBook()
    else:
        ab = pb.load_addressBook()

    return ab


def add_phone(*args):

    ab = loadAB()

    name = pb.Name(input('Contact name (required): '))
    print(name.value)

    address = pb.Address(input('Contact address (optional): '))

    while True:
        try:
            phone = pb.Phone(input('Contact phone (required): '))
            break
        except ValueError as e:
            print(e)
    print(phone.value)

    while True:
        try:
            birthday = pb.Birthday(input('Contact birthday (optional): '))
            break
        except ValueError as e:
            print(e)
    print(birthday.value)

    while True:
        try:
            email = pb.Email(input('Contact email (optional): '))
            break
        except ValueError as e:
            print(e)
    print(email.value)

    record = pb.Record(name, address, phone, birthday, email)
    confirm = input(
        f'Add record {record.records} to address book (y/n)?: ')
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


def add_notes(*args):
    if not nb.load_notesBook():
        notesB = nb.NotesBook()
    else:
        notesB = nb.load_notesBook()

    while True:
        try:
            note = nb.Note(input('Type your notes (required): '))
            break
        except ValueError as e:
            print(e)
    print(note.value)

    while True:
        try:
            teg = nb.Teg(input('Type Teg for your notes (required): '))
            break
        except ValueError as e:
            print(e)
    print(teg.value)

    record = nb.NoteRecord(note, teg)

    confirm = input(
        f'Add notes {record.noterecors} to NotessBook (y/n)?: ')
    if confirm.lower() == 'y':
        notesB.add_record(record)
        nb.save_notesBook(notesB)


def add_command(*args):
    if CURRENT_MODE == '1':
        add_phone()
    if CURRENT_MODE == '2':
        add_notes()


def greeting_command(*args):
    print(f'in greeting_command')


def show_phone_command(*args):
    print(f'in show_pbone_command')
    pb.load_addressBook()


def show_all_command(*args):
    if CURRENT_MODE == '1':
        if not pb.load_addressBook():
            ab = pb.AddressBook()
        else:
            ab = pb.load_addressBook()
        print(ab)

    if CURRENT_MODE == '2':
        if not nb.load_notesBook():
            noteB = nb.NotesBook()
        else:
            noteB = nb.load_notesBook()
        print(noteB.values())


def help_command(*args):
    print(f"""I can work in different mode.\n
            1. First - {CURRENT_MODES['1']} \n
            2. Second - {CURRENT_MODES['2']} \n
            3. Third - {CURRENT_MODES['3']}\n
            in each mode you can call command 'help' for more information""")


def delete_command(*args):
    if CURRENT_MODE == '1':
        print(delete_ab_record(args[0]))


def exit_command(*args):
    return('exit')


COMMANDS = {ADD_COMMANDS: add_command, GREETING_COMMANDS: greeting_command,
            SHOW_PHONE_COMMANDS: show_phone_command, SHOW_ALL_COMMANDS: show_all_command, EXIT_COMMANDS: exit_command, HELP_COMMANDS: help_command, DELTE_COMMANDS: delete_command}


# general function


def non_command():
    return 'Sorry, i don`t know this command'


def parse_data(command, list):
    for i in list:
        if command.startswith(i):
            return command.replace(i, '').strip()


def parse_command(command):
    for i in COMMANDS.keys():
        com = command.lower()
        if com.startswith(i):
            data = parse_data(command, i)
            return COMMANDS[i](data)
    return non_command()


def work_mode(*args):
    global CURRENT_MODE
    if args[0] in CURRENT_MODES.keys():
        print(f'We are in {CURRENT_MODES[args[0]]}')
        CURRENT_MODE = args[0]
        while True:
            result = parse_command(
                input(f'({CURRENT_MODES[args[0]]}) type command: '))
            if result == 'exit':
                print("Good Bye!")
                CURRENT_MODE = ''
                break
            print(result)
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
