#!/usr/bin/env python
'''
Created on Oct 26, 2017

@author: Luis Gallet
'''
import subprocess, sys, socket
 
def TraceRoute(ipAddress):
    cmd = ["tracert", "-d", "-w", "1000", "-h", "50", ipAddress]
    res = ''
    responseList = []
    try:
        response = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = response.communicate()
        
        if output:
            if response.returncode == 0:
                res = output
        if error:
            res = "Error "+ str(response.returncode)+ ": "+ str(error.strip(),'utf-8')
    except OSError as e:
        res = "Error "+ e.errno+ " "+ e.strerror+ " "+ e.filename
    except:
        res = "Error "+ sys.exc_info()[0]

    if not res:
        print("Command failed")
    else:
        if res.startswith(b'Error'):
            return res
        else:
            res = (str(res,'utf-8')).strip()
            res = res.replace("\r", "")
            splitted = res.split("\n")
            
            for element in splitted:
                element = element.strip()
                if element:
                    responseList.append(element)   
                         
            #remove first and last element of the list
            del responseList[0]
            del responseList[len(responseList)-1]
            hops, RTT = __ParseResponse(responseList)
            
            IPaddrFromKnownLoc = socket.gethostbyname(socket.gethostname())
            c = 300000000
            # c = (2*distance)/RTT
            # distance = (c * RTT)/2
            distance = (c*RTT)/2000000
            
            print("From:" + IPaddrFromKnownLoc + " to:" + ipAddress + " Hops:" + str(hops) + " RTT:" + str(RTT) + "ms" + " Distance:" + str(distance) + " radius in km")
            return "From:" + IPaddrFromKnownLoc + " to:" + ipAddress + " Hops:" + str(hops) + " RTT:" + str(RTT) + "ms" + " Distance:" + str(distance) + " radius in km"
                          
def readFile(myFile):
    read_data = ""
    with open(myFile) as f:
        read_data = f.read().splitlines()
    #print(read_data)
    return read_data

def __ParseResponse(routeList):
    RTTListPerHops = []
    hops = len(routeList) 
    
    for route in routeList:
        timesPerHopList = route.split()    
        del timesPerHopList[0]
        del timesPerHopList[len(timesPerHopList)-1]
        avgRTT = 0
        valueCounter = 0
        for item in timesPerHopList:
            if item == "<1":
                time = 0
            else:
                try:
                    time = int(item)
                except ValueError:
                    continue
            avgRTT += time
            valueCounter += 1
        avgRTT = (avgRTT/valueCounter) if (valueCounter > 0) else 0 
        RTTListPerHops.append(avgRTT)
    
    RTTListPerHops.sort()
    RTT = RTTListPerHops[len(RTTListPerHops)-1]
    
    return[hops, RTT]

if __name__ == '__main__':
    for index, IPs in enumerate(sys.argv):
        if index == 0:
            continue
        else:
            my_data = []
            theIPs = readFile(IPs)
            for x in theIPs:
                my_data.append(TraceRoute(x))
            f = open('Results.txt','w')
            for x in my_data:
                f.write(x+"\n")    