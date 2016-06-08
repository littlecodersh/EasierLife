import requests

proxies = {
    "http": "http://127.0.0.1:1080",
    "https": "https://127.0.0.1:1080", }   
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:5.0) Gecko/20100101 Firefox/5.0', }
url = 'http://translate.google.cn/translate_a/t'

class TranslateClient(object):
    def __init__(self):
        self.params = {
            'client': 'p',
            'ie': 'UTF-8',
            'oe': 'UTF-8',
            'tl': None,
            'sl': None,
            'text': None, }
    def get(self, text, tl = 'zh-CN', sl = 'auto'):
        self.params['text'] = text
        self.params['tl'] = tl
        self.params['sl'] = sl
        return requests.post(url, self.params, headers = headers, proxies = proxies).json()[0]

if __name__ == '__main__':
    tc = TranslateClient()
    print(tc.get('test'))
