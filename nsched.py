### Simple scheduler scrypt to execute a function


import sched
import time

from dump import fetch_bond_data



scheduler = sched.scheduler(time.time, time.sleep)

def get_data(name):
        fetch_bond_data()
        print 'EVENT:', time.time(), name

print 'START:', time.time()

secondsinday=60

for i in range(0,4):
        scheduler.enter(10*i+10, 1, get_data, (str(i)))

scheduler.run()
