from collections import UserDict
import pickle
import re


class Field():
    pass


class Note(Field):

    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):

        if not re.match(r'[A-Za-zА-Яа-я]\w', new_value) or len(new_value) <= 2:
            raise ValueError('Note is not text')
       # elif re.match(r'[A-Za-zА-Яа-я]\w', value) and len(value) > 30:
          #  print('Note is more lenght')
    #    elif re.match(r'[A-Za-zА-Яа-я]\w', value) and len(value) <= 2:
            #print('Note is too short')
        else:
            self.__value = new_value


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
            if not re.match(r'[A-Za-zА-Яа-я]\w', value) or 10 <= len(value) < 3:
                raise ValueError('Teg must be 3 symbols min')

            else:
                self.__value = value


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
            result += f'id  {key} | note - {data["Note"]} | tegs - {data["Teg"]}\n'
        return result

    def __getitem__(self, key):
        rec = self.data[key]
        return f'id - {key} | Note: {rec["Note"]} | Teg: {rec["Teg"]}'

    def add_record(self, obj):
        if isinstance(obj, NoteRecord):
            self.data[len(self.data)] = obj.noterecors
            return self.data

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

    def delete_record(self, index):
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
        if len(line) < 3:
            raise ValueError(f'Parameter must be 3 or more symbol')

        self.value = str.lower(line)
        self.dict_key = {}
        self.dict_value = {}
        result = []
        for key, value in self.data.items():
            if str(key).find(self.value) >= 0:
                self.dict_key[key] = self.data[key]
            if value['Note'].find(self.value) >= 0:
                self.dict_value[key] = value
            if value['Teg'].lower().find(self.value) >= 0:
                self.dict_value[key] = value

        if len(self.dict_key) > 0 and len(self.dict_value) > 0:
            for key, data in self.dict_key.items():
                result.append(self[key])
            for key, data in self.dict_value.items():
                result.append(self[key])
            return result

        elif len(self.dict_key) > 0 and len(self.dict_value) == 0:
            for key, data in self.dict_key.items():
                result.append(self[key])
            return result
        elif len(self.dict_key) == 0 and len(self.dict_value) > 0:
            for key, data in self.dict_value.items():
                result.append(self[key])
            return result


# edit, del TEG


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
    pass
