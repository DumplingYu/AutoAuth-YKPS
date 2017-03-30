# AutoAuth - YKPS
# 3.1.5
# Author: George Yu
# URL: https://github.com/yu-george/AutoAuth-YKPS/

VERSION = '3.1.5'

def notif(message, exitAfter=True, soundName='Basso'):
    system('osascript -e \'display notification "{}" with title "AutoAuth" sound name "{}"\''.format(message, soundName))
    if exitAfter:
        exit()

try:
    from requests import get, post
    from requests.exceptions import Timeout
    from os import system, popen, path
    from sys import version_info
    from socket import gethostbyname, gethostname, getfqdn
    from uuid import UUID, getnode
    from urllib.parse import unquote
    from base64 import b64decode
    from threading import Thread
    from re import compile
except ImportError:
    notif('Error while importing [0x01]')

def check_update():
    try:
        web = get('https://raw.githubusercontent.com/yu-george/AutoAuth-YKPS/master/version', timeout=1.5)
        latest = web.text.strip()
        if latest != VERSION:
            notif('Update Available!', False)
    except Timeout:
        pass
    except Exception:
        pass

def login_webauth(): # Web Authentication
    try:
        url = 'https://auth.ykpaoschool.cn/portalAuthAction.do'
        form_data = {'wlanuserip': ipAddr,
                     'mac': macAddr,
                     'wlanacname': 'hh1u6p',
                     'wlanacIp': '192.168.186.2',
                     'userid': username,
                     'passwd':password}
        post(url, data=form_data, verify=False)
    except Exception:
        notif('Error while logging in the web authentication [0x04]')

def login_blueauth(): # The Blue Auth Page
    try: # Get authServ and oldURL
        headers = {'User-Agent': 'Mozilla/5.0',
                   'Accept-Encoding': 'gzip, deflate, sdch',
                   'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'}
        web = get('http://www.apple.com/cn/', allow_redirects=True, headers=headers)
        oldURL, authServ = compile(r'oldURL=([^&]+)&authServ=(.+)').findall(unquote(web.url))[0]
    except IndexError:
        return
    except Exception:
        notif('Error while trying to get required info [0x05]')
    try: # Login
        url = 'http://192.168.1.1:8181/'
        form_data = {'txtUserName': username,
                     'txtPasswd': password,
                     'oldURL': oldURL,
                     'authServ': authServ}
        post(url, data=form_data, verify=False)
    except Exception:
        notif('Error while loggin in the blue auth page [0x06]')

def auth():
    login_webauth()
    login_blueauth()

print(version_info)
if version_info[0] < 3:
    notif('Python version too old [0x00]')

try:
    # Get Private IP Address and MAC Address
    try:
        ipAddr = gethostbyname(gethostname())
    except Exception:
        try:
            ipAddr = gethostbyname(getfqdn())
        except Exception:
            ipAddr = popen("ifconfig | grep 'inet ' | grep -v '127.0' | xargs | awk -F '[ :]' '{print $2}'").readline().strip()
            if not ipAddr:
                raise Exception() # This exception will be excepted by the very outer except
    macAddr = ':'.join([UUID(int=getnode()).hex[-12:].upper()[i:i+2] for i in range(0,11,2)])
except Exception:
    notif('Error while initializing [0x02]')

try: # Get Username and Password
    file = open(path.expanduser('~/Library/Application Support/AutoAuth/usr.dat'))
    username = file.readline().strip()
    password = b64decode(file.readline().strip().encode()).decode()
    if not username or not password:
        raise Exception() # This exception will be excepted by the very outer except
except Exception:
    notif('Error while getting user info [0x03]')

Thread(target=check_update).start()
Thread(target=auth).start()
