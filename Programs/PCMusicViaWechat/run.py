#coding=utf8
import itchat
from Lib.InteractMusicApi import interact_select_song, close_music

HELP_MSG = '''\
欢迎使用微信网易云音乐
帮助： 显示帮助
关闭： 关闭歌曲
歌名： 按照引导播放音乐\
'''

@itchat.msg_register('Text')
def music_player(msg):
    if msg['ToUserName'] != 'filehelper': return
    if msg['Text'] == u'关闭':
        close_music()
        return '音乐已关闭'
    if msg['Text'] == u'帮助':
        return HELP_MSG
    else:
        return interact_select_song(msg['Text'])

itchat.auto_login(True, enableCmdQR = True)
itchat.send(HELP_MSG) 
itchat.run()
