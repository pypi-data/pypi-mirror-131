import time

def TimingFunction(timing):
    def Function_A(func):
        def Function_B(*args,**kwargs):
            while True:
                if int(time.mktime(time.strptime(timing, "%Y-%m-%d %H:%M:%S"))) <= int(time.time()):
                    return func(*args,**kwargs)
                time.sleep(1)
        return Function_B
    return  Function_A