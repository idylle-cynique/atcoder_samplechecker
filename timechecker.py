import os, time
import threading

'''
    ある関数ないしメソッドの処理を行なったときに発生する処理時間を計測
    規定時間を超えたときに自動で処理を中断させるため、threadingライブラリを利用
'''

class TimeChecker:
    elapsed_time = float(0)
    def __init__(self,func,commandline,set_time=2.10):
        self.set_time = set_time
        self.thread_func = threading.Thread(target=func, args=(commandline,), daemon=True)

    def start_timer(self):
        start_time = time.perf_counter()
        self.thread_func.start()
        self.thread_func.join(timeout=self.set_time)

        self.elapsed_time = time.perf_counter() - start_time
        print(self.elapsed_time)

def longtime(x):
    for n in range(x**9):
        pass
    return 

def main():
    timer = TimeChecker(func=longtime,commandline=5)
    timer.start_timer()

    if timer.elapsed_time > timer.set_time:
        print("TLE")
    else:
        print("NOT TLE")


if __name__ == "__main__":
    main()

