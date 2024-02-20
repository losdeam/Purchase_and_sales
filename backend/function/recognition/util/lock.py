import os

def acquire_lock(script_path):
    lock_file  = script_path[:-3] + ".lock"
    try:
        # 尝试创建锁文件
        lock_fd = os.open(lock_file, os.O_CREAT | os.O_EXCL | os.O_RDWR)
        return lock_fd,lock_file
    except :
        # 锁文件已存在，表示脚本已在运行
        return None

def release_lock(lock_fd,lock_file):
    os.close(lock_fd)
    os.remove(lock_file)

