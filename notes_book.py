from collections import UserDict
import pickle
import re

class Field():
    def __init__(self, value):
        self.__value = None
        self.value = value


class Note(Field):

    @property
    def note(self):
        return self.__note 
    
    @note.setter
    def note(self, value):
        if re.match(r'[\w{5}]', value) and len(value) < 30:
            self.__note = value
        elif re.match(r'[\w{5}]', value) and len(value) > 30:
            print('Note is more lenght')
        elif len(value) < 4:
            print('Note is too short')
        else:
            print(f'Note is not text')


class Teg(Field):

    @property
    def teg(self):
        return self.__teg

    @teg.setter
    def teg(self, value):
        if re.match(r'\w{5}'):
            self.__teg = value
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

    def add_record(self, obj):
        if isinstance(obj, NoteRecord):
            self.data[len(self.data)] = obj.noterecors



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








