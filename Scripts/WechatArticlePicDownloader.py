#coding=utf8
import requests, re, os
from Tkinter import Tk, Button, Entry
import tkMessageBox

def download_pic_from_url(url, picDir):
    content = requests.get(url).content
    postfix = re.compile('wx_fmt=([a-z]+)').search(url).groups()[0]
    with open((picDir+'.'+postfix).encode('cp936'), 'wb') as f: f.write(content)

def get_pic_url_from_url(url):
    html = requests.get(url).content
    return re.compile('<img .*? data-src="(.*?)" .*?>').findall(html)

def get_title_cover_from_url(url):
    content = requests.get(url).content
    regexDict = {
        'title': 'var msg_title = "(.*?)";',
        'pic_url': 'var msg_cdn_url = "(.*?)";', }
    try:
        for k, r in regexDict.items():
            regexDict[k] = re.compile(r).search(content).groups()[0]
    except:
        return '', ''
    return regexDict['title'].decode('utf8'), regexDict['pic_url']

def button_clicked():
    url = inputEntry.get().strip()
    if not 'http' in url:
        tkMessageBox.showinfo('Warning', u'把http或者https也加进去吧')
        return
    try:
        title, picUrl = get_title_cover_from_url(url)
    except:
        tkMessageBox.showinfo('Warning', u'网址读取错误，请尝试使用浏览器读取网址判断是否可以打开')
        return
    if not title:
        tkMessageBox.showinfo('Warning', u'检测到非微信文章页面')
        return
    for sk in (r'\/:*?"<>|'): title = title.replace(sk, '')
    if not os.path.exists(title.encode('cp936')): os.mkdir(title.encode('cp936'))
    download_pic_from_url(picUrl, os.path.join(title, u'标题图'))
    for i, picUrl in enumerate(get_pic_url_from_url(url), 1):
        download_pic_from_url(picUrl, os.path.join(title, str(i)))
    tkMessageBox.showinfo('Info', u'读取成功，请打开"%s"文件夹查看'%title)

mainWindow = Tk()
button = Button(mainWindow, cnf = {'command': button_clicked, 'text': 'Download', 'justify': 'right', })
inputEntry = Entry(mainWindow, width=70)
inputEntry.pack()
button.pack()
mainWindow.title(u'微信图片下载器')
mainWindow.mainloop()
