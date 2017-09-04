try:
    file = open("ip.txt","r")
    lines = file.readlines()
    ip = []
    for line in lines:
        line = str(line).replace("\n", "")
        ip.append(line)
    print ip
    file.close()
except:
    print "die"


