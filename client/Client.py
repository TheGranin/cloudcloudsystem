'''
Created on Apr 8, 2013

@author: Simon
'''
import httplib, pygame, StringIO, thread
from pygame.locals import *



class Client():
    def __init__(self):
        self.BASE_URL = "129.242.22.192"
        self.PORT = 8080
        
        self._setup_menu()
        
          
        self.screen = None
        
        self.running = True
        
        self.image = None
        self.font = None
        
        self.mode = " "
        self.cloude = 0.0
        
        
        #self.getCloudValue("")
    
    def start(self):
        thread.start_new_thread(self.display, ())
        #self.display()
        self.run()
        
    def run(self):
        while(self.running):
            self.mode = "Manual: Waits for command"
            cmd = raw_input('CMD: ')
            cmd = cmd.split()
            
            if cmd[0] in ['exit', 'e', '-e']:
                self.running = False
            else:
                self.command(cmd)
            
    def display(self):
        pygame.init()  
        clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((704, 576))
        self.fontType = pygame.font.SysFont("None", 40)
        
        while (self.running):
            for event in pygame.event.get():
                    if event.type == QUIT:
                        self.running = False
                        return
                    elif event.type == KEYDOWN:          
                        if event.key == K_ESCAPE:
                            self.running = False
                            return
                        
            pygame.draw.rect(self.screen, (3,3,3), (0, 0, self.screen.get_width(), self.screen.get_height()))
            clock.tick(20)
            
            if self.image != None:
                self.screen.blit(self.image, (0, 0))
            
            if self.font != None:
                self.screen.blit(self.fontType.render(str(self.font), 0, (255,0,0)), (40,500))
            
            self.screen.blit(self.fontType.render(str("MODE: "+self.mode), 0, (255,0,0)), (40,40))
            self.screen.blit(self.fontType.render("Value: "+ str(self.cloude), 0, (255,0,0)), (40,80))
            
            pygame.display.flip()
                
    
    def Get(self, path):
        conn = httplib.HTTPConnection(self.BASE_URL, self.PORT)        
        conn.request("GET", path)
        response = conn.getresponse()
        conn.close()
        return response        
             
    def command(self, cmd):
        method = cmd[0]
        if method in ["cloud", "c", "-c"]:
            print "Getting cloud value"
            # TODO get cloud
            self.getCloudValue("a")#cmd[1])
            
        
        elif method in ["help", "h", "-h"]:
            print self.help
    
    def smoothScrool(self, timeStart, timeEnd):
        pass
            
    def getCloudValue(self, time):
        #try:
            time = "/2003/03/22/0115"#time
            
            self.mode = "Gets date:" + time
            
            msg = self.Get(time)
        
            print msg.status, msg.reason
            print msg.status
            #if msg.status[0] == 200:
            #    self.mode = "Got picture"
            
            jpeg_data = msg.read()
        
            buff = StringIO.StringIO()
            buff.write(jpeg_data)
            buff.seek(0)
            
            self.image = pygame.image.load(buff)
            self.font = time
            
            
            
            #with open('out.jpg', 'wb') as out_file:
            #    out_file.write(jpeg_data)
   
        #except:
        #    print "Client Error"
        
    def _setup_menu(self):
        self.help = """Cloud commands:
        Help: help, h, -h
        Exit: exit, e, -e
        Get cloud value:
            Random: c
            Single: c yyyy/mm/dd/hhmm
            """
        
            
if __name__ == '__main__':
    client = Client()
    client.start()
    print "Exit program"
    
    
    