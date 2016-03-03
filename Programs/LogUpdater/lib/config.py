import os, json

while 1:
    try:
        with open(os.path.join('infolist', 'config.json')) as f: configInfo = json.loads(f.read())
        break
    except:
        print 'Load config.json failed, please check whether anything is wrong'

# Login info
userID = configInfo['userID']
password = configInfo['password']
baseUrl = configInfo['baseUrl']

# Infomation provided by user about cases and users
userNameStorage = os.path.join('infolist', configInfo['userNameStorage'])
caseStorage = os.path.join('infolist', configInfo['caseStorage'])
xmlInput = configInfo['xmlInput']

# Sheets stored for use
metaStorage = os.path.join('data', configInfo['metaStorage'])
uploadFile = os.path.join('data', configInfo['uploadFile'])
debugFile = os.path.join('data', configInfo['debugFile'])
