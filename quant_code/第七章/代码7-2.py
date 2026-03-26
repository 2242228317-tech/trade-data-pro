import  threading
threading.enumerate()
threading.active_count()

def thread_job1():
    print('This is a thread of %s' % threading.current_thread())

def main():
    thread = threading.Thread(target=thread_job1,)   # 定义线程 
    thread.start()  # 让线程开始工作
    
if __name__ == '__main__':
    main()
print(threading.active_count())
threading.enumerate()

import threading
import time

def thread_job():
    print("S1 start\n")
    for i in range(5):
        time.sleep(1) # 任务间隔0.1s
    print("S1 finish\n")

added_thread = threading.Thread(target=thread_job, name='T1')
added_thread.start()
print("all done\n")

import threading
import time

def thread_job():
    print("S1 start\n")
    for i in range(5):
        time.sleep(1) # 任务间隔0.1s
    print("S1 finish\n")

added_thread = threading.Thread(target=thread_job, name='S1')
added_thread.start()
added_thread.join()
print("all done\n")

import threading
import time

def thread_job():
    print("S1 start\n")
    for i in range(5):
        time.sleep(1) # 任务间隔0.1s
    print("S1 finish\n")

added_thread = threading.Thread(target=thread_job, name='S1')
added_thread.start()
added_thread.join()
print("all done\n")

def S1_job():
    print("S1 start\n")
    for i in range(5):
        time.sleep(1)
    print("S1 finish\n")

def S2_job():
    print("S2 start\n")
    for i in range(10):
        time.sleep(0.1)
    print("S2 finish\n")

thread_1 = threading.Thread(target=S1_job, name='S1')
thread_2 = threading.Thread(target=S2_job, name='S2')
thread_1.start() # 开启T1
thread_2.start() # 开启T2
print("all done\n")

thread_1 = threading.Thread(target=S1_job, name='S1')
thread_2 = threading.Thread(target=S2_job, name='S2')
thread_1.start() # 开启T1
thread_2.start() # 开启T2
thread_1.join() # notice the difference!
thread_2.join() # notice the difference!
print("all done\n")


