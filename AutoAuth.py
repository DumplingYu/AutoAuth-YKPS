# AutoAuth - YKPS
# 3.1.1
# Author: George Yu
# Github: https://github.com/yu-george/AutoAuth-YKPS/

VERSION = '3.1.1'

try:
    import os
    import requests
    from socket import gethostbyname, gethostname, getfqdn
    from uuid import UUID, getnode
    from urllib.parse import unquote
    from base64 import b64decode
    from threading import Thread
except ImportError:
    notif('Error while importing [0x01]')

def notif(message):
    os.system('osascript -e \'display notification "{}" with title "AutoAuth" sound name "Basso"\''.format(message))
    exit()

def check_update():
    try:
        web = requests.get('https://raw.githubusercontent.com/yu-george/AutoAuth-YKPS/master/version', timeout=1.5)
        latest = web.text
        if latest != VERSION:
            os.system('osascript -e \'display notification "Update Available!" with title "AutoAuth" sound name "Glass"\'')
    except requests.exceptions.Timeout:
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
        requests.post(url, data=form_data, verify=False)
    except Exception:
        notif('Error while logging in the web authentication [0x04]')

def login_blueauth(): # The Blue Auth Page
    try: # Get authServ and oldURL
        headers = {'User-Agent': 'Mozilla/5.0',
                   'Accept-Encoding': 'gzip, deflate, sdch',
                   'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'}
        web = requests.get('http://www.apple.com/cn/', allow_redirects=True, headers=headers)
        oldURL = unquote(web.url.split('oldURL=')[1].split('&')[0])
        authServ = unquote(web.url.split('authServ=')[1])
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
        requests.post(url, data=form_data, verify=False)
    except Exception:
        notif('Error while loggin in the blue auth page [0x06]')

def auth():
    login_webauth()
    login_blueauth()

try:
    requests.packages.urllib3.disable_warnings() # Disable Warnings
    # Get Private IP Address and MAC Address
    ipAddr = gethostbyname(getfqdn())
    macAddr = ':'.join([UUID(int=getnode()).hex[-12:].upper()[i:i+2] for i in range(0,11,2)])
except Exception:
    notif('Error while initializing [0x02]')

try: # Get Username and Password
    file = open(os.path.expanduser('~/Library/Application Support/AutoAuth/usr.dat'))
    username = file.readline().strip()
    password = b64decode(file.readline().strip().encode()).decode()
except Exception:
    notif('Error while getting user info [0x03]')

Thread(target=check_update).start()
Thread(target=auth).start()
