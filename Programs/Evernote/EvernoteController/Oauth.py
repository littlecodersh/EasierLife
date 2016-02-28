#coding=utf8
import requests
from urllib import unquote
import json, sys, time
import getpass

DEBUG = True
class Oauth():
    config = {
            True:{
                'key': '',
                'secret': '',
                'url': 'sandbox.evernote.com'
                },
            False:{
                'key': '',
                'secret': '',
                'url': 'app.yinxiang.com'
                }
            }
    def __init__(self,debug):
        self.debug = debug
        self.consumerKey = self.config[self.debug]['key']
        self.consumerSecret = self.config[self.debug]['secret']
        self.evernoteUrl = self.config[self.debug]['url']
    def oauth(self):
        try:
            data = json.loads(open('config.json','r').read())
            if int(data['edam_expires']) <= time.time()*1000+10000 or self.debug != data['DEBUG']: raise Exception
            return data['oauth_token']
        except:
            pass
        self.__get_tmp_token()
        self.__get_ver()
        return self.__get_token()
    def __get_tmp_token(self):
        payload = {
            'oauth_callback': '127.0.0.1',
            'oauth_consumer_key': self.consumerKey,
            'oauth_signature': self.consumerSecret,
            'oauth_signature_method': 'PLAINTEXT',
        }
        r = requests.get('https://%s/oauth'%self.evernoteUrl, params = payload)

        if not 'oauth_token' in r.text: raise Exception('oauth_token not found')
        self.tmpOauthToken = dict(item.split('=',1) for item in unquote(r.text).split('&'))['oauth_token'],
        line_write('Got tmp_oauth_token')
    def __get_login_info(self):
        line_write(' '*30)
        account = raw_input('Username: ')
        password = getpass.getpass('Password: ')
        return account,password
    def __get_ver(self):
        while True:
            account, password = self.__get_login_info()
            access = {
                'authorize': 'Authorize',
                'oauth_token': self.tmpOauthToken,
                'username': account,
                'password': password,
            }
            r = requests.post('https://%s/OAuth.action'%self.evernoteUrl, data = access)
            if 'oauth_verifier' in r.url: break
            print 'login failed'

        self.verifier = dict(item.split('=', 1) for item in r.url.split('?')[-1].split('&'))['oauth_verifier']
        line_write('Got oauth_verifier')
    def __get_token(self):
        payload = {
            'oauth_consumer_key': self.consumerKey,
            'oauth_token': self.tmpOauthToken,
            'oauth_verifier': self.verifier,
            'oauth_signature': self.consumerSecret,
            'oauth_signature_method': 'PLAINTEXT',
        }
        r = requests.get('https://%s/oauth'%self.evernoteUrl, params = payload)

        if not ('oauth_token' in r.text and 'edam_expires' in r.text): raise Exception('Token Not Found')
        with open('config.json','w') as f:
            f.write(json.dumps({
                'oauth_token': dict(item.split('=',1) for item in unquote(r.text).split('&'))['oauth_token'],
                'edam_expires': dict(item.split('=',1) for item in unquote(r.text).split('&'))['edam_expires'],
                'DEBUG': self.debug
                }))
        line_write('Got oauth_token')
        return dict(item.split('=',1) for item in unquote(r.text).split('&'))['oauth_token']

def line_write(s):
    sys.stdout.write((s+'\r').decode('UTF-8').encode(sys.getfilesystemencoding()))
    sys.stdout.flush()

if __name__=='__main__':
    print Oauth().oauth()
