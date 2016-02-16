#coding=utf8
from client.ExcelClient import ExcelClient

import json

def get_stored_cases(storageDir):
    # case_num, case_id, project
    ec = ExcelClient(storageDir, sourceIndex = (0,2,3))
    r = {}
    while 1:
        userInfo = ec.getData()
        if userInfo is None: break
        r[userInfo[2]] = [userInfo[0], userInfo[1]]
    return r

if __name__ == '__main__':
    with open('config.json') as f: configInfo = json.loads(f.read())
    print 'Getting the %s file.'%configInfo['metaStorage']
    caseDict = get_stored_cases(configInfo['caseStorage'])

    print 'Please wait for about half a minute'
    oec = ExcelClient(outputDir = configInfo['uploadFile'], outputHeader = ['case_num', 'case_id', 'date', 'description'])
    # to, filename, created_on, case_name, subject
    iec = ExcelClient(configInfo['metaStorage'], sourceIndex = (0,4,5,7,6))
    while 1:
        mailInfo = iec.getData()
        if not mailInfo: break
        outputList = []
        for key, value in caseDict.items():
            if '' != mailInfo[3] == key:
                outputList = sum([outputList, [value[0], value[1], mailInfo[2].replace('/','-'),
                    u'与{0}就{1}进行沟通，并发送{2}给{0}。'.format(mailInfo[0], mailInfo[1],
                        mailInfo[4].encode('utf8').split(':')[-1].split('：')[-1].decode('utf8'))]], [])
        if not outputList: raise Exception('Case on {} not found'.format(mailInfo[2]))
        oec.storeData(outputList)
    print 'Output succeeded! Please check %s before run the upload.py'%configInfo['uploadFile']
