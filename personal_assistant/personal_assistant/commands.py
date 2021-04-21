import os.path


from personal_assistant.helpers_commands import *

CURRENT_MODES = {'1': 'PhoneBook',
                 '2': 'NotesBook', '3': 'SortFolder'}

EXIT_COMMANDS = ("good bye", "close", "exit", "bye")
FIND_COMMANDS = ("find",)
EDIT_COMMANDS = ("edit",)
BIRTHDAY_COMMANDS = ("birthday",)
SELECT_COMMANDS = ("select", "sel")
ADD_COMMANDS = ("add", "+")
DELETE_COMMANDS = ("delete", "del", "-",)
GREETING_COMMANDS = ("hello", "alloha",)
SHOW_ALL_COMMANDS = ("show all", "show")
HELP_COMMANDS = ("help",)
SORT_COMMANDS = ("sort",)


def add_command(*args, **kwargs):
    mode = kwargs["MODE"]
    record = kwargs["RECORD"]
    cur_id = kwargs["ID"]

    if mode == '1' and not record:
        add_contact()
    elif mode == '1' and record and args[0] == 'phone':
        phone = input_phone()
        record.add_phone(phone)
        update_ab(RECORD=record, ID=cur_id)
    if mode == '2':
        add_notes()


def birthday_command(*args, **kwargs):
    result = []

    if kwargs["MODE"] == '1':
        ab = loadAB()
        for key, rec in ab.data.items():

            if not args[0] == '':
                if not args[0].isdigit():
                    return print(f'Parametr must be a digits')
                if rec.days_to_birthday() <= int(args[0]):
                    result.append(ab[key])
            else:
                result.append(
                    f'id - {key} | name - {rec["name"]} | birthday - {rec["birthday"]}')
    if len(result) == 0:
        result.append(
            f'You are a happy man \N{grinning face with smiling eyes}')

    for i in result:
        print(i)


def greeting_command(*args, **kwargs):
    print(f'Hello! i\'m your personal assistan.')


def show_all_command(*args, **kwargs):
    mode = kwargs['MODE']
    record = kwargs['RECORD']
    if mode == '1' and not record:
        ab = loadAB()
        print(ab)
    elif mode == '2':
        noteB = loadNB()
        for key in noteB.data.keys():
            print(noteB[key])
    else:
        print(record)


def select_command(*args, **kwargs):
    mode = kwargs["MODE"]
    record = kwargs["RECORD"]
    cur_id = kwargs["ID"]

    if check_id(args[0]):
        cur_id = args[0]
    else:
        print(f'Parametr "id" must be a digit not "{args[0]}"')
        return None
    if mode == '1':
        ab = loadAB()
        try:
            return ab[int(cur_id)], cur_id
        except KeyError as e:
            print(f'Sorry, PhoneBook has no record with id {e}')

    elif mode == '2':
        noteB = loadNB()
        try:
            return noteB[int(cur_id)]
        except KeyError as e:
            print(f'Sorry, NoteBook has no record with id {e}')


def edit_command(*args, **kwargs):

    mode = kwargs["MODE"]
    record = kwargs["RECORD"]
    cur_id = kwargs["ID"]

    if not record:
        print(f'Before editing record - please, select it. (Command "select id_record")')
        return None

    if not args[0]:
        print(f'For edit field please type fieldname after command "edit"')
        return None

    if mode == '1' and record and args[0].lower() == 'phone':
        try:
            CURRENT_ID = args[1]
        except IndexError:
            print(f'Please type id phone after command')
            return None
        if not check_id(CURRENT_ID):
            print(f'Parametr "id" must be a digit not "{CURRENT_ID}"')
            return None
        new_phone = input_phone()
        record.edit_phone(int(CURRENT_ID), new_phone)
        update_ab(RECORD=record, ID=cur_id)

    elif mode == '1' and record and args[0].lower() == 'name':
        record.records['name'] = input_name().value
        update_ab(RECORD=record, ID=cur_id)

    elif mode == '1' and record and args[0].lower() == 'birthday':
        record.records['birthday'] = input_birthday().value
        update_ab(RECORD=record, ID=cur_id)

    elif mode == '1' and record and args[0].lower() == 'email':
        record.records['email'] = input_email().value
        update_ab(RECORD=record, ID=cur_id)

    elif mode == '1' and record and args[0].lower() == 'address':
        record.records['address'] = input_address().value
        update_ab(RECORD=record, ID=cur_id)

    elif mode == '2' and record and args[0].lower() == 'note':
        record.edit_note(input_note())
        update_nb(record)

    elif mode == '2' and record and args[0].lower() == 'teg':
        record.edit_teg(input_teg())
        update_nb(record)

    else:
        print(non_command())


