import time

def print_local_time():
    local_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    print(local_time)
