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
    def value(self, value):
        
        if re.match(r'[A-Za-zА-Яа-я]\w', value) and 3 < len(value) < 30:
            self.__value = new_value
        elif re.match(r'[A-Za-zА-Яа-я]\w', value) and len(value) > 30:
            print('Note is more lenght')
        elif re.match(r'[A-Za-zА-Яа-я]\w', value) and len(value) < 3:
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
            if re.match(r'[A-Za-zА-Яа-я]\w', value) and 3 < len(value) < 10:
                self.__value = value
            elif re.match(r'[A-Za-zА-Яа-я]\w', value) and len(value) < 3:
                print('Teg must be 3 symbols min')
            else:
                print(f'Teg is not text')


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
        self.value = str.lower(line)
        self.dict_key = {}
        self.dict_value = {}
        result = ''
        for key, value in self.data.items():
            if str(key).find(self.value) >= 0:
                self.dict_key[key] = self.data[key]
            if value['Note'].lower().find(self.value) >= 0:
                self.dict_value[key] = value
            if value['Teg'].lower().find(self.value) >= 0:
                self.dict_value[key] = value
          
        if len(self.dict_key) > 0 and len(self.dict_value) > 0:
            for key, data in self.dict_key.items():
                result += f'id  {key} | note - {data["Note"]} | tegs - {data["Teg"]}\n'
            for key, data in self.dict_value.items():
                result += f'id  {key} | note - {data["Note"]} | tegs - {data["Teg"]}\n'
            return result
            
        elif len(self.dict_key) > 0 and len(self.dict_value) == 0:
            for key, data in self.dict_key.items():
                result += f'id  {key} | note - {data["Note"]} | tegs - {data["Teg"]}\n'
            return result
        elif len(self.dict_key) == 0 and len(self.dict_value) > 0:
            for key, data in self.dict_value.items():
                result += f'id  {key} | note - {data["Note"]} | tegs - {data["Teg"]}\n'
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

    while True:
        af = Note(input('Enter the note: '))

        if af.value != None:
            break

    while True:
        t = Teg(input('Enter the teg: '))
        if t.value != '':
            break