import os, time
import threading

'''
    ある関数ないしメソッドの処理を行なったときに発生する処理時間を計測
    規定時間を超えたときに自動で処理を中断させるため、threadingライブラリを利用
'''

class TimeChecker:
    elapsed_time = float(0)
    def __init__(self,func,set_time=2.10):
        self.set_time = set_time
        self.thread_func = threading.Thread(target=func,daemon=True)

    def start_timer(self):
        start_time = time.perf_counter()

        self.thread_func.start()
        self.thread_func.join(timeout=self.set_time*1.5)

        self.elapsed_time = time.perf_counter() - start_time
        print(self.elapsed_time)


def longtime():
    for n in range(10):
        pass
    return 

def main():
    timer = TimeChecker(func=longtime)
    timer.start_timer()

    if timer.elapsed_time > timer.set_time:
        print("TLE")
    else:
        print("NOT TLE")

    hogetimer = TimeChecker(lambda:[i for i in range(10**6)])
    hogetimer.start_timer()

if __name__ == "__main__":
    main()

