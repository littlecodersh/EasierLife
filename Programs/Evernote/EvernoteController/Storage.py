#coding=utf8
import sys
import evernote.edam.type.ttypes as Types
import evernote.edam.notestore.NoteStore as NoteStore

# Data Structure
# notebookName:{
#     'notebook': notebook
#     'notes': {
#         noteName: note
#         ...
#     }
# }

class Storage():
    storage = {}
    def __init__(self, noteStore, token):
        for nb in noteStore.listNotebooks():
            self.storage[nb.name] = {}
            self.storage[nb.name]['notebook'] = nb
            self.storage[nb.name]['notes'] = {}
            f = NoteStore.NoteFilter()
            f.notebookGuid = nb.guid
            for ns in noteStore.findNotes(token, f, 0, 999).notes:
                self.storage[nb.name]['notes'][ns.title] = ns
        self.defaultNotebook = noteStore.getDefaultNotebook(token).name
    def create_note(self, note, notebookName):
        if not notebookName: notebookName = self.defaultNotebook
        self.storage[notebookName]['notes'][note.title] = note
    def create_notebook(self, notebook):
        if self.storage.has_key(notebook.name): return
        self.storage[notebook.name] = {}
        self.storage[notebook.name]['notebook'] = notebook
        self.storage[notebook.name]['notes'] = {}
    def move_note(self, fullNoteName, _to):
        note = self.myfile(fullNoteName)
        self.storage[_to]['notes'][note.title] = note
        del self.storage[fullNoteName.split('/')[0]]['notes'][note.title]
    def delete_note(self, fullNoteName):
        del self.storage[fullNoteName.split('/')[0]]['notes'][fullNoteName.split('/')[1]]
    def delete_notebook(self, notebook):
        del self.storage[notebook]
    def myfile(self, s):
        f = s.split('/')
        if '/' in s:
            return self.storage[f[0]]['notes'][f[1]]
        else:
            return self.storage[f[0]]['notebook']
    def show_notebook(self):
            for bn, nb in self.storage.items(): print_line(bn)
    def show_notes(self, notebook = None):
        for bn, nb in self.storage.items():
            if not notebook: print_line(bn + ':')
            if not notebook or bn == notebook:
                for nn, ns in nb['notes'].items():
                    print_line(('' if notebook else '    ')+nn)
def print_line(s):
    t = sys.getfilesystemencoding()
    print s.decode('UTF-8').encode(t)
