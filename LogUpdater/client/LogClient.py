#coding=utf8
import requests, json

class LogClient:
    def __init__(self):
        self.read_in_personal_info()
        self.s = requests.Session()
        while not 'userstatus' in self.login(): print 'Try Again'
        print 'Login Succeed'
    def read_in_personal_info(self):
        with open('config.json') as f:
            try:
                personal_info = json.loads(f.read())
                self.userID = personal_info['userID']
                self.password = personal_info['password']
                self.baseUrl = personal_info['baseUrl']
            except:
                print 'Load personal data failed, please check config.json'
    def login(self):
        r = self.s.get(self.baseUrl + '/count.asp', stream = True)
        with open('count.jpg', 'wb') as f: f.write(r.content)
        mofei = raw_input('mofei: ')
        payloads = {
            'userID': self.userID,
            'password': self.password,
            'mofei': mofei, }
        headers = { 'Content-Type': 'application/x-www-form-urlencoded', }
        r = self.s.post(self.baseUrl + '/loginResult.asp',
            data = payloads, headers = headers)
        return r.url
    def upload_log(self, clientId, caseId, date, description):
        payloads = {
            'RegisterType': 'NEW',
            'wl_category' : '0',
            'wl_client_id' : clientId,
            'wl_case_id' : caseId,
            'wl_empl_id' : '111',
            'wl_work_type': '01',
            'wl_date': date,
            'wl_own_hours': '0',
            'wl_start_date': '09:00',
            'wl_description': description.encode('gbk'),}
        headers = { 'Content-Type': 'application/x-www-form-urlencoded', }
        r = self.s.post(self.baseUrl + '/worklog/WorklogSave.asp', data = payloads, headers = headers)

if __name__ == '__main__':
    lc = LogClient()
    lc.upload_log('0210340', '021G20110002', '2016-2-3', u'测试')

