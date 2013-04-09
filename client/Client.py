'''
Created on Apr 8, 2013

@author: Simon
'''
import httplib


class Client():
    def __init__(self):
        self.BASE_URL = "localhost"
        self.PORT = 8080
        
        self.help = """Cloud commands:
        Help: help, h, -h
        Exit: exit, e, -e
        Get cloud value:
            Random: c
            Single: c yy.mm.dd.hhmm
            """
        
    
    def Get(self, path):
        
        conn = httplib.HTTPConnection(self.BASE_URL, self.PORT)
        
        conn.request("GET", path)
        
        response = conn.getresponse()

        conn.close()
        
        return response        
        #print response.status, response.reason
        
        #data = response.read()
        
        #print data
    
    def run(self):
        while(True):
            cmd = raw_input('CMD: ')
            cmd = cmd.split()
            
            if cmd[0] in ['exit', 'e', '-e']:
                break
            else:
                self.command(cmd)
                
    def command(self, cmd):
        method = cmd[0]
        if method in ["cloud", "c", "-c"]:
            print "Getting cloud value"
            # TODO get cloud
            
        
        elif method in ["help", "h", "-h"]:
            print self.help
            
    def getCloudValue(self, time):
        msg = self.Get(time)
        print msg.status, msg.reason
            
if __name__ == '__main__':
    client = Client()
    client.run()
    print "Exit program"
    
    
    