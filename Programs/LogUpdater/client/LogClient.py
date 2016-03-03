#coding=utf8
import requests, os, re

DEBUG = False

class LogClient:
    def __init__(self, userID, password, baseUrl):
        self.userID = userID
        self.password = password
        self.baseUrl = baseUrl
        self.s = requests.Session()
        self.set_env()
        self.read_in_personal_info()
        if not self.login(): os._exit()
        self.get_view_settings()
    def set_env(self):
        self.headers = {
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.3; WOW64; Trident/7.0; .NET4.0E; .NET4.0C; InfoPath.3; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729)',
            'Content-Type': 'application/x-www-form-urlencoded', }
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
        return False
    def get_view_settings(self):
        r = self.s.get(self.baseUrl + '/worklog/worklogregister.aspx', headers = self.headers)
        regex = {
            '__VIEWSTATE': 'id="__VIEWSTATE" value="(.*?)" />',
            '__VIEWSTATEGENERATOR': 'id="__VIEWSTATEGENERATOR" value="(.*?)" />',
            '__EVENTVALIDATION': 'id="__EVENTVALIDATION" value="(.*?)" />', }
        for key, value in regex.items(): regex[key] = re.compile(value)
        self.viewSetting = {key: re.findall(value, r.text) for key, value in regex.items()}
    def upload_log(self, clientId, caseId, date, description, hours = 0):
        try:
            payloads = {
                "__VIEWSTATE": self.viewSetting['__VIEWSTATE'],
                '__VIEWSTATEGENERATOR': self.viewSetting['__VIEWSTATEGENERATOR'],
                "__EVENTVALIDATION": self.viewSetting['__EVENTVALIDATION'],
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
            if DEBUG:
                with open('debug.htm','w') as f: f.write(r.content)
            return True if 'document.frmSaveSubmit.submit' in r.text else False
        except:
            return False

if __name__ == '__main__':
    lc = LogClient()
    r = lc.upload_log('0210866', '021M20140034', '2016-3-1', u'测试', 0)
