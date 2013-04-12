'''
Created on Apr 8, 2013

@author: Simon
'''
import httplib, pygame, cStringIO, thread, argparse, time, random, datetime, Timer
from pygame.locals import *
from miniboids import *

class SETTINGS():
    MAX_REDIRS = 2
    START_ADDRESS = "129.242.22.192"
    START_PORT = 8080
    
    AVG_SAMPLES = 10


class TYPES():
    REQ_TYPE_DATE = 0
    REQ_TYPE_SEQ = 1
    
    

        

class Client():
    def __init__(self):
        # Communication
        self.BASE_URL = SETTINGS.START_ADDRESS
        self.PORT = SETTINGS.START_PORT
        
        # GRAPHICS
        self.screen = None
        self.running = True
        self.image = None
        self.font = None
        self.mode = " "
        self.cloude = 0.0
        
        
        self.timer = Timer.Timer(SETTINGS.AVG_SAMPLES)
        
        
        self.resTime = 0
        self.maxTime = 0
        self.avgTime = 0
        
        self.fifteenMinutes = datetime.timedelta(minutes=15)
        
        self.redirects = 0
        self.maxRedirs = SETTINGS.MAX_REDIRS
        
        self._setup_menu()
        
    
    def start(self, auto = False):
        thread.start_new_thread(self.display, ())
        if auto:
            self.autoTest()
        else:
            self.run()
            
    def autoTest(self):        
        while(self.running):
            sleep = random.randrange(0, 5)
            for x in range(0, sleep+1):
                self.mode = "AUTO TEST: Sleep: "+ str(sleep-x)+" sec"
                time.sleep(1)
            
            requestType = self._getRandReqType()
            if requestType == TYPES.REQ_TYPE_DATE:
                self.autoGet()
            elif requestType == TYPES.REQ_TYPE_SEQ:
                self.autoScrool()
    
    def _getRandReqType(self):
        range = random.randrange(0, 101)
        if range > 50:
            return TYPES.REQ_TYPE_SEQ
        else:
            return TYPES.REQ_TYPE_DATE
            
    def _randDate(self):
        year = 2003
        month = 3#random.randrange(1, 12)
        day = 22#random.randrange(1, 28)
        hour = random.randrange(1, 23)
        minute = random.randrange(0, 59)
        minute -= minute % 15
        return "%d/%02d/%02d/%02d%02d" % (year, month, day, hour, minute)
        
    def autoGet(self):
        numGets = random.randrange(1, 20)
        for x in range(1, numGets+1):
            self.mode = str("RANDOM GET: %d of total %d images" % (x, numGets))
            self.getCloudValue(self._randDate())
              
    def autoScrool(self):
        year = 2003
        month = 3#random.randrange(1, 12)
        day = 22#random.randrange(1, 28)
        hour = random.randrange(1, 23)
        minute = random.randrange(0, 59)
        minute -= minute % 15 
        start = "%d/%02d/%02d/%02d%02d" % (year, month, day, hour, minute)
        
        scroll_intervall = random.randrange(1, 4)
        
        if scroll_intervall == 4:
            day = random.randrange(day, 28)
        
        hour = random.randrange(hour, 23)
        minute = random.randrange(minute, 59)
        minute -= minute % 15 
        end = "%d/%02d/%02d/%02d%02d" % (year, month, day, hour, minute)
        
        self.smoothScrool(start, end, scroll_intervall)        
                
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
        pygame.display.init()
        pygame.font.init()
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
            time_passed = clock.tick(30)
            time_passed_seconds = time_passed / 1000.0
            
            if self.image != None:
                self.screen.blit(self.image, (0, 0))
            
            for boid in boids:
                boid.update_vectors(boids,[], [])
                boid.move(time_passed_seconds, self.screen)
                    
                boid.draw(self.screen)
            
            
            self.screen.blit(self.fontType.render(str(self.mode), 0, (255,0,0)), (40,40))
            
            if self.font != None:
                self.screen.blit(self.fontType.render(str(self.font), 0, (255,0,0)), (40,500))
                
            if self.cloude != None:
                self.screen.blit(self.fontType.render(str("Clouds: %.1f %%" % (self.cloude)), 0, (255,0,0)), (40,80))
            
            
            self.screen.blit(self.fontType.render(str("CUR: %4dms    Max: %4dms    AVG(%d): %4dms" % (self.resTime, self.maxTime, SETTINGS.AVG_SAMPLES, self.avgTime)), 0, (255,0,0)), (40,530))
            
            pygame.display.flip()
                
    
    def Get(self, path):
        conn = httplib.HTTPConnection(self.BASE_URL, self.PORT)        
        
        self.timer.startTimer()
        conn.request("GET", path)
        
        
        response = conn.getresponse()
        
        self.timer.stopTimer()
        
        self.resTime, self.maxTime, self.avgTime = self.timer.getValues()
        headerDict = self._headerToDict(response.getheaders())
        data = (response.status, response.read(), headerDict)
        conn.close()
        return data
    
    def _headerToDict(self, headers):
        dict = {}
        for header in headers:
            dict[header[0]] = header[1]
        return dict 
             
    def command(self, cmd):
        method = cmd[0]
        if method in ["cloud", "c", "-c"]:
            print "Getting cloud value"
            # TODO get cloud
            self.getCloudValue("a")#cmd[1])
            
        
        elif method in ["help", "h", "-h"]:
            print self.help
    
    def smoothScrool(self, timeStart, timeEnd, interval = 1):
        startDate = datetime.datetime.strptime(timeStart, "%Y/%m/%d/%H%M")
        endDate = datetime.datetime.strptime(timeEnd, "%Y/%m/%d/%H%M")
        
        while (startDate < endDate):
            self.mode = "SMOOTH SCROLL INT: " + str(interval * 15)+"min"
            startDate = startDate + (interval*self.fifteenMinutes)
            print startDate
            self.getCloudValue(startDate.strftime("%Y/%m/%d/%H%M"))
                                     
        
            
    def getCloudValue(self, time):
        try:
            #time = "/2003/03/22/0115"#time
            
            date = datetime.datetime.strptime(time, "%Y/%m/%d/%H%M")
            
            #date = date + (random.randrange(0, 100)*self.fifteenMinutes)
            
            #self.mode = "Gets date:" + time
            
            print date.strftime("/%Y/%m/%d/%H%M")
            
            status, data, headers = self.Get(date.strftime("/%Y/%m/%d/%H%M"))
        
            print headers        
            print status
            
            if status == httplib.OK:
                #self.mode = "Got picture"    
                jpeg_data = data
               
                buff = cStringIO.StringIO()
                buff.write(jpeg_data)
                buff.seek(0)
                
                self.image = pygame.image.load(buff)
                self.font = time
                self.cloude = float(headers['x-cc'])
            
            elif status == httplib.SEE_OTHER:
                self.font = "GOT REDIRECT"
                print "REDIRECT TO: ", headers["location"]
                self.redirects += 1
                if self.redirects >= self.maxRedirs:
                    print "Can't connect to server"
            
            elif status == httplib.BAD_REQUEST:
                self.font = "SERVER ERROR BAD REQUEST"
                
            elif status == httplib.NOT_FOUND:
                #self.mode = "SERVER ERROR DATE NOT FOUND"
                self.image = None
                self.font = "DATE NOT FOUND"
                
            else:
                print "STATUS IS", status 
                self.font = "SERVER ERROR"
                 
            
            
            
            #with open('out.jpg', 'wb') as out_file:
            #    out_file.write(jpeg_data)
   
        except Exception as e:

            print "Client Error"
            print e
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
    
    
    
