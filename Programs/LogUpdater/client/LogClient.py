#coding=utf8
import requests, json

class LogClient:
    def __init__(self):
        self.s = requests.Session()
        self.set_env()
        self.read_in_personal_info()
        while not self.login(): pass
        print 'Login Succeed'
    def set_env(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded', }
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
        def try_login():
            payloads = {
                'userID': self.userID,
                'password': self.password,
                'rememberuser': '1',
                'RegisterSource': '', }
            r = self.s.post(self.baseUrl + '/login/loginresult.aspx',
                data = payloads, headers = self.headers)
            return r.url
        if 'mydesktop' in try_login():
            cookiesList = {name:data for name,data in self.s.cookies.items()}
            self.OfficeID = cookiesList['UserOffice'] 
            self.emplId = cookiesList['User']
            return True
        print 'UserId or Password is incorrect'
        ans = raw_input('Change the config.json or [q]uit: ')
        if ans == 'q': raise Exception('User choose to quit')
        self.read_in_personal_info()
        return False
    def upload_log(self, clientId, caseId, date, description, hours = 0):
        try:
            payloads = {
                '__VIEWSTATE': '/wEPDwULLTE5NjYzNTQyNjJkZEmpSJnpIAxLpnCxj19EhiWWhyZe',
                '__VIEWSTATEGENERATOR': '2A830DFF',
                '__EVENTVALIDATION': '/wEWAgLWj8zjAQKVsJOsD2f8q58shkx5+PhMa3WQ3eQsx10v',
                'temp_hour1': '0',
                'temp_minute1': '0',
                'temp_hour2': '0',
                'temp_minute2': '0',
                'Savebtn1': '\261\243 \264\346',
                'wl_category' : '0',
                'wl_work_type': '01',
                'OfficeID' : self.OfficeID,
                'wl_empl_id' : self.emplId,
                'wl_client_id' : clientId,
                'wl_case_id' : caseId,
                'workdate': date,
                'wl_own_hours': hours,
                'wl_description': description.encode('gbk'), }
            r = self.s.post(self.baseUrl + '/worklog/worklogregister.aspx', data = payloads, headers = self.headers)
            return True if 'document.frmSaveSubmit.submit' in r.text else False
        except:
            return False

if __name__ == '__main__':
    lc = LogClient()
    r = lc.upload_log('0210866', '021M20140034', '2016-3-1', u'测试')
