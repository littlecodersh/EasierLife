import re
import xml.dom.minidom

def re_solve(fileDir):
    regex = {
            'info': '={50}\n([\s\S]*?)\n={50}',
            'item': 'item.*?: (.*?)\n',
            'requiredItems': ['Filename', 'From', 'To', 'Subject', 'Created On', 'Inline'],}
    for item in regex['requiredItems']: regex[item] = regex['item'].replace('item', item)
    regex = {key: (re.compile(value) if isinstance(value, basestring) else None) for key, value in regex.items()}

    with open(fileDir) as f: data = f.read().decode('utf-16')
    attaList = re.findall(regex['info'], data)
    infoList = [{key: re.search(value, atta) for key, value in regex.items()} for atta in attaList]
    
    return infoList

def xml_solve(fileDir):
    requiredItems = ['to', 'to_email', 'from', 'from_email', 'filename', 'created_on', 'subject']
    infoList = []
    dom = xml.dom.minidom.parse(fileDir)
    root = dom.documentElement
    for node in root.getElementsByTagName('item'):
        if node.getElementsByTagName('inline')[0].firstChild.data != 'Yes':
            info = {key: node.getElementsByTagName(key)[0].firstChild.data
                    if node.getElementsByTagName(key)[0].firstChild else '' for key in requiredItems}
            infoList.append(info)
    requiredItems[1] = requiredItems[1].lower()
    requiredItems[3] = requiredItems[3].lower()
    return infoList

if __name__ == '__main__':
    infoList = xml_solve('atta.xml')
    for info in infoList:
        for key, value in info.items():
            print '%s: %s'%(key, value)
        print
