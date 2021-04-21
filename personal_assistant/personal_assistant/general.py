from os import stat_result


from personal_assistant import sort, phone_book as pb, notes_book as nb
from personal_assistant.commands import *

# general function


def parse_data(command, list):
    for i in list:
        if command.startswith(i):
            data = command.replace(i, '').strip()
            return data.split(' ')


def parse_command(command, **kwargs):
    for i in COMMANDS.keys():
        com = command.lower()
        if com.startswith(i):
            data = parse_data(com, i)
            mode = kwargs['MODE']
            record = kwargs['RECORD']
            cur_id = kwargs['ID']
            return COMMANDS[i](*data, MODE=mode, RECORD=record, ID=cur_id)
    return non_command()


def input_command(*args, **kwargs):
    mode = kwargs["MODE"]
    record = kwargs["RECORD"]
    cur_id = kwargs["ID"]
    command = input(
        f'( {CURRENT_MODES[mode]} mode {"" if not record else str(record) }) type command: ')
    result = parse_command(
        command, MODE=kwargs['MODE'], RECORD=record, ID=cur_id)
    if isinstance(result, (pb.Record, nb.NoteRecord)):
        command = input_command(MODE=mode, RECORD=result, ID=cur_id)
    if type(result) == tuple and isinstance(result[0], (pb.Record, nb.NoteRecord)) and result[1]:
        command = input_command(MODE=mode, RECORD=result[0], ID=result[1])
    return ''


def work_mode(*args, **kwargs):

    if args[0] in CURRENT_MODES.keys():
        print(f'We are in {CURRENT_MODES[args[0]]} mode')
        mode = args[0]
        record = None
        cur_id = None
        while True:
            result = input_command(MODE=mode, RECORD=record, ID=cur_id)
            if result == 'exit' and not record:
                print("Good Bye!")
                break
            elif result == 'exit' and record:
                record = None
            elif result:
                print(result)
    else:
        pass


def p_a():
    print('Hi! I\'m your personal helper (PH). For more information type "help"')
    while True:
        mode = None
        record = None
        cur_id = None
        result = input('PH says - please, select a workmode or "exit":')
        if result in ('1', '2', '3'):
            work_mode(result)
        else:
            result = parse_command(result, MODE=mode, RECORD=record, ID=cur_id)
        if result == 'exit':
            print("Good Bye!")
            break


if __name__ == '__main__':
    p_a()
