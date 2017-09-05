#!/usr/bin/python
#encoding=utf8  
# leslie

# 此处加入ip 注意列表格式-_-
# 如果当前目录存在ip.txt 则优先读取文件
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
        '216.45.55.35',
        '216.189.158.66',
        '185.199.225.67',
        '66.70.158.60',
        '109.230.219.1',
        '185.194.236.25',
        '89.34.26.50',
        '109.235.69.33',
        '176.31.141.12',
        '5.196.116.230',
        '127.0.0.1'
    ]

# 第三方pure pyhton ping 实现
# 修改了my_ID变量的获取方式
# 修改了主方法返回类型
##########################################################
"""
    A pure python ping implementation using raw socket.


    Note that ICMP messages can only be sent from processes running as root.


    Derived from ping.c distributed in Linux's netkit. That code is
    copyright (c) 1989 by The Regents of the University of California.
    That code is in turn derived from code written by Mike Muuss of the
    US Army Ballistic Research Laboratory in December, 1983 and
    placed in the public domain. They have my thanks.

    Bugs are naturally mine. I'd be glad to hear about them. There are
    certainly word - size dependenceies here.

    Copyright (c) Matthew Dixon Cowles, <http://www.visi.com/~mdc/>.
    Distributable under the terms of the GNU General Public License
    version 2. Provided with no warranties of any sort.

    Original Version from Matthew Dixon Cowles:
      -> ftp://ftp.visi.com/users/mdc/ping.py

    Rewrite by Jens Diemer:
      -> http://www.python-forum.de/post-69122.html#69122


    Revision history
    ~~~~~~~~~~~~~~~~

    March 11, 2010
    changes by Samuel Stauffer:
    - replaced time.clock with default_timer which is set to
      time.clock on windows and time.time on other systems.

    May 30, 2007
    little rewrite by Jens Diemer:
     -  change socket asterisk import to a normal import
     -  replace time.time() with time.clock()
     -  delete "return None" (or change to "return" only)
     -  in checksum() rename "str" to "source_string"

    November 22, 1997
    Initial hack. Doesn't do much, but rather than try to guess
    what features I (or others) will want in the future, I've only
    put in what I need now.

    December 16, 1997
    For some reason, the checksum bytes are in the wrong order when
    this is run under Solaris 2.X for SPARC but it works right under
    Linux x86. Since I don't know just what's wrong, I'll swap the
    bytes always and then do an htons().

    December 4, 2000
    Changed the struct.pack() calls to pack the checksum and ID as
    unsigned. My thanks to Jerome Poincheval for the fix.

    Januari 27, 2015
    Changed receive response to not accept ICMP request messages.
    It was possible to receive the very request that was sent.

    Last commit info:
    ~~~~~~~~~~~~~~~~~
    $LastChangedDate: $
    $Rev: $
    $Author: $
"""


import os, sys, socket, struct, select, time, random

if sys.platform == "win32":
    # On Windows, the best timer is time.clock()
    default_timer = time.clock
else:
    # On most other platforms the best timer is time.time()
    default_timer = time.time

# From /usr/include/linux/icmp.h; your milage may vary.
ICMP_ECHO_REQUEST = 8 # Seems to be the same on Solaris.


def checksum(source_string):
    """
    I'm not too confident that this is right but testing seems
    to suggest that it gives the same answers as in_cksum in ping.c
    """
    sum = 0
    countTo = (len(source_string)/2)*2
    count = 0
    while count<countTo:
        thisVal = ord(source_string[count + 1])*256 + ord(source_string[count])
        sum = sum + thisVal
        sum = sum & 0xffffffff # Necessary?
        count = count + 2

    if countTo<len(source_string):
        sum = sum + ord(source_string[len(source_string) - 1])
        sum = sum & 0xffffffff # Necessary?

    sum = (sum >> 16)  +  (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff

    # Swap bytes. Bugger me if I know why.
    answer = answer >> 8 | (answer << 8 & 0xff00)

    return answer


def receive_one_ping(my_socket, ID, timeout):
    """
    receive the ping from the socket.
    """
    timeLeft = timeout
    while True:
        startedSelect = default_timer()
        whatReady = select.select([my_socket], [], [], timeLeft)
        howLongInSelect = (default_timer() - startedSelect)
        if whatReady[0] == []: # Timeout
            return

        timeReceived = default_timer()
        recPacket, addr = my_socket.recvfrom(1024)
        icmpHeader = recPacket[20:28]
        type, code, checksum, packetID, sequence = struct.unpack(
            "bbHHh", icmpHeader
        )
        # Filters out the echo request itself. 
        # This can be tested by pinging 127.0.0.1 
        # You'll see your own request
        if type != 8 and packetID == ID:
            bytesInDouble = struct.calcsize("d")
            timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]
            return timeReceived - timeSent

        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return


