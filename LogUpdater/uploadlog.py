from client.ExcelClient import ExcelClient
from client.LogClient import LogClient

import json

if __name__ == '__main__':

    with open('config.json') as f: configInfo = json.loads(f.read())
    iec = ExcelClient(configInfo['metaStorage'], sourceIndex = (0,1,2,3))
    oec = ExcelClient(outputDir = configInfo['bugFile'], outputHeader = ['case_num', 'case_id', 'date', 'description'])
    lc = LogClient()
    lineNum = 2

    while 1:
        mailInfo = ec.getData()
        if mailInfo is None: break
        if not lc.upload_log(*mailInfo):
            print 'Line %s: upload failed'%lineNum
            oec.storeData(mailInfo)
        lineNum += 1

    print 'Upload succeeded! Please check %s if you see something failed'%configInfo['bugFile']
