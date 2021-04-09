from os import error
import phone_book as ph

# tuple with commands words
EXIT_COMMANDS = ("good bye", "close", "exit", "bye")
ADD_COMMANDS = ("add", "+")
GREETING_COMMANDS = ("hello", "alloha",)
SHOW_PHONE_COMMANDS = ("phone", "pb")
SHOW_ALL_COMMANDS = ("show all", "show")
HELP_COMMANDS = ("help",)
CURRENT_MODES = {'1': 'PoneBook mode',
                 '2': 'Notes mode', '3': 'Clear folder mode'}
CURRENT_MODE = ''

# command helpers


def add_command(*args):
    if CURRENT_MODE == '1':
        if not ph.load_addressBook():
            ad = ph.AddressBook()
        else:
            ad = ph.load_addressBook()
        name = ph.Name(input('Contact name (required): '))
        print(name.value)

        while True:
            try:
                phone = ph.Phone(input('Contact phone (required): '))
                break
            except ValueError as e:
                print(e)
        print(phone.value)

        while True:
            try:
                birthday = ph.Birthday(input('Contact birthday (optional): '))
                break
            except ValueError as e:
                print(e)
        print(birthday.value)
        record = ph.Record(name, phone, birthday)
        confirm = input(
            f'Add record {record.records} to address book (y/n)?: ')
        if confirm.lower() == 'y':
            ad.add_record(record)
            ph.save_addressBook(ad)


def greeting_command(*args):
    print(f'in greeting_command')


def show_phone_command(*args):
    print(f'in show_phone_command')
    ph.load_addressBook()
    ph.Phone


def show_all_command(*args):
    if CURRENT_MODE == '1':
        if not ph.load_addressBook():
            ad = ph.AddressBook()
        else:
            ad = ph.load_addressBook()
        print(ad.values())


def help_command(*args):
    print(f"""I can work in different mode.\n
            1. First - {CURRENT_MODES['1']} \n
            2. Second - {CURRENT_MODES['2']} \n
            3. Third - {CURRENT_MODES['3']}\n
            in each mode you can call command 'halp' to more information""")


def exit_command(*args):
    return('exit')


COMMANDS = {ADD_COMMANDS: add_command, GREETING_COMMANDS: greeting_command,
            SHOW_PHONE_COMMANDS: show_phone_command, SHOW_ALL_COMMANDS: show_all_command, EXIT_COMMANDS: exit_command, HELP_COMMANDS: help_command}


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
        result = input('PH says - please, chose workmode or "exit":')
        if result in ('1', '2', '3'):
            work_mode(result)
        else:
            result = parse_command(result)
        if result == 'exit':
            print("Good Bye!")
            break
        print(result)
