import os
import time

from define import BASE_DIR

class ScriptLock:
    def __init__(self, lock_name):
        self._lock_name = lock_name

    def get_lock_file_path(self):
        return '{}/lock/{}.LOCK'.format(BASE_DIR, self._lock_name)

    def check_lock(self):
        lock_file_path = self.get_lock_file_path()
        if os.path.isfile(lock_file_path):
            f = open(lock_file_path, mode='r+')
            t = f.readline()
            if int(time.time()) - int(t) > 600:
                self.release_lock()
                return False
            return True
        return False

    def acquire_lock(self):
        lock_file_path = self.get_lock_file_path()
        now = str(int(time.time()))
        f = open(lock_file_path, mode='w+')
        f.write(now)
        f.close()

    def release_lock(self):
        lock_file_path = self.get_lock_file_path()
        os.remove(lock_file_path)