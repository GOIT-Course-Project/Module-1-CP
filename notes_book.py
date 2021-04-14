from collections import UserDict
import pickle
import re


class Field():
    def __init__(self, value):
        self.__value = None
        self.value = value


class Note(Field):

    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if re.match(r'\w', value) and len(value) < 50:
            self.__value = value
        elif re.match(r'\w', value) and len(value) > 50:
            print('Note is more lenght')
        elif len(value) < 4:
            print('Note is too short')
        else:
            print(f'Note is not text')


class Teg(Field):

    def __init__(self, value):
        self.__value = ''
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not value:
            self.__value = value
        else:
            if re.match(r'[A-Za-zА-Яа-я]\w{2}', value) and len(value) >= 3:
                self.__value = value
            else:
                print(f'Teg is too long')


class NoteRecord():
    def __init__(self, *args):
        self.noterecors = {}
        self.noterecors['Note'] = None
        self.noterecors['Teg'] = ''

        for arg in args:
            if isinstance(arg, Note):
                self.noterecors['Note'] = arg.value
            elif isinstance(arg, Teg):
                self.noterecors['Teg'] = arg.value

    def __str__(self):
        return f'Note: {self.noterecors["Note"][:5]}... | Teg: {self.noterecors["Teg"]}'

    def edit_note(self, obj):
        if isinstance(obj, Note):
            self.noterecors['Note'] = obj.value

    def edit_teg(self, obj):
        if isinstance(obj, Teg):
            self.noterecors['Teg'] = obj.value

    def del_note(self, obj):
        if isinstance(obj, Note):
            self.noterecors['Note'].remove(obj.value)


class NotesBook(UserDict):

    def __init__(self):
        super(NotesBook, self).__init__()
        self._count = 0

    def __str__(self):
        result = ''
        for key, data in self.data.items():
            result += f'id  {key} | note - {data["Note"]} | teg - {data["Teg"]}\n'
        return result

    def __getitem__(self, key):
        rec = self.data[key]
        return f'id - {key} | Note: {rec["Note"]} | Teg: {rec["Teg"]}'

    def add_record(self, obj):
        if isinstance(obj, NoteRecord):
            self.data[len(self.data)] = obj.noterecors
            return self.data

    def delete_record(self, key):
        if key in self.data:
            self.data.pop(key)
            new_ab = UserDict()
            i = 0
            for v in self.data.values():
                new_ab[i] = v
                i += 1
            self.data = new_ab
        else:
            return(f'{key} is not exist in NoteBook.')

 # edit, del and find NOTE
    def edit_note(self, index, new_obj):
        self._count = 0
        if len(self.data) > index:
            if isinstance(new_obj, Note):
                for i in self.data.values():
                    if self._count == index:
                        i['Note'] = new_obj.value
                    self._count += 1
            return self.data
        else:
            return 'Note index is not exist'

    def del_note(self, index):
        if index in self.data.keys():
            self.data.pop(index)
            new_nb = UserDict()
            i = 0
            for v in self.data.values():
                new_nb[i] = v
                i += 1
            self.data = new_nb
            return self.data
        else:
            return(f'{index} is not exist in NoteBook.')

    def find_note(self, line):
        result = []
        for key, value in self.data.items():
            if line in value['Note'].lower():
                result.append(str(self[key]))
        return result
        # self.value = str(line)
        # self.dict_key = {}
        # self.dict_value = {}
        # result_key = None
        # result_value = None
        # for key, value in self.data.items():
        #     if line.isdigit():
        #         if str(key).find(self.value) >= 0:
        #             self.dict_key[key] = self.data[key]
        #     if line.isalpha():
        #         if len(self.value) >= 3:
        #             if value['Note'].find(self.value) >= 0:
        #                 self.dict_value[key] = value
        #         else:
        #             return(f'{line} is too short')

        # if len(self.dict_key) > 0 and len(self.dict_value) > 0:
        #     return self.dict_key, self.dict_value
        # elif len(self.dict_key) > 0 and len(self.dict_value) == 0:
        #     return self.dict_key
        # elif len(self.dict_key) == 0 and len(self.dict_value) > 0:
        #     return self.dict_value


# edit, del and find TEG


    def edit_teg(self, index, new_obj):
        self._count = 0
        if len(self.data) > index:
            if isinstance(new_obj, Teg):
                for i in self.data.values():
                    if self._count == index:
                        i['Teg'] = new_obj.value
                    self._count += 1
            return self.data
        else:
            return 'Teg index is not exist'

    def del_teg(self, index):
        if len(self.data) > index:
            self.data[index]['Teg'] = ''
            return self.data
        else:
            return 'Teg index is not exist'

    def find_teg(self, line):
        self.value = str(line)
        self.dict_key = {}
        self.dict_value = {}

        for key, value in self.data.items():
            if line.isdigit():
                if str(key).find(self.value) >= 0:
                    self.dict_key[key] = self.data[key]
            if line.isalpha():
                if len(self.value) >= 3:
                    if value['Teg'].find(self.value) >= 0:
                        self.dict_value[key] = value
                else:
                    return(f'{line} is too short')

        if len(self.dict_key) > 0 and len(self.dict_value) > 0:
            return self.dict_key, self.dict_value
        elif len(self.dict_key) > 0 and len(self.dict_value) == 0:
            return self.dict_key
        elif len(self.dict_key) == 0 and len(self.dict_value) > 0:
            return self.dict_value


def save_notesBook(obj):
    with open('notes_book.bin', 'wb') as file:
        pickle.dump(obj, file)


def load_notesBook():
    try:
        file = open('notes_book.bin', 'rb')
    except FileNotFoundError:
        return False
    else:
        with file:
            return pickle.load(file)


if __name__ == '__main__':

    while True:
        af = Note(input('Enter the note: '))

        if af.value != None:
            break

    while True:
        t = Teg(input('Enter the teg: '))
        if t.value != None:
            break

    record = NoteRecord(af, t)
    record1 = NoteRecord(t, Note('Ghjcnj'))
    record2 = NoteRecord(af)
    book = NotesBook()
    print(book.add_record(record))
    print(book.add_record(record1))
    print(book.add_record(record2))

    c = Note(input('Enter the new note:'))
    print(book.edit_note(0, c))
    print(book.del_note(1))
    print(book.add_record(record1))
    print(book.edit_teg(0, Teg('weekf')))
    # print(book.del_teg(0))
    print(book.find_note('0'))
    print(book.find_note('он'))
    print(book.find_teg('week'))
