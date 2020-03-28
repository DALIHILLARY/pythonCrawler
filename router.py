#!/usr/bin/env python3

#this is a simple script to control access to router

import requests
from bs4 import BeautifulSoup
import random
import string
import os
from time import sleep
from multiprocessing import Process


#function to pick/scrap last mac from router
def pickMac(activeMac):
    headers = {"GET":"/status/status_deviceinfo.htm HTTP/1.1",
                "Host":"192.168.3.47",
                "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language":"en-US,en;q=0.5",
                "Accept-Encoding":"gzip, deflate",
                "Connection":"close",
                "Cookie":"C0=21232f297a57a5a743894a0e4a801fc3; C1=5f4dcc3b5aa765d61d8327deb882cf99",
                "Upgrade-Insecure-Requests":"1",
                "Cache-Control":"max-age=0"}

    cookies = {"C0":"21232f297a57a5a743894a0e4a801fc3","C1":"5f4dcc3b5aa765d61d8327deb882cf99"}


    while(True):
        try:
            r = requests.get("http://192.168.3.47/status/status_deviceinfo.htm",cookies=cookies,headers=headers)

            soup = BeautifulSoup(r.text,'html.parser')
            soup = soup.find_all('table')[2]
            soup = soup.find_all('td')[2:]

            index = 1
            
            for _ in soup:
                index = index +1

                if(index%2 == 0):
                    continue

                activeMac.append(_.getText())
            #break out of infinte loop
            break

        except:

            print("\nERROR::>>FAILED TO ESTABLISH CONNECTION TO ROUTER\n")
            print("reconnecting Please Wait......")
            sleep(10)
    
    

    
def login():
    payload = {'tipsFlag':'0', 'timevalue':'0','Login_Name':'admin','uiWebLoginhiddenUsername':'21232f297a57a5a743894a0e4a801fc3','uiWebLoginhiddenPassword':'5f4dcc3b5aa765d61d8327deb882cf99'}
    headers={"POST":"/Forms/login_security_1 HTTP/1.1",
                "Host":"192.168.3.47",
                "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language":"en-US,en;q=0.5",
                "Accept-Encoding":"gzip, deflate",
                "Referer":"http://192.168.3.47/login_security.htm",
                "Content-Type":"application/x-www-form-urlencoded",
                "Content-Length":"196",
                "Connection":"close",
                "Upgrade-Insecure-Requests":"1"}

    url = 'http://192.168.3.47/Forms/login_security_1'

    while(True):
        try:
            r = requests.post(url,data=payload,headers=headers, allow_redirects=True)
        except:
            print("\n ERROR::>>FAILED TO ESTABLISH CONNECTION TO ROUTER\n")

        sleep(600)



def removeMac(parameters):
    url = 'http://192.168.3.47/Forms/home_wlan_1'
    cookies = {"C0":"21232f297a57a5a743894a0e4a801fc3","C1":"5f4dcc3b5aa765d61d8327deb882cf99"}
    headers={"POST":"/Forms/home_wlan_1 HTTP/1.1",
                "Host":"192.168.3.47",
                "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language":"en-US,en;q=0.5",
                "Accept-Encoding":"gzip, deflate",
                "Referer":"http://192.168.3.47/basic/home_wlan.htm",
                "Content-Type":"application/x-www-form-urlencoded",
                "Content-Length":"906",
                "Connection":"close",
                "Cookie":"C0=21232f297a57a5a743894a0e4a801fc3; C1=5f4dcc3b5aa765d61d8327deb882cf99",
                "Upgrade-Insecure-Requests":"1"}

    while(True):
        try:
            r = requests.post(url,cookies=cookies,headers=headers, data=parameters, allow_redirects=True)

            break
        except:
            print("\nERROR::>>FAILED TO ESTABLISH CONNECTION TO ROUTER\n")
            print("reconnecting Please Wait......")
            sleep(10)
   

#generate 8 alphanumeric password
def changePass(parameters={},activeUsers=[]):
    while(True):
        #execute after login process
        sleep(60*60)
        pickMac(activeUsers)

        for _ in [""]:
            try:
                activeUsers.remove(_)
            except:
                continue

        if len(activeUsers)==0:
            with open(".blockedUsers.txt","a+") as userMac:
                userMac.truncate(0)

            pickMac(activeUsers)

            """Generate a random string of letters and digits """
            lettersAndDigits = string.ascii_letters + string.digits
            newPass =  ''.join(random.choice(lettersAndDigits) for i in range(8))
            parameters.update({"PreSharedKey":newPass,"WLANFLT_MAC":""})
            removeMac(parameters)

            with open(".password.txt","w+") as passkey:
                passkey.write(newPass)






def monitor(parameters,time,blockedUsers,activeUsers,latestUser="",parameterx=[]):

    # print(parameters,time,blockedUsers,activeUsers,latestUser,parameterx)
    if len(latestUser) != 0:
        parameterx = parameters
        parameterx.update({"WLANFLT_MAC":activeUsers})
        removeMac(parameterx)

    else:
        pickMac(activeUsers)
        latestUser = activeUsers[-1]

    #make process sleep for specified time
    sleep(60*time)
    newBlockedUsers =[]
    with open(".blockedUsers.txt","a+") as userMac:
        userMac.write(latestUser+"\n")

    with open(".blockedUsers.txt","r") as users:
        blockedUsers = users.readlines()

    for _ in blockedUsers:
        
        newBlockedUsers.append(_.strip("\n"))

    parameterx = parameters
    parameterx.update({"WLANFLT_MAC":newBlockedUsers})
    removeMac(parameterx)


