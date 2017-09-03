#!/usr/bin/python
#encoding=utf8  
# leslie

from threading import Thread
import time
import os
import commands
import urllib
import json
import platform
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 此处加入ip 注意列表格式-_-
ip = [  '101.254.176.225',
        '222.186.56.1',
        '103.236.136.1',
        '103.42.212.162', 
        '47.89.38.47', 
        '103.95.29.1',
        '103.88.45.1', 
        '103.86.46.1',
        '92.223.73.113',
        '103.19.8.83',
        '92.223.80.1',
        '45.76.70.196', 
        '103.82.5.171', 
        '185.199.225.67',
        '216.189.158.66',
        '109.230.219.1',
        '185.194.236.25',
        '89.34.26.50',
        '176.31.141.12',
    ]

region = []
delay = []
lost = []
sent = []
sysstr = platform.system()

def requestInfo(ip,i):
    response = urllib.urlopen('https://ip.huomao.com/ip?ip=' + ip)
    jsonstr = json.loads(response.read())
    region[i] = jsonstr["country"] + jsonstr["province"] + jsonstr["city"] + jsonstr["isp"]

def printDelay():
    while 1:
        if sysstr == "Darwin":
            os.system('clear')
            for i in range(len(ip)):
                print ip[i] + "\t" + "dalay:" + delay[i] + " " + "lost:" + str(lost[i]) + " \t" + "sent:" + str(sent[i]) + "\t" + region[i]
        elif sysstr == "Linux":
            os.system('clear')
            for i in range(len(ip)):
                print ip[i] + "\t" + "dalay:" + delay[i] + "\b " + "lost:" + str(lost[i]) + " \t" + "sent:" + str(sent[i]) + "\t" + region[i]
        elif sysstr == "Windows":
            os.system('cls')
            for i in range(len(ip)):
                print ip[i] + "\t" + "dalay:" + delay[i] + " " + "lost:" + str(lost[i]) + " \t" + "sent:" + str(sent[i]) + "\t" + region[i]
        
        time.sleep(1)

def ping(ip,i):
    while 1:
        output = ""
        if sysstr == "Darwin":
            output = commands.getoutput("ping -c 1 -t 1 " + ip + "|grep time|awk -F '=' '{print $4}'")
        elif sysstr == "Linux":
            output = commands.getoutput("ping -c 1 -w 1 " + ip + "|grep time|awk -F '=' '{print $4}'")
        elif sysstr == "Windows":
            output = commands.getoutput("ping -n 1 -w 500 " + ip).replace("'{ '", "").decode("GBK").encode("UTF-8")
            output = commands.getoutput("echo " + output + "|grep 时间=").replace("'{ '", "").decode("GBK").encode("UTF-8")
            output = commands.getoutput("echo " + output + "|awk -F '=' '{print $3}'").replace("'{ '", "").decode("GBK").encode("UTF-8")
            # output = commands.getoutput("ping -n 1 -w 500 " + ip + "|grep 时间=|awk -F '=' '{print $3}'")
        if output == "":
            lost[i] += 1
            output = "          "
        else:
            if len(output) < 10:
                output += " "
        sent[i] += 1
        delay[i] = output
        time.sleep(0.5)

def main():
    # init
    for i in range(len(ip)):
        region.append("")
        delay.append("")
        lost.append(0)
        sent.append(0)
    for i in range(len(ip)):
        t = Thread(target=ping, args=(ip[i],i))
        t.start()
    for i in range(len(ip)):
        t = Thread(target=requestInfo, args=(ip[i],i))
        t.start()
    th = Thread(target=printDelay)
    th.start()
    q = raw_input()
    if q == "q":
        sys.exit(0)

if __name__ == '__main__':
	main()