#coding=utf8
import psutil, _winreg, os

SHADOWSOCKS_PATH = r'"Shadowsocks.lnk"'
PROXY_PORT = '127.0.0.1:8080'

def manage_shadowsocks(flag='kill'): # kill/create
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name'])
        except psutil.NoSuchProcess:
            pass
        else:
            if pinfo['name']=='Shadowsocks.exe':
                if flag == 'kill': proc.terminate()
                return
    if flag == 'create': os.startfile(SHADOWSOCKS_PATH)

def get_process(keyList):
    try:
        i = 0
        while True:
            name, value, type = _winreg.EnumValue(key,i)
            keyList[str(name)] = value
            i+=1
    except WindowsError:
        pass
    return keyList

def set_proxy(keyList):
    if keyList.has_key('AutoConfigURL'): _winreg.DeleteValue(key, 'AutoConfigURL')
    if keyList['ProxyEnable'] != 1: _winreg.SetValueEx(key, 'ProxyEnable', 0, _winreg.REG_DWORD, 1)
    if not keyList.has_key('ProxyServer'): 
        _winreg.CreateKey(key, 'ProxyServer')
        _winreg.SetValueEx(key, 'ProxyServer', 0, _winreg.REG_SZ, PROXY_PORT)
    elif keyList['ProxyServer'] != PROXY_PORT: 
        _winreg.SetValueEx(key, 'ProxyServer', 0, _winreg.REG_SZ, PROXY_PORT)


if __name__ == '__main__':
    key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Internet Settings", 0, _winreg.KEY_ALL_ACCESS)
    keyList = get_process({})
    if not keyList.has_key('AutoConfigURL') and keyList['ProxyEnable'] == 1 and keyList.has_key('ProxyServer') and keyList['ProxyServer'] == PROXY_PORT: # determine whether proxy is well set
        # if it's well set, close the proxy and clear the proxy setting
        manage_shadowsocks('create') # shadowsocks will automatically change regs
        print 'Ports Closed and Shadowsocks Started'
    else:
        # if it's not well set, get it done properly
        manage_shadowsocks('kill')
        set_proxy(keyList)
        print 'Shadowsocks Closed and Ports Set to '+PROXY_PORT
