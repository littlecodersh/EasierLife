from client.ExcelClient import ExcelClient
from client.LogClient_old import LogClient
import config

def uploadlog():
    iec = ExcelClient(config.uploadFile, sourceIndex = (0,1,2,4,3))
    oec = ExcelClient(outputDir = config.debugFile, outputHeader = ['case_num', 'case_id', 'date', 'time', 'description'])
    lc = LogClient(config.userID, config.password, config.baseUrl)
    lineNum = 2

    while raw_input('Ready to upload? [y]:') != 'y': pass

    while 1:
        mailInfo = iec.getData()
        if mailInfo is None: break
        if not lc.upload_log(*mailInfo):
            print 'Line %s: upload failed'%lineNum
            oec.storeData(mailInfo[:3] + [mailInfo[4], mailInfo[3]])
        lineNum += 1

    print 'Upload succeeded! Please check %s if you see something failed'%config.debugFile

if __name__ == '__main__':
    uploadlog()
