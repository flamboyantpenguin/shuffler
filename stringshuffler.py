#String Shuffler Experiment 3
#Version 1.5.0
#Last Updated: 25-07-2023
#DAWN/Experiments

import os
import sys
import csv
from json import dump
from random import shuffle
from time import sleep, time, ctime, strftime
from threading import Thread
from multiprocessing import SimpleQueue


k = 0
n = 20
stime = 0
sdir = '.'
activity = []
lIcon = ['|', '/', '-', '\\']
about='''
\033[36mProgram to experimentally calculate the probability of shuffling a string until the same string is obtained.

Probability of shuffling a string without repetition is 1/(n!)

-----Probability of shuffling a string by m threads at the same time-----

A -> Atleast one success

\t\tP(A) = 1-((n!-1)**m/(n!)**m)
where m is the number of threads and n is the number of letters (without repetition)\033[0m\n
'''


def logger(message):
    with open(sdir+'/log.txt', 'a') as log:
        log.write(strftime('%Y-%m-%d/%H:%M:%S> '))
        log.write(message)
        log.write('\n')


def generateReport(f, l, t):
    d = {'Record':sdir.split('/')[1], 'String':data, 'First Hit':[f], 'Last Hit':[l], 'Display Time':t}
    with open(sdir+'/data.json', 'w') as f:
        dump(d, f, indent=2)


def exportData(data):
    header = ['Thread', 'Iterations', 'Time']
    with open(sdir+'/data.csv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(header)
        writer.writerows(data)


def optimize(rdata):
    tdata, t = [],[]
    for i in rdata:
        tdata.append([rdata.index(i)+1,int(i.split('/')[0][15:]), float(i.split('/')[1][:-1])])
        t.append(float(i.split('/')[1][:-1]))
    fhit = [t.index(min(t))+1, tdata[t.index(min(t))][1], tdata[t.index(min(t))][2]]
    lhit = [t.index(max(t))+1, tdata[t.index(max(t))][1], tdata[t.index(max(t))][2]]
    return tdata, fhit, lhit


def shuffler(ostring, string, queue):
    i=1
    try:
        while ostring != string:
            i+=1
            queue.put('\033[31mMismatch ({}/{})'.format(str(i),round(time()-stime,4)))
            shuffle(string)
            if 'kill' in globals():
                break
        else:
            t = time()
            print('\a', end='')
            logger('Thread {} Success!'.format([i[1] for i in activity].index(queue)+1))
            while 1:
                queue.put('\033[32mSuccess! ({}/{})'.format(str(i),round(t-stime,4)))
                logger(str(globals()))
                if 'kill' in globals():
                    break
    except Exception as e:
       while 1:
            queue.put('\033[31m{}! (0/0)'.format(e))
            if 'kill' in globals():
                break
    return


def constructor(data, sdata):
    #Constructor
    for i in range(n):
        q = SimpleQueue()
        t = Thread(target=shuffler, args=(data, sdata, q))
        t.daemon = True
        activity.append([t, q])


def clear():
    if sys.platform == 'linux':
        os.system('clear')
    else:
        os.system('cls')


def initialise():
    global stime
    global sdir
    sdir+=strftime('/Records/%Y%m%d%H%M%S')
    if not(os.path.exists('./Records')): os.mkdir('Records')
    os.mkdir(sdir)
    stime = time()
    for i in activity:
        i[0].start()


#main
os.system('echo on')
print('\033[33mString Shuffler Test 2')
print('Powered By DAWN/Experiments\033[0m\n')
print(ctime())
print(about)
data = list(input('Enter string: '))
n = int(input('Number of threads: '))
print(data, '\n')
sleep(2)
sdata = data.copy()
shuffle(sdata)
constructor(data, sdata)
initialise()
while 1:
    k = k+1 if k < 3 else 0
    rdata = [i[1].get() for i in activity]
    print('\033[33mshuffler 1.5.0')
    print('A Probability simulation program for obtaining the same combination after shuffling a string')
    print('\nShuffling {}> [{}]\n\n\033[0m'.format(data, lIcon[k]))
    for i in range(0,n,1):
        if i % 5 == 0 and i != 0 and i != 1: print('\n')
        print('\033[0mT{}:'.format(i+1), rdata[i], end='| ', flush=True)
    if int(time()-stime) > 60: print('\n\n\033[36mTime taken:', round((time()-stime)/60, 2), 'minutes\033[0m\n')
    else: print('\n\n\033[36mTime taken:', round(time()-stime, 2), 'seconds\033[0m\n')
    sleep(0.01)
    print('\n\n\033[32mDAWN/Experiments')
    clear()
    if all(['\033[32mSuccess' == i[:12] for i in rdata]):
        t = time()
        print('\a', end='')
        killAllThreads = True
        tdata,fhit,lhit = optimize(rdata)
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
