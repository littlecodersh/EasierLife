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
# noteDictFormat: {
# 'notebookName':[('note1', timeStamp), ..],
# }

class Storage():
    storage = {}
    def __init__(self):
        self.available = False
    def update(self, token, noteStore):
        for nb in noteStore.listNotebooks():
            self.storage[nb.name] = {}
            self.storage[nb.name]['notebook'] = nb
            self.storage[nb.name]['notes'] = {}
            f = NoteStore.NoteFilter()
            f.notebookGuid = nb.guid
            for ns in noteStore.findNotes(token, f, 0, 999).notes:
                self.storage[nb.name]['notes'][ns.title] = ns
        self.defaultNotebook = noteStore.getDefaultNotebook(token).name
    def create_note(self, note, notebookName = None):
        if notebookName is None: notebookName = self.defaultNotebook
        self.storage[notebookName]['notes'][note.title] = note
        return True
    def create_notebook(self, notebook):
        if self.storage.get(notebook.name) is None: return False
        self.storage[notebook.name] = {}
        self.storage[notebook.name]['notebook'] = notebook
        self.storage[notebook.name]['notes'] = {}
        return True
    def copy_note(self, fullNotePath, _to = None):
        if _to is None: _to = self.defaultNotebook
        note = self.get(fullNotePath)
        if note is None: return False
        self.storage[_to]['notes'][note.title] = note
        return True
    def move_note(self, fullNotePath, _to = None):
        r = self.copy_note(fullNotePath, _to)
        if r == False: return False
        del self.storage[fullNotePath.split('/')[0]]['notes'][note.title]
        return True
    def delete_note(self, fullNotePath):
        if self.get(fullNotePath) is None: return False
        del self.storage[fullNotePath.split('/')[0]]['notes'][fullNotePath.split('/')[1]]
        return True
    def delete_notebook(self, notebook):
        if self.get(notebook) is None: return False
        del self.storage[notebook]
        return True
    def get(self, s):
        f = s.split('/')
        r = self.storage.get(f[0])
        if r is None: return
        if '/' in s: return r['notes'].get(f[1])
        return r.get('notebook')
    def get_note_dict(self):
        noteDict = {}
        for nbName, nb in self.storage.iteritems():
            noteDict[nbName] = []
            for nName, n in nb['notes'].iteritems():
                noteDict[nbName].append((nName, n.updated / 1000))
        return noteDict
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
