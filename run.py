
from subprocess import call
import thread
from config import *
#import spur

#call(["python", "Serverfrontend.py"])

#def ssh(tile):
	#shell = spur.SshShell(hostname="rocksvv.cs.uit.no", username="inf3200", password="ADSpassord")
	#shell.run(["ssh", tile])
	#return shell

def run_server1():
	#call(["python", "Serverfrontend.py", "-p " + str(Servers[0][1]), "-s 1"])
	call(["ssh", "tile-5-1"])
	#shell = ssh("tile-5-1")
	call(["ls"])
def run_server2():
	call(["python", "Serverfrontend.py", "-p " + str(Servers[1][1]), "-s 2"])
def run_server3():
	call(["python", "Serverfrontend.py", "-p " + str(Servers[2][1]), "-s 3"])
	
thread.start_new_thread(run_server1, ())
#thread.start_new_thread(run_server2, ())
#thread.start_new_thread(run_server3, ())


try:
	while(True):
		pass
except Exception:
	print "Complete"
