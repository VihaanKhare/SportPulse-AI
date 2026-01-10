import requests
import random
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv() #load the env into python's os env

FETCH_PROXY_URL = os.getenv('FETCH_PROXY_URL') #api endpoint for fetching proxy ips
PATH = os.path.join(os.path.dirname(__file__),'data/free-proxy-list.txt') #file location to store all ip addresses 

proxyList = []

data = requests.get(FETCH_PROXY_URL)

#generates free-proxy-list.txt file
def generateFile():
    with open(PATH,'w') as file:
            file.write(data.text)

#initializes proxyList[]
def createProxyList():
    with open(PATH) as file:
        for index in range(0,20):
            line = file.readline().split('\n')[0]
            proxyList.append(line)

    
    return(proxyList)

#updates the proxy list after 10 minutes
def timeFileUpdateCheck(hour, minute):
    hour = int(hour)
    minute = int(minute)
    with open(os.path.join(os.path.dirname(__file__),'data/time.txt')) as file:
          timeString = file.read()
          prevHour = int(timeString.split(' ')[1].split(':')[0])
          prevMinute = int(timeString.split(' ')[1].split(':')[1])
    if(hour-prevHour>1):
         return True
    if(hour-prevHour <=1 and hour-prevHour>=0):
        minute = minute + 60*(hour-prevHour)
        if(minute-prevMinute>10):
              return True
        else:
             return False
    if(hour-prevHour<0):
        return True

#returns a random ip address from proxyList
def randomProxyPicker():
    if(os.path.exists(os.path.join(os.path.dirname(__file__),'data/time.txt'))):
        toCheck = timeFileUpdateCheck(f'{datetime.now().hour}',f'{datetime.now().minute}')
    else:
        with open(os.path.join(os.path.dirname(__file__),'data/time.txt'),'w') as f:
            f.write(f'{datetime.now().hour}:{datetime.now()}')
        toCheck = True
    if(toCheck == True): 
        with open(os.path.join(os.path.dirname(__file__),'data/time.txt'),'w') as f:
            f.write(f'{datetime.now().hour}:{datetime.now()}')
        generateFile()
    proxies = createProxyList()
    return random.choice(proxies)