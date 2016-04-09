#coding=utf8
import os, sys
from NetEaseMusicApi import api

__all__ = ['interact_select_song', 'close_music']

DEFAULT_FOLDER = 'storage'
DEFAULT_LIMIT = 10
SINGLE_DETAIL_LENGTH = 10

def _search_song_id_by_name(number = DEFAULT_LIMIT, singleDetailLength = SINGLE_DETAIL_LENGTH):
    def _get_detail(item, detailList):
        valueList = []
        for detail in detailList:
            value = item
            for key in detail.split('/'):
                try:
                    try:
                        key = int(key)
                    except:
                        pass
                    value = value[key]
                except:
                    value = '';break
            valueList.append(value[:singleDetailLength])
        return '-'.join(valueList)
    while 1:
        songName = yield
        itemList = api.search.songs(songName, number)
        if itemList is None:
            yield; continue
        else:
            candidatesList = []
            for i, item in enumerate(itemList):
                candidatesList.append(('%-' + str(len(itemList)/10 + 4) + 's%s')%(
                    '[%s]'%(i+1), _get_detail(item, ['name', 'artists/0/name', 'album/name'])))
            yield '\n'.join(candidatesList)
        selectIndex = yield
        try:
            selectIndex = int(selectIndex) - 1
            if selectIndex < 0 or len(itemList) < selectIndex: raise Exception
        except:
            yield; continue
        yield itemList[selectIndex]['id']

ssibn = _search_song_id_by_name()
ssibn.next()

def search_song_id_by_name(msgInput):
    r = ssibn.send(msgInput)
    ssibn.next()
    return r

def _interact_select_song(folder = 'storage'):
    if not os.path.exists(folder): os.mkdir(folder)
    while 1:
        songName = yield
        songCandidates = search_song_id_by_name(songName)
        if songCandidates:
            yield songCandidates
        else:
            yield u'没有找到%s。'%songName
            continue
        selectIndex = yield
        songId = search_song_id_by_name(selectIndex)
        if songId:
            song = api.song.detail(songId)[0]
            songDir = os.path.join(folder, song['name'] + '.mp3')
            with open(songDir, 'wb') as f:
                f.write(api.download(song['bMusic']['dfsId']))
            os.startfile(songDir)
            yield u'%s 正在播放'%songName
        else:
            yield u'无效选项，请重新搜索'

iss = _interact_select_song()
iss.next()

def interact_select_song(msgInput):
    r = iss.send(msgInput)
    iss.next()
    return r

with open(os.path.join(DEFAULT_FOLDER, 'stop.mp3'), 'w') as f: pass

def close_music():
    os.startfile(os.path.join(DEFAULT_FOLDER, 'stop.mp3'))


if __name__ == '__main__':
    while 1:
        msg = raw_input('>').decode(sys.stdin.encoding)
        print interact_select_song(msg)
