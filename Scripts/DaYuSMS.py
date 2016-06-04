#coding=utf8
import json

import top

r = top.api.AlibabaAliqinFcTtsNumSinglecallRequest()
r.set_app_info(top.appinfo('your_app_key', 'your_app_secret'))
 
r.tts_param = json.dumps({
    'code': u'You will get this through you phone',})
r.extend = 'TG'
r.called_num = 'your_phone_number'
r.called_show_num = '4008823220'
r.tts_code = 'TTS_10265961'

try:
    print r.getResponse()
except Exception, e:
    print e.submsg
