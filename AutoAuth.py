# AutoAuth - YKPS
# 2.0.0

import os

def notif(message):
    os.system('osascript -e \'display notification "%s" with title "AutoAuth" sound name "Basso"\''%message)
    exit()

try:
    from socket import gethostbyname, gethostname
    from uuid import UUID, getnode
    from urllib.parse import unquote
    import requests
except ImportError:
    notif('Error while importing [0x01]')

try:
    requests.packages.urllib3.disable_warnings() #Disable Warnings

    #Get Private IP Address and MAC Address
    ipAddr = gethostbyname(gethostname())
    macAddr = ':'.join([UUID(int=getnode()).hex[-12:].upper()[i:i+2] for i in range(0,11,2)])
except Exception:
    notif('Error while initializing [0x02]')

try:
    #Get Username and Password
    file = open('/Users/GeorgeYu/Library/Application Support/My Python Projects/AutoAuth/secret.DO_NOT_OPEN_THIS_FILE.txt')
    username = file.readline().strip()
    password = file.readline().strip()
except Exception:
    notif('Error while getting user info [0x03]')

try:
    #Web Authentication
    url = 'https://auth.ykpaoschool.cn/portalAuthAction.do'
    form_data = {'wlanuserip':ipAddr,'mac':macAddr,'wlanacname':'hh1u6p','wlanacIp':'192.168.186.2','userid':username,'passwd':password}

    requests.post(url,data=form_data,verify=False)
except Exception:
    notif('Error while logging in the web authentication [0x04]')

try:
    #The Blue Auth Page
    #Get authServ and oldURL
    headers={'Host': 'baike.baidu.com',
             'Connection': 'keep-alive',
             'Upgrade-Insecure-Requests': '1',
             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
             'Accept-Encoding': 'gzip, deflate, sdch',
             'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
             'Cookie': 'BDUSS=1TZkl1ZmY0UlNwMU1maWFzRFlISFJ-UXpxVkstZEZpVG9FNVlLSnFIRnhOSHRYQVFBQUFBJCQAAAAAAAAAAAEAAABk6aI00azT473I19MAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHGnU1dxp1NXN2; BAIDUID=CE9CF86CBB4C5C8EABE77A1511FF6BB1:FG=1; PSTM=1470233145; BIDUPSID=EEE7F3B881F3651B2B6B4C04B9D7EC1B'}
    web = requests.get('http://baike.baidu.com', allow_redirects=True, headers=headers)
    oldURL = unquote(web.url.split('oldURL=')[1].split('&')[0])
    authServ = unquote(web.url.split('authServ=')[1])
except IndexError:
    exit()
except Exception as e:
    notif('Error while trying to get required info [0x05]')
try:
    #Login
    url = 'http://192.168.1.1:8181/'
    form_data = {'txtUserName':username,'txtPasswd':password,'oldURL':oldURL,'authServ':authServ}
    requests.post(url,data=form_data,verify=False)
except Exception:
    notif('Error while loggin in the blue auth page [0x06]')
