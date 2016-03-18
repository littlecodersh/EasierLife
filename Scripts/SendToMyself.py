#coding=utf8
import os, sys, platform
import requests, time, re, subprocess
import json, xml.dom.minidom

BASE_URL = 'https://login.weixin.qq.com'
OS = platform.system()
INTERACT_URL = None

session = requests.Session()
uuid = None
baseRequest = {}

def get_QRuuid():
    url = '%s/jslogin'%BASE_URL
    params = {
        'appid': 'wx782c26e4c19acffb',
        'fun': 'new',
    }
    r = session.get(url, params = params)

    regx = r'window.QRLogin.code = (\d+); window.QRLogin.uuid = "(\S+?)";'
    data = re.search(regx, r.text)
    if data and data.group(1) == '200': return data.group(2)

def get_QR():
    url = '%s/qrcode/%s'%(BASE_URL, uuid)
    r = session.get(url, stream = True)
    with open('QR.jpg', 'wb') as f: f.write(r.content)
    if OS == 'Darwin':
        subprocess.call(['open', 'QR.jpg'])
    elif OS == 'Linux':
        subprocess.call(['xdg-open', 'QR.jpg'])
    else:
        os.startfile('QR.jpg')

def check_login(uuid):
    url = '%s/cgi-bin/mmwebwx-bin/login'%BASE_URL
    payloads = 'tip=1&uuid=%s&_=%s'%(uuid, int(time.time()))
    r = session.get(url, params = payloads)

    regx = r'window.code=(\d+)'
    data = re.search(regx, r.text)
    if not data: return False

    def one_line_print(msg):
        sys.stdout.write('%s\r'%msg)
        sys.stdout.flush()
    if data.group(1) == '200':
        regx = r'window.redirect_uri="(\S+)";'
        global INTERACT_URL
        INTERACT_URL = re.search(regx, r.text).group(1)
        r = session.get(INTERACT_URL, allow_redirects=False)
        INTERACT_URL = INTERACT_URL[:INTERACT_URL.rfind('/')]
        get_login_info(r.text)
        return True
    elif data.group(1) == '201':
        one_line_print('Please press confirm')
    elif data.group(1) == '408':
        one_line_print('Please reload QR Code')
    return False

def get_login_info(s):
    global baseRequest
    for node in xml.dom.minidom.parseString(s).documentElement.childNodes:
        if node.nodeName == 'skey':
            baseRequest['Skey'] = node.childNodes[0].data.encode('utf8')
        elif node.nodeName == 'wxsid':
            baseRequest['Sid'] = node.childNodes[0].data.encode('utf8')
        elif node.nodeName == 'wxuin':
            baseRequest['Uin'] = node.childNodes[0].data.encode('utf8')
        elif node.nodeName == 'pass_ticket':
            baseRequest['DeviceID'] = node.childNodes[0].data.encode('utf8')

def web_init():
    url = '%s/webwxinit?r=%s' % (INTERACT_URL, int(time.time()))
    payloads = {
        'BaseRequest': baseRequest,
    }
    headers = { 'ContentType': 'application/json; charset=UTF-8' }
    r = session.post(url, data = json.dumps(payloads), headers = headers)
    dic = json.loads(r.content.decode('utf-8', 'replace'))
    return dic['User']['UserName']

def send_msg(toUserName = None, msg = 'Test Message'):
    url = '%s/webwxsendmsg'%INTERACT_URL
    payloads = {
            'BaseRequest': baseRequest,
            'Msg': {
                'Type': 1,
                'Content': msg.encode('utf8') if isinstance(msg, unicode) else msg,
                'FromUserName': myUserName.encode('utf8'),
                'ToUserName': (toUserName if toUserName else myUserName).encode('utf8'),
                'LocalID': int(time.time()),
                'ClientMsgId': int(time.time()),
                },
            }
    headers = { 'ContentType': 'application/json; charset=UTF-8' }
    session.post(url, data = json.dumps(payloads, ensure_ascii = False), headers = headers)

if __name__ == '__main__':
    while uuid is None: uuid = get_QRuuid()
    get_QR()
    print 'QR is shown'
    while not check_login(uuid): pass
    myUserName = web_init()
    print 'Login successfully you can send messages now, input q to exit'
    msg = None
    while msg != 'q':
        if msg: send_msg(myUserName, msg)
        msg = raw_input('>').decode(sys.stdin.encoding)
    print 'Have fun:)'
