import requests, getpass

class Oauth(object):
    def __init__(self, consumerKey, consumerSecret, sandbox = True, isInternational = False):
        if sanbox:
            self.host = 'sandbox.evernote.com'
        elif isInternational:
            self.host = 'app.evernote.com'
        else:
            self.host = 'app.yinxiang.com'
        self.host = host
        self.consumerKey = consumerKey
        self.consumerSecret = consumerSecret
    def oauth(self):
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
        r = requests.get('https://%s/oauth'%self.host, params = payload)
        if not 'oauth_token' in r.text: raise Exception('oauth_token not found')
        self.tmpOauthToken = dict(item.split('=',1) for item in unquote(r.text).split('&'))['oauth_token'],
    def __get_login_info(self):
        account = raw_input('Username: ')
        password = getpass.getpass('Password: ')
        return account, password
    def __get_ver(self):
        while 1:
            account, password = self.__get_login_info()
            access = {
                'authorize': 'Authorize',
                'oauth_token': self.tmpOauthToken,
                'username': account,
                'password': password,
            }
            r = requests.post('https://%s/OAuth.action'%self.host, data = access)
            if 'oauth_verifier' in r.url: break
        self.verifier = dict(item.split('=', 1) for item in r.url.split('?')[-1].split('&'))['oauth_verifier']
    def __get_token(self):
        payload = {
            'oauth_consumer_key': self.consumerKey,
            'oauth_token': self.tmpOauthToken,
            'oauth_verifier': self.verifier,
            'oauth_signature': self.consumerSecret,
            'oauth_signature_method': 'PLAINTEXT',
        }
        r = requests.get('https://%s/oauth'%self.host, params = payload)

        if not ('oauth_token' in r.text and 'edam_expires' in r.text): raise Exception('Token Not Found')
        return (dict(item.split('=',1) for item in unquote(r.text).split('&'))['oauth_token'],
            dict(item.split('=',1) for item in unquote(r.text).split('&'))['edam_expires'], self.host)

if __name__=='__main__':
    key = ''
    secret = ''
    print Oauth(key, secret).oauth()
