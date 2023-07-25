#String Shuffler Experiment 3
#Version 1.5.0
#Last Updated: 25-07-2023
#DAWN/Experiments

import os
import sys
import csv
from json import dump
from random import shuffle
from threading import Thread
from multiprocessing import SimpleQueue
from time import sleep, time, ctime, strftime


n = 20
sdir = '.'
k, stime = 0,0
endOnAllHit = False
killAllThreads = False #Do not change before program execution
activity, hit = [], []
lIcon = ['|', '/', '-', '\\'] #Loading Animation Characters

#Program Description 
about='''
\033[36mProgram to experimentally calculate the probability of shuffling a string until the same string is obtained.\033[0m
\033[31mNote: There will be a time lag between Displaying Thread status and thread hit. To avoid this, allow endOnAllHit\033[0m\n
'''


def logger(message):
    #Logger function
    with open(sdir+'/log.txt', 'a') as log:
        log.write(strftime('%Y-%m-%d/%H:%M:%S> '))
        log.write(message)
        log.write('\n')


def generateReport(f, l, t):
    #Exports Report Data as JSON
    d = {'Record':sdir.split('/')[1], 'String':data, 'First Hit':[f], 'Last Hit':[l], 'Display Time':t}
    with open(sdir+'/data.json', 'w') as f:
        dump(d, f, indent=2)


def exportData(data):
    #Exports Report Data as CSV
    header = ['Thread', 'Iterations', 'Time']
    with open(sdir+'/data.csv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(header)
        writer.writerows(data)


def optimize(rdata):
    #Optimises Queue Data for Report Generation
    tdata, t = [],[]
    for i in rdata:
        tdata.append([rdata.index(i)+1,int(i.split('/')[0][15:]), float(i.split('/')[1][:-1])])
        t.append(float(i.split('/')[1][:-1]))
    fhit = [t.index(min(t))+1, tdata[t.index(min(t))][1], tdata[t.index(min(t))][2]]
    lhit = [t.index(max(t))+1, tdata[t.index(max(t))][1], tdata[t.index(max(t))][2]]
    return tdata, fhit, lhit


def shuffler(ostring, string, queue):
    #Shuffler
    global hit
    i=1
    try:
        while ostring != string:
            i+=1
            queue.put('\033[31mMismatch ({}/{})'.format(str(i),round(time()-stime,4)))
            shuffle(string)
            if killAllThreads: break
        else:
            t = time()
            hit.append('Yes')
            print('\a', end='')
            logger('Thread {} Success!'.format([i[1] for i in activity].index(queue)+1))
            while 1:
                queue.put('\033[32mSuccess! ({}/{})'.format(str(i),round(t-stime,4)))
                if killAllThreads: break
    except Exception as e:
       while 1:
            queue.put('\033[31m{}! (0/0)'.format(e))
            if killAllThreads: break
    return


def constructor(data, sdata):
    #Thread Constructor
    for i in range(n):
        q = SimpleQueue()
        t = Thread(target=shuffler, args=(data, sdata, q))
        t.daemon = True
        activity.append([t, q])


def checkHit():
    #Function to Check whether All Thread hit. Applicable only if EndOnAllHit = True
    global killAllThreads
    while 1:
        if len(hit) == n:
            killAllThreads = True
            break


def clear():
    #Clears console output
    if sys.platform == 'linux': os.system('clear')
    else: os.system('cls')


def initialise(endOnAllHit):
    #Function for Initialising Threads and Generating Directories for Reports
    global stime
    global sdir
    sdir+=strftime('/Records/%Y%m%d%H%M%S')
    if not(os.path.exists('./Records')): os.mkdir('Records')
    os.mkdir(sdir)
    stime = time()
    for i in activity: i[0].start()
    if endOnAllHit:
        t = Thread(target=checkHit)
        t.daemon = True
        t.start()


#main
if sys.platform != 'linux': os.system('echo on') #To enable ASCII codes in Windows

#Introduction
print('\033[33mString Shuffler Test 2')
print('Powered By DAWN/Experiments\033[0m\n')
print(ctime())
print(about)

#User Input
data = list(input('Enter string: '))
n = int(input('Number of threads: '))
endOnAllHit = True if input('End program on all thread hit? (Y/N): ')[0].upper() == 'Y' else False
print(data, '\n')
sleep(2)
sdata = data.copy()
shuffle(sdata)
constructor(data, sdata)
initialise(endOnAllHit)
while 1:
    k = k+1 if k < 3 else 0
    #Obtaining Thread Status from Queues
    rdata = [i[1].get() for i in activity]

    #Header
    print('\033[33mshuffler 1.5.0')
    print('A Probability simulation program for obtaining the same combination after shuffling a string')
    print('\nShuffling {}> [{}]\n\n\033[0m'.format(data, lIcon[k]))

    #Thread Status
    for i in range(0,n,1):
        if i % 5 == 0 and i != 0: print('\n')
        print('\033[0mT{}:'.format(i+1), rdata[i], end='| ', flush=True)

    #Display Time
    if int(time()-stime) > 60: print('\n\n\033[36mTime taken:', round((time()-stime)/60, 2), 'minutes\033[0m\n')
    else: print('\n\n\033[36mTime taken:', round(time()-stime, 2), 'seconds\033[0m\n')
    sleep(0.01)

    #Footer
    print('\n\n\033[32mDAWN/Experiments')
    clear()

    #Shifting to report phase on All Thread Hit or 'Success' flag from Queues
    if all(['\033[32mSuccess' == i[:12] for i in rdata]) or killAllThreads == True:
        t = time()
        print('\a', end='')
        killAllThreads = True
        tdata,fhit,lhit = optimize(rdata)

        #HitReport
        print('\033[36m\nAll threads terminated successfully')
        print('Display Time:', round((t-stime)/60, 2), 'minutes')
        print('\n-----First Hit-----')
        print('Thread:', fhit[0])
        print('Iterations:', fhit[1])
        print('Time:', fhit[2], 'seconds')
        print('-------------------\n')
        print('\n-----Last Hit-----')
        print('Thread:', lhit[0])
        print('Iterations:', lhit[1])
        print('Time:', lhit[2], 'seconds')
        print('------------------\n')
        generateReport(fhit, lhit, round((t-stime)/60, 2))
        exportData(tdata)
        ch = input('Press any key to exit\033[0m')
        break
sys.exit()
