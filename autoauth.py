import socket
import uuid
import requests

requests.packages.urllib3.disable_warnings() #Disable Warnings

#Get Private IP Address and MAC Address
ipAddr = socket.gethostbyname(socket.gethostname())
macAddr = ':'.join([uuid.UUID(int=uuid.getnode()).hex[-12:].upper()[i:i+2] for i in range(0,11,2)])

#Get Username and Password
try:
	with open('user.dat') as dataFile:
    	username = dataFile.readline().strip()
    	password = dataFile.readline().strip()
except Exception as e:
	print('[ERROR] %s'%e)
	input()
	exit(-1)

#Web Authentication Page
url = 'https://auth.ykpaoschool.cn/portalAuthAction.do'
form_data = {'wlanuserip':ipAddr,'mac':macAddr,'wlanacname':'hh1u6p','wlanacIp':'192.168.186.2','userid':username,'passwd':password}

try:
    requests.post(url, data=form_data, verify=False)
except Exception as e:
    print('[ERROR] %s'%e)
    input()
    exit(-1)

#Blue Auth Page
url = 'http://192.168.1.1:8181/'
authServ = 'KVW4EtNMbo5/+u85r456zjg2Mcg+SdmChszWCQWjWiXl1Hb1bV/hhqkkc1jK1CqKoWU4hu8EafvmvGBr9L74aRoQjMkO3nxJWNpRwQ51eSQlnpPK7WOMS0iWLxaoWod9na30aL17FfRXPHx6t5EkTCdCuL9YtXBacRji4GkjVThFKdRvRKIK0tzZFSmzxZbwGdu1SIyuWQrO7+LKyTsY+sHM6oxNyo3QUJsnjzH/GiMw6N6eJE1JgJ4PUam7+zoYqJPZMeFMWbRU8Spwt0KKmgsR7I8+hLT/xyr7FVOXQOMtwYbG83TNVnp95XDy9WPo3Rj0mDZtBOuQWjRyVRzl96gU0J76iQNbwjcB16mkQIrIsrmhNnxj94iZqv4rprdqkX87YMReXlt00YsomeEvU7kFfuuncY1iqYn/QMi3folyrlB5iyGlhjql5/zyRso3VPkE4Vn7qhsAl0c='
form_data = {'txtUserName':username,'txtPasswd':password,'authServ':authServ}

try:
    requests.post(url, data=form_data, verify=False)
except Exception as e:
    print('[ERROR] %s'%e)
    input()
    exit(-1)

print('You have been connected to Wi-Fi! Enjoy!')