if __name__ == "__main__":

    activeUsers =[]
    blockedUsers =[]
    wifiPassword =""
    parameters ={"wlanWEBFlag":"0",
                "AccessFlag":"0",
                "wlan_APenable":"1",
                "DfsTypeChangeFlag":"0",
                "countrySelect":"93",
                "Channel_ID":"00000000",
                "AdvWlan_slPower":"High",
                "BeaconInterval":"100",
                "RTSThreshold":"2347",
                "FragmentThreshold":"2346",
                "DTIM":"1",
                "WirelessMode":"802.11b+g+n",
                "WLANChannelBandwidth":"Auto",
                "WLANGuardInterval":"Auto",
                "WLANMCS":"Auto",
                "WLSSIDIndex":"1",
                "ESSID":"KLICKNET CAFE BUKOTO",
                "wlan_PerSSIDenable":"1",
                "ESSID_HIDE_Selection":"0",
                "UseWPS_Selection":"0",
                "WPSMode_Selection":"1",
                "WEP_Selection":"WPA2-PSK",
                "WDSMode_Selection":"0",
                "WLAN_FltActive":"1",
                "WLAN_FltAction":"00000001",
                "WLanLockFlag":"0",
                "wlanRadiusWEPFlag":"0",
                "SSIDCheckFlag":"0"
                }

    login = Process(target=login,args=[])
    login.start()

    passKey = Process(target=changePass,args=[parameters,activeUsers])


    while(True):
        # login()
        blockedUsers.clear()
        if os.name == 'nt':
            os.system("cls")
        else:
            os.system("clear")

        password =""
        with open(".password.txt","r") as passkey:
            password = passkey.readline()
        print("NEW WIFI PASSWORD:::>>> %s" %password)
        menu ="\n1. Active Users\n2. Re-charge User"
        print(menu)
        print("Enter Options: ",end ="")

        while(True):
            choice = input()
            #menu to select data
            if choice == "1":
                activeUsers.clear()
                pickMac(activeUsers)
                counter =0
                print("ACTIVE USERS\n")
                for _ in activeUsers:
                    counter = counter+1
                    print("%d --> %s"%(counter,_))

                print("Press Enter to Continue")
                input()

                break
                

            elif choice == "2":
                if os.name == 'nt':
                    os.system("cls")
                else:
                    os.system("clear")
                    
                print("\n RE-CHARGE USER\n1. New Client\n2.Blocked Users\n \nEnter option: ",end="")
                while(True):
                    command = input()
                    if command =="1":
                        time = int(input("Enter time (min):  "))
                   
                        client = Process(target=monitor,args=[parameters,time,blockedUsers,activeUsers])
                        client.start()

                        # #create new process for client
                        # pid = os.fork()
                        # if pid == 0:
                        #     pickMac(activeUsers)
                        #     latestUser = activeUsers[-1]
                        #     print(latestUser)
                        #     #make process sleep for specified time
                        #     sleep(60*time)
                        #     with open(".blockedUsers.txt","a+") as userMac:
                        #         userMac.write(latestUser+"\n")

                        #     with open(".blockedUsers.txt","r") as users:
                        #         blockedUsers = users.readlines()
                            
                        #     newBlockedUsers = []
                        #     for _ in blockedUsers:
                        #         newBlockedUsers.append(_.strip("\n"))

                        #     parameterx = parameters
                        #     parameterx.update({"WLANFLT_MAC":newBlockedUsers})
                        #     removeMac(parameterx)
                        #     exit()
                        break
                    elif command == "2":
                        with open(".blockedUsers.txt","r") as users:
                            blockedUsers = users.readlines()
                        
                        oldBlockedUsers = []
                        for _ in blockedUsers:
                            oldBlockedUsers.append(_.strip("\n"))
                    
                        print("\n BLOCKED USERS")
                        counter = 0
                        for _ in oldBlockedUsers:
                            counter = counter+1
                            print("%d --> %s"%(counter,_))

                        userIndex = int(input("\nEnter User to Recharge: "))
                        user = oldBlockedUsers[userIndex-1]

                        oldBlockedUsers.remove(user)

                        try:
                            blockedUsers.remove(user+"\n")
                        except:
                            blockedUsers.remove(user)

                        with open(".blockedUsers.txt","w+") as users:
                            users.truncate()
                            for _ in blockedUsers:
                                users.write(_)

                        time = int(input("\nEnter time (min):  "))

                        client = Process(target=monitor,args=[parameters,time,blockedUsers,oldBlockedUsers,user])
                        client.start()

                        # #create new process for client
                        # pid = os.fork()
                        # monitor(parameters,time,blockedUsers,activeUsers,parameterx)
                        # if pid == 0:
                        #     removeMac(parameterx)

                        #         #make process sleep for specified time
                        #     sleep(60*time)
                        #     newBlockedUsers =[]
                        #     with open(".blockedUsers.txt","a+") as userMac:
                        #         userMac.write(user+"\n")

                        #     with open(".blockedUsers.txt","r") as users:
                        #         blockedUsers = users.readlines()
                            
                        #     for _ in blockedUsers:
                                
                        #         newBlockedUsers.append(_.strip("\n"))

                        #     parameterx = parameters
                        #     parameterx.update({"WLANFLT_MAC":newBlockedUsers})
                        #     removeMac(parameterx)

                        #     #terminate child process
                        #     exit()


                        break
                    else:
                        print("\n\nWrong choice Re-Enter command:  ",end="")
                
                break
                
            else:
                print("\n\nInvalid Choice Re-Enter command:  ",end="")




    
