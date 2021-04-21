from personal_assistant import sort, phone_book as pb, notes_book as nb


def add_contact(*args, **kwargs):

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
        print(ab.add_record(record))
        pb.save_addressBook(ab)


def add_notes(*args, **kwargs):
    notesB = loadNB()

    note = input_note()

    teg = input_teg()

    record = nb.NoteRecord(note, teg)

    confirm = input(
        f'Add notes {record.noterecors} to NotessBook (y/n)?: ')
    if confirm.lower() == 'y':
        print(notesB.add_record(record))
        nb.save_notesBook(notesB)


def check_id(id):
    result = False
    if id.isdigit():
        result = True
    return result


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
            note = nb.Note(input('Type your note (required): '))
            break
        except ValueError as e:
            print(e)
    return note


def input_teg():
    while True:
        try:
            teg = nb.Teg(input('Type Teg for your note (optional): '))
            break
        except ValueError as e:
            print(e)
    return teg


def loadAB():
    if not pb.load_addressBook():
        ab = pb.AddressBook()
    else:
        ab = pb.load_addressBook()

    return ab


def loadNB():
    if not nb.load_notesBook():
        notesB = nb.NotesBook()
    else:
        notesB = nb.load_notesBook()
    return notesB


def phone_add(*args, **kwargs):
    mode = kwargs['MODE']
    record = kwargs['RECORD']
    cur_id = kwargs['ID']
    if mode == '1' and record:
        phone = input_phone()
        record.add_phone(phone)
        update_ab(CURRENT_RECORD)


def update_ab(*args, **kwargs):
    rec = kwargs['RECORD']
    cur_id = int(kwargs['ID'])
    ab = loadAB()
    ab[cur_id] = rec
    pb.save_addressBook(ab)


def update_nb(record):
    global CURRENT_RECORD, CURRENT_ID
    delete_nb_record(CURRENT_ID)
    noteB = loadNB()
    noteB.add_record(record)
    nb.save_notesBook(noteB)
    CURRENT_ID = None
    CURRENT_RECORD = None
