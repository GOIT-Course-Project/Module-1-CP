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
        if re.match(r'[A-Za-zА-Яа-я]\w{2}', value) and len(value) < 30:
            self.__value = value
        elif re.match(r'[A-Za-zА-Яа-я]\w{2}', value) and len(value) > 30:
            print('Note is more lenght')
        elif len(value) < 4:
            print('Note is too short')
        else:
            print(f'Note is not text')


class Teg(Field):

    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not value:
            self.__value = value
        if re.match(r'[A-Za-zА-Яа-я]\w{2}', value) and len(value) >= 3:
            self.__value = value
        else:
            print(f'Teg is too long')

class NoteRecord():
    def __init__(self, *args):
        self.noterecors = {}
        self.noterecors['Note'] = None
        self.noterecors['Teg'] = None

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

    def add_record(self, obj):
        if isinstance(obj, NoteRecord):
            self.data[len(self.data)] = obj.noterecors
            return self.data

 # edit and del NOTE
    def edit_note(self, index, new_obj):
        self._count = 0
        if len(self.data) > index:
            if isinstance(new_obj, Note):
                for i in self.data.values():
                    if self._count == index:
                        i['Note'] = new_obj.value
                    self._count +=1
            return self.data
        else:
            return 'Note index is not exist'

    def del_note(self, index):
        if len(self.data) > index:
            del self.data[index]
            return self.data
        else:
            return 'Note index is not exist'

# edit and del TEG
    def edit_teg(self, index, new_obj):
        self._count = 0
        if len(self.data) > index:
            if isinstance(new_obj, Teg):
                for i in self.data.values():
                    if self._count == index:
                        i['Teg'] = new_obj.value
                    self._count +=1
            return self.data
        else:
            return 'Teg index is not exist' 

    def del_teg(self, index):
        if len(self.data) > index:
            self.data[index]['Teg'] = None
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
    










