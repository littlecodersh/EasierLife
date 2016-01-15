import time, requests
phone = 'Your Phone Number'
count = 0

while True:
    r = requests.get('http://estock.xyzq.com.cn/validation/mobile?mobile=%s&_=1451390067874'%phone)
    count += 1
    print count
