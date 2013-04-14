import datetime
import random

Servers = [('tile-5-1',8080),('tile-4-1',8080),('tile-3-1',8080)]
C2Server = "http://0.0.0.0:1234/"
C3Server = "http://0.0.0.0:4321/"
#C2Server = "http://vvnas00:9909/"
#C3Server = "http://rocksvv.cs.uit.no:9909/?"

imageCacheSize = 50
ccCacheSize = 50000

def getRandomServer():
	return Servers[random.randint(0,len(Servers))]

def roundTime(dt=None, roundTo=60):
   """Round a datetime object to any time laps in seconds
   dt : datetime.datetime object, default now.
   roundTo : Closest number of seconds to round to, default 1 minute.
   Author: Thierry Husson 2012 - Use it as you want but don't blame me.
   """
   if dt == None : dt = datetime.datetime.now()
   seconds = (dt - dt.min).seconds
   # // is a floor division, not a comment on following line:
   rounding = (seconds+roundTo/2) // roundTo * roundTo
   return dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)

   
   