def send_one_ping(my_socket, dest_addr, ID):
    """
    Send one ping to the given >dest_addr<.
    """
    dest_addr  =  socket.gethostbyname(dest_addr)

    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    my_checksum = 0

    # Make a dummy heder with a 0 checksum.
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, ID, 1)
    bytesInDouble = struct.calcsize("d")
    data = (192 - bytesInDouble) * "Q"
    data = struct.pack("d", default_timer()) + data

    # Calculate the checksum on the data and the dummy header.
    my_checksum = checksum(header + data)

    # Now that we have the right checksum, we put that in. It's just easier
    # to make up a new header than to stuff it into the dummy.
    header = struct.pack(
        "bbHHh", ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), ID, 1
    )
    packet = header + data
    my_socket.sendto(packet, (dest_addr, 1)) # Don't know about the 1


def do_one(dest_addr, timeout):
    """
    Returns either the delay (in seconds) or none on timeout.
    """
    icmp = socket.getprotobyname("icmp")
    try:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    except socket.error, (errno, msg):
        if errno == 1:
            # Operation not permitted
            msg = msg + (
                " - Note that ICMP messages can only be sent from processes"
                " running as root."
            )
            raise socket.error(msg)
        raise # raise the original error

    # my_ID = os.getpid() & 0xFFFF
    # my_ID = threading.current_thread().ident & 0xFFFF
    my_ID = int(str(random.random()).replace("0.", "")) & 0xFFFF

    send_one_ping(my_socket, dest_addr, my_ID)
    delay = receive_one_ping(my_socket, my_ID, timeout)

    my_socket.close()
    return delay


def verbose_ping(dest_addr, timeout = 1, count = 1):
    """
    Send >count< ping to >dest_addr< with the given >timeout< and display
    the result.
    """
    for i in xrange(count):
        # print "ping %s..." % dest_addr,
        try:
            delay  =  do_one(dest_addr, timeout)
        except socket.gaierror, e:
            #print "failed. (socket error: '%s')" % e[1]
            return ""
            break

        if delay  ==  None:
            #print "failed. (timeout within %ssec.)" % timeout
            return ""
        else:
            delay  =  delay * 1000
            # print "get ping in %0.2fms" % delay
            return "%0.3f ms" % delay
    print





# multiping 实现
# leslie
################################################

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

region = []
delay = []
lost = []
loststr = []
sent = []
sentstr = []
sysstr = platform.system()

def requestinfo(ip,i):
    response = urllib.urlopen('https://ip.huomao.com/ip?ip=' + ip)
    jsonstr = json.loads(response.read())
    region[i] = jsonstr["country"] + jsonstr["province"] + jsonstr["city"] + jsonstr["isp"]

def printdelay():
    while 1:
        clear = ""
        if sysstr == "Windows":
            clear = "cls"
        else:
            clear = "clear"
        os.system(clear)
        for i in range(len(ip)):
            print ip[i] + "\t" + "dalay:" + delay[i] + "lost:" + loststr[i] + "sent:" + sentstr[i] + region[i]
        time.sleep(1)

def ping(ip,i):
    while 1:
        if sysstr == "Darwin":
            output = commands.getoutput("ping -c 1 -t 1 " + ip + "|grep time|awk -F '=' '{print $4}'")
        else:
            output = verbose_ping(ip)
        if output == "":
            output = "丢失       "
            lost[i] += 1
            le = len(str(lost[i]))
            if le == 1:
                loststr[i] = str(lost[i]) + "  "
            elif le == 2:
                loststr[i] = str(lost[i]) + " "
        else:
            le = len(output)
            if le == 7:
                output += "     "
            elif le == 8:
                output += "   "
            elif le == 9:
                output += "  "
            elif le == 10:
                output += " "
        sent[i] += 1
        le = len(str(sent[i]))
        if le == 1:
            sentstr[i] = str(sent[i]) + "    "
        elif le == 2:
            sentstr[i] = str(sent[i]) + "   "
        elif le == 3:
            sentstr[i] = str(sent[i]) + "  "
        elif le == 4:
            sentstr[i] = str(sent[i]) + " "
        delay[i] = output
        time.sleep(0.5)

def main():
    try:
        # 处理win记事本会把utf-8保存为utf-8 BOM的问题
        BOM = b'\xef\xbb\xbf'
        with open("ip.txt", 'rb') as f:
            if f.read(3) == BOM:
                data = f.read()
                with open("ip.txt", 'wb') as f:
                    f.write(data)
                    f.close()
        file = open("ip.txt","r")
        lines = file.readlines()
        global ip
        ip = []
        for line in lines:
            if str(line).startswith("#"):
                continue
            line = str(line).replace("\n", "").replace(" ", "")
            if line == "":
                continue
            ip.append(line)
        file.close()
    except:
        file = open("ip.txt", "w")
        file.write("# 此处增删ip 一行一个 保存之后重新启动脚本\n")
        for i in range(len(ip)):
            file.write(ip[i] + "\n")
        file.close()
    for i in range(len(ip)):
        region.append("")
        delay.append("")
        lost.append(0)
        loststr.append("   ")
        sent.append(0)
        sentstr.append("     ")
    for i in range(len(ip)):
        t = Thread(target=ping, args=(ip[i],i))
        t.start()
    for i in range(len(ip)):
        t = Thread(target=requestinfo, args=(ip[i],i))
        t.start()
    th = Thread(target=printdelay)
    th.start()
    q = raw_input()
    if q == "q":
        sys.exit(0)

if __name__ == '__main__':
	main()







