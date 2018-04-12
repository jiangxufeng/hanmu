from celery import task
import requests
import json
import time
import hashlib
import random
import sys
from bs4 import BeautifulSoup as bs
from datetime import datetime
from .message import send_sms
import uuid


def MD5(s):
    return hashlib.md5(s.encode()).hexdigest()


def encrypt(s):
    result = ''
    for i in s:
        result += table[ord(i) - ord('0')]
    return result


alphabet = list('abcdefghijklmnopqrstuvwxyz')
random.shuffle(alphabet)
table = ''.join(alphabet)[:10]

API_ROOT = 'http://client3.aipao.me/api'
Version = '2.11'

@task
def run_u():
    IMEI = 'f55ed0d195f94077b42010a470f68de2'
    RunDist = str(1600 + random.randint(0, 3))  # meters
    RunStep = str(random.randint(1000, 1300))
    RunTime = str(random.randint(720, 1000))
 #   print('11')

    TokenRes = requests.get(
        API_ROOT + '/%7Btoken%7D/QM_Users/Login_AndroidSchool?IMEICode=' + IMEI)
    TokenJson = json.loads(TokenRes.content.decode('utf8', 'ignore'))

    print(TokenJson)
    try:
        last_time, count = get_late_time(248397)
        #       print(last_time)
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')[:10]
        #       print(now)
    except:
        return False
    if last_time == now:
        return False
    if count >= 32:
        return False
    # headers
    token = TokenJson['Data']['Token']
    userId = str(TokenJson['Data']['UserId'])
    timespan = str(time.time()).replace('.', '')[:13]
    auth = 'B' + MD5(MD5(IMEI)) + ':;' + token
    nonce = str(random.randint(100000, 10000000))
    sign = MD5(token + nonce + timespan + userId).upper()


    header = {'nonce': nonce, 'timespan': timespan,
              'sign': sign, 'version': Version, 'Accept': None, 'User-Agent': None, 'Accept-Encoding': None, 'Connection': 'Keep-Alive'}

    # Start Running
    SRSurl = API_ROOT + '/' + token + '/QM_Runs/SRS?S1=30.534737&S2=114.367785&S3=1600'
    SRSres = requests.get(SRSurl, headers=header, data={})
    SRSjson = json.loads(SRSres.content.decode('utf8', 'ignore'))


  #  Running Sleep
    StartT = time.time()
    for i in range(int(RunTime)):
        time.sleep(1)
        print("Current Minutes: %d Running Progress: %.2f%%\r" %
             (i / 60, i * 100.0 / int(RunTime)))
    print("")
    print("Running Seconds:", time.time() - StartT)


    # print(SRSurl)
    # print(SRSjson)

    RunId = SRSjson['Data']['RunId']

    # End Running
    EndUrl = API_ROOT + '/' + token + '/QM_Runs/ES?S1=' + RunId + '&S4=' + \
        encrypt(RunTime) + '&S5=' + encrypt(RunDist) + \
        '&S6=&S7=1&S8=' + table + '&S9=' + encrypt(RunStep)

    EndRes = requests.get(EndUrl, headers=header)
    EndJson = json.loads(EndRes.content.decode('utf8', 'ignore'))

    # print("-----------------------")
    # print("Time:", RunTime)
    # print("Distance:", RunDist)
    # print("Steps:", RunStep)
    # print("-----------------------")
    param = json.dumps({
        'count': count+1
    })
    if EndJson['Success']:
        business_id = uuid.uuid1()
        try:
            send_sms(business_id, '13260628109', "偷懒玩家", 'SMS_130913044', param)
        except:
            return True


def get_late_time(UserId):
    url = 'http://sportsapp.aipao.me/Manage/UserDomain_SNSP_Records.aspx/MyResutls?userId=%d' % UserId
    header = {
        'Host': 'sportsapp.aipao.me',
        'User-Agent': 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Connection': 'keep-alive'
    }
    html = requests.get(url, headers=header).text
   # print(html.text)
    soup = bs(html, 'lxml')
    last_time = soup.find(attrs={'class': 'time'})
    num = soup.find_all(attrs={'class': 'mod01'})
    #   print(last_time.text)
    count = num[1].text.strip()[:2]
 #   print(last_time.text)
    return last_time.text, count


if __name__ == '__main__':
    get_late_time(248397)