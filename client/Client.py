'''
Created on Apr 8, 2013

@author: Simon
'''
import httplib, pygame, StringIO, thread, argparse, time, random, datetime
from pygame.locals import *
from miniboids import *



class Client():
    def __init__(self):
        self.BASE_URL = "129.242.22.192"
        self.PORT = 8080
        
        self._setup_menu()
        
        self.screen = None
        
        self.running = True
        
        self.image = None
        self.font = None
        
        self.fifteenMinutes = datetime.timedelta(minutes=15)
        
        self.mode = " "
        self.cloude = 0.0
    
    def start(self, auto = False):
        thread.start_new_thread(self.display, ())
        #self.display()
        if auto:
            self.autoTest()
        else:
            self.run()
            
    def autoTest(self):
        print "AutoTest"
        
        while(self.running):
            self.mode = "AUTO TEST"
            sleep = random.randrange(0, 5)
            for x in range(0, sleep+1):
                self.mode = "AUTO TEST: Sleep: "+str(sleep-x)+" sec"
                time.sleep(1)
            
            #self.getCloudValue("2003/03/22/0115")
            self.smoothScrool("2003/03/22/0115", "2003/03/22/0400")
            
            
                
    def run(self):
        print "manual mode"
        
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
        
        boids = []
        for x in range(random.randrange(10, 30)):        
            boids.append(Boid(self.screen))
        
        
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
            time_passed = clock.tick(100)
            time_passed_seconds = time_passed / 1000.0
            
            if self.image != None:
                self.screen.blit(self.image, (0, 0))
            
            for boid in boids:
                boid.update_vectors(boids,[], [])
                boid.move(time_passed_seconds, self.screen)
                    
                boid.draw(self.screen)
            
            
            
            if self.font != None:
                self.screen.blit(self.fontType.render(str(self.font), 0, (255,0,0)), (40,500))
                
            if self.cloude != None:
                self.screen.blit(self.fontType.render("Value: "+ str(self.cloude), 0, (255,0,0)), (40,80))
            
            self.screen.blit(self.fontType.render(str(self.mode), 0, (255,0,0)), (40,40))
            
            
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
        startDate = datetime.datetime.strptime(timeStart, "%Y/%m/%d/%H%M")
        endDate = datetime.datetime.strptime(timeEnd, "%Y/%m/%d/%H%M")
        
        while (startDate < endDate):
            startDate = startDate + self.fifteenMinutes
            print startDate
            self.getCloudValue(startDate.strftime("%Y/%m/%d/%H%M"))
                                     
        
            
    def getCloudValue(self, time):
        try:
            #time = "/2003/03/22/0115"#time
            
            date = datetime.datetime.strptime(time, "%Y/%m/%d/%H%M")
            
            #date = date + (random.randrange(0, 100)*self.fifteenMinutes)
            
            self.mode = "Gets date:" + time
            
            print date.strftime("/%Y/%m/%d/%H%M")
            msg = self.Get(date.strftime("/%Y/%m/%d/%H%M"))
        
            print msg.status, msg.reason
            
            if msg.status == 200:
                self.mode = "Got picture"
                
                jpeg_data = msg.read()
                
                buff = StringIO.StringIO()
                buff.write(jpeg_data)
                buff.seek(0)
                
                self.image = pygame.image.load(buff)
                self.font = time
            
            elif msg.status == 303:
                self.mode = "GOT REDIRECT"
            
            elif msg.status == 400:
                self.mode = "SERVER ERROR BAD REQUEST"
                
            elif msg.status == 404:
                self.mode = "SERVER ERROR DATE NOT FOUND"
                self.image = None
                self.font = "DATE NOT FOUND"
                
            else:
                self.mode = "SERVER ERROR"
                 
            
            
            
            #with open('out.jpg', 'wb') as out_file:
            #    out_file.write(jpeg_data)
   
        except:
            print "Client Error"
            self.mode = "CLIENT ERROR"
            self.font = "CLIENT COLD NOT CONNECT"
            self.cloude = None
            self.image = None
        
    def _setup_menu(self):
        self.help = """Cloud commands:
        Help: help, h, -h
        Exit: exit, e, -e
        Get cloud value:
            Random: c
            Single: c yyyy/mm/dd/hhmm
            """
        
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--auto", help = "run client in Auto mode", action = 'store_true')

    args = parser.parse_args()
    
    client = Client()
    client.start(args.auto)
    print "Exit program"
    
    
    