from EvernoteController import EvernoteController
from Memo import Memo

MEMO_NAME = 'Memo'
MEMO_DIR = 'Memo'
MEMO_STORAGE_DIR = 'S-Memo'

def f(fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
    except:
        pass

m = Memo()
e = EvernoteController()
f(e.create_notebook, MEMO_DIR)
f(e.create_notebook, MEMO_STORAGE_DIR)
f(e.move_note, MEMO_DIR+'/'+MEMO_NAME, MEMO_STORAGE_DIR)
e.create_note('Memo', m.raw_memo(), MEMO_DIR)
