#coding=utf8
import sys, hashlib, re, time
import evernote.edam.type.ttypes as Types
import evernote.edam.notestore.NoteStore as NoteStore
from evernote.api.client import EvernoteClient

from storage import Storage

class EvernoteController(object):
    def __init__(self, token, isSpecialToken = False, sandbox = False, isInternational = False):
        self.token = token
        if sandbox:
            self.client = EvernoteClient(token=self.token)
        elif isInternational:
            self.client = EvernoteClient(token=self.token, service_host='app.evernote.com')
        else:
            self.client = EvernoteClient(token=self.token, service_host='app.yinxiang.com')
        self.isSpecialToken = isSpecialToken
        self.userStore = self.client.get_user_store()
        self.noteStore = self.client.get_note_store()
        self.storage = Storage(self.token, self.noteStore)
    def create_notebook(self, title):
        if self.get(title): return False
        notebook = Types.Notebook()
        notebook.name = title
        notebook = self.noteStore.createNotebook(notebook)
        self.storage.create_notebook(notebook)
        return True
    def create_note(self, title, notebook = None, content = None, fileDir = None):
        if self.get('%s/%s'%(notebook or self.storage.defaultNotebook, title)): return False
        note = Types.Note()
        note.title = title
        note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
        note.content += '<en-note>'
        note.content += content or ''
        if notebook: note.notebookGuid = self.get(notebook).guid
        if not fileDir is None:
            with open(fileDir, 'rb') as f: fileBytes = f.read()
            fileData = Types.Data()
            fileData.bodyHash = self._md5(fileBytes)
            fileData.size = len(fileBytes)
            fileData.body = fileBytes
            fileAttr = Types.ResourceAttributes()
            fileAttr.fileName = title + '.md'
            fileAttr.attachment = True
            fileResource = Types.Resource()
            fileResource.data = fileData
            fileResource.mime = 'application/octet-stream'
            fileResource.attributes = fileAttr
            note.resources = [fileResource]
            note.content += '<en-media type="application/octet-stream" hash="%s"/>'%fileData.bodyHash
        note.content += '</en-note>'
        note = self.noteStore.createNote(note)
        self.storage.create_note(note, notebook)
        return True
    def update_note(self, title, notebook = None, content = None, fileDir = None):
        note = self.get('%s/%s'%(notebook or self.storage.defaultNotebook, title))
        if note is None: return self.create_note(title, notebook, content or '', fileDir)
        try:
            header, oldContent = re.compile('(.*?)<en-note>(.*?)</en-note>').findall(note.content)[0]
        except:
            header = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
            oldContent = ''
        guid = note.guid
        oldContent = re.sub('<en-media.*?/>', '', oldContent)
        note = Types.Note()
        note.guid = guid
        note.title = title
        note.content = header
        note.content += '<en-note>'
        note.content += content or oldContent
        if not fileDir is None:
            with open(fileDir, 'rb') as f: fileBytes = f.read()
            fileData = Types.Data()
            fileData.bodyHash = self._md5(fileBytes)
            fileData.size = len(fileBytes)
            fileData.body = fileBytes
            fileAttr = Types.ResourceAttributes()
            fileAttr.fileName = title + '.md'
            fileAttr.attachment = True
            fileResource = Types.Resource()
            fileResource.data = fileData
            fileResource.mime = 'application/octet-stream'
            fileResource.attributes = fileAttr
            note.resources = [fileResource]
            note.content += '<en-media type="application/octet-stream" hash="%s"/>'%fileData.bodyHash
        note.content += '</en-note>'
        self.noteStore.updateNote(self.token, note)
        self.storage.delete_note('%s/%s'%(notebook or self.storage.defaultNotebook, title))
        self.storage.create_note(note, notebook)
        return True
    def get_attachment(self, note):
        note = self.get(note)
        return (self.noteStore.getResourceData(resource.guid) for resource in note.resources)
    def move_note(self, note, _to):
        if self.get(note) is None: return False
        if type(self.get(note)) != type(Types.Note()) or type(self.get(_to)) != type(Types.Notebook()): raise Exception('Type Error')
        self.noteStore.copyNote(self.token, self.get(note).guid, self.get(_to).guid)
        if self.isSpecialToken:
            self.noteStore.expungeNote(self.token, self.get(note).guid)
        else:
            self.noteStore.deleteNote(self.token, self.get(note).guid)
        self.storage.move_note(note, _to)
        return True
    def delete_note(self, note):
        if self.get(note): return False
        if type(self.get(note)) != type(Types.Note()): raise Exception('Types Error')
        if self.isSpecialToken:
            self.noteStore.expungeNote(self.token, self.get(note).guid)
        else:
            self.noteStore.deleteNote(self.token, self.get(note).guid)
        self.storage.delete_note(note)
        return True
    def delete_notebook(self, notebook):
        if self.get(notebook) or not self.isSpecialToken: return False
        if type(self.get(notebook)) != type(Types.Notebook()): raise Exception('Types Error')
        self.noteStore.expungeNotebook(self.token, self.get(notebook).guid)
        self.storage.delete_note(note)
        return True
    def get(self, s):
        return self.storage.get(s)
    def show_notebook(self):
        self.storage.show_notebook()
    def show_notes(self, notebook=None):
        self.storage.show_notes(notebook)
    def _md5(self, s):
        m = hashlib.md5()
        m.update(s)
        return m.hexdigest()

if __name__ == '__main__':
    # You can get this from 'https://%s/api/DeveloperToken.action'%SERVICE_HOST >>
    # In China it's https://app.yinxiang.com/api/DeveloperToken.action <<
    token = DEV_TOKEN
    e = EvernoteController(token, True, True)
    e.update_note('Hello', 'Test', 'Changed', 'README.md')

if False:
    e.create_notebook('Notebook1')
    e.create_note('Hello', '<en-note>Hello, world!</en-note>', 'Notebook1')
    e.create_notebook('Notebook2')
    e.show_notes()
    e.move_note('Notebook1/Hello', 'Notebook2')
    e.show_notes()
    e.delete_note('Notebook2/Hello')
    # deleting notebook can only be available when you use developer token for you own evernote
    e.delete_notebook('Notebook1')
    e.delete_notebook('Notebook2')
    e.show_notes()