def help_command(*args, **kwargs):
    mode = kwargs["MODE"]
    record = kwargs["RECORD"]
    cur_id = kwargs["ID"]

    if mode == '1' or mode == '2':
        print(f"""In {CURRENT_MODES[mode]} mode.
            You can see all records in your {CURRENT_MODES[mode]} - just type {SHOW_ALL_COMMANDS} command
            You can add, delete or edit record in your AddressBook
            For adding type {ADD_COMMANDS}
            For deleting type {DELETE_COMMANDS} and specify the id record
            Before editing you must select record, type {SELECT_COMMANDS} and specify the id""")
    elif mode == '3':
        print(f"""In {CURRENT_MODES[mode]} mode.
            You can sort and organize your folders, just type command "sort" and PATH to folder""")
    else:
        print(f"""I can work in different mode.
            1 - {CURRENT_MODES['1']} mode
            2 - {CURRENT_MODES['2']} mode
            3 - {CURRENT_MODES['3']} mode
            in each mode you can call command 'help' for more information""")


def delete_command(*args, **kwargs):
    mode = kwargs["MODE"]
    record = kwargs["RECORD"]
    cur_id = kwargs["ID"]

    if args[0] == '':
        print(f'For delete record please type id after command')
        return None
    if mode == '1' and not record:
        delete_ab_record(args[0])
        print((f'Record delete succsesful.'))
    elif mode == '1' and record and args[0] == 'phone':
        record.delete_phone(int(args[1]))
        print((f'Phone delete succsesful.'))
        update_ab(record)
    elif mode == '2' and not record:
        delete_nb_record(args[0])
        print((f'Record delete succsesful.'))


def find_command(*args, **kwargs):
    mode = kwargs["MODE"]
    record = kwargs["RECORD"]
    cur_id = kwargs["ID"]

    if mode == '1':
        ab = loadAB()
        try:
            for value in ab.find(args[0]):
                print(value)
        except ValueError as e:
            print(e)

    if mode == '2':
        noteB = loadNB()
        try:
            for value in noteB.find_note(args[0]):
                print(value)
        except ValueError as e:
            print(e)


def sort_command(*args, **kwargs):
    mode = kwargs["MODE"]
    record = kwargs["RECORD"]
    cur_id = kwargs["ID"]

    if mode == '3':

        if not args[0]:
            print(f'You must type PATH to folder')
            return None
        if os.path.exists(args[0]):
            if sort.grabPath(args[0]):
                print(f'Directory with PATH {args[0]} sort successful.')
        else:
            print(f'Sorry, directory with PATH {args[0]} not exist')


def exit_command(*args, **kwargs):
    return 'exit'


def non_command():
    return 'Sorry, i don`t know this command'


COMMANDS = {ADD_COMMANDS: add_command, GREETING_COMMANDS: greeting_command, SHOW_ALL_COMMANDS: show_all_command,
            EXIT_COMMANDS: exit_command, HELP_COMMANDS: help_command, DELETE_COMMANDS: delete_command,
            SELECT_COMMANDS: select_command, EDIT_COMMANDS: edit_command, FIND_COMMANDS: find_command,
            BIRTHDAY_COMMANDS: birthday_command, SORT_COMMANDS: sort_command}
