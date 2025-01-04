import time
from subprocess import call

call("python","bot\\test.py")
time.sleep(5)
call("python","music.py")
call("python","webserver.py")