import fcntl

def ac_lock(lock_file: str):
    lock_fd = open(lock_file, "w")
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        print("Lock acquired")
        return lock_fd
    except BlockingIOError:
        return None
        
def re_lock(lock_file: str):
    lock_fd = open(lock_file, 'w')
    fcntl.flock(lock_fd, fcntl.LOCK_UN)
    print("Lock released")
    lock_fd.close()