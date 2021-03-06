from pygame.locals import *
import pygame
from  copy import deepcopy
import os
#from cache import Cache 

class Display():
	"""
	Code to display information on the server
	"""
	def __init__(self):
		self.running = True
		self.started = False
		self.avgIM = 0
		self.avgCC = 0
		self.prosent = 0
	def caclucateAvg(self, cache):
		cc = 0
		im = 0
		clDictHitMiss = deepcopy(cache.clDictHitMiss)
		ilDictHitMiss = deepcopy(cache.ilDictHitMiss)
		if len(clDictHitMiss) < 100 or len(ilDictHitMiss) < 100:
			self.prosent = (len(clDictHitMiss) + len(ilDictHitMiss))/2
			return cc,im
		self.started = True
		for i in clDictHitMiss:
			im += i
		for i in ilDictHitMiss:
			cc += i
		return cc, im
			
	def run(self, cache, timer, timer2, timer3):
		try:
			pygame.display.init()
			pygame.font.init()
			clock = pygame.time.Clock()
			os.environ['SDL_VIDEO_WINDOW_POS'] = str(0) + ',' + str(0)
			self.screen = pygame.display.set_mode((300, 400))
			self.fontType = pygame.font.SysFont("None", 40)
			self.fontType2 = pygame.font.SysFont("None", 20)
			self.fontType3 = pygame.font.SysFont("None", 30)
			while (self.running):
				for event in pygame.event.get():
						if event.type == QUIT:
							self.running = False
							os._exit(0)
							return
						elif event.type == KEYDOWN:          
							if event.key == K_ESCAPE:
								self.running = False
								os._exit(0)
								return
						
				pygame.draw.rect(self.screen, (3,3,3), (0, 0, self.screen.get_width(), self.screen.get_height()))
				time_passed = clock.tick(10)
				time_passed_seconds = time_passed / 1000.0
				
				if not self.started:
					self.screen.blit(self.fontType.render("Gathering Data..."+str(self.prosent) + "%", 0, (255,0,0)), (10,90))
				
				
					
				self.avgIM, self.avgCC = self.caclucateAvg(cache)
				self.screen.blit(self.fontType.render("Avg Image Hit: "+ str(self.avgIM) +"%", 0, (255,255,0)), (10,10))
				self.screen.blit(self.fontType.render("Avg Cloud Hit: "+ str(self.avgCC) +"%", 0, (255,255,0)), (10,50))
				
				deepTimer = deepcopy(timer)
				resTime, maxTime, avgTime = deepTimer.getValues()
				
				self.screen.blit(self.fontType3.render("Response Time:", 0, (255,255,0)), (10,160))
				self.screen.blit(self.fontType2.render(str("CUR: %4dms  Max: %4dms"  % (resTime, maxTime)), 0, (255,255,0)), (10,190))
				
				self.screen.blit(self.fontType2.render(str("AVG(%d): %4dms"%(timer.getNumSamples(), avgTime)), 0,(255,255,0)), (10,210))
				
				
				
				
				deepTimer2 = deepcopy(timer2)
				resTime, maxTime, avgTime = deepTimer2.getValues()
		
				self.screen.blit(self.fontType3.render("CloudValue calc Time:", 0, (255,255,0)), (10,240))
				self.screen.blit(self.fontType2.render(str("CUR: %4dms  Max: %4dms"  % (resTime, maxTime)), 0, (255,255,0)), (10,270))
				self.screen.blit(self.fontType2.render(str("AVG(%d): %4dms"%(timer.getNumSamples(), avgTime)), 0,(255,255,0)), (10,290))
				
				
				deepTimer3 = deepcopy(timer3)
				resTime, maxTime, avgTime = deepTimer3.getValues()
				self.screen.blit(self.fontType3.render("C2 Server Time:", 0, (255,255,0)), (10,320))
				self.screen.blit(self.fontType2.render(str("CUR: %4dms  Max: %4dms"  % (resTime, maxTime)), 0, (255,255,0)), (10,350))
				
				self.screen.blit(self.fontType2.render(str("AVG(%d): %4dms"%(timer.getNumSamples(), avgTime)), 0,(255,255,0)), (10,370))
				

				pygame.display.flip()
		except Exception as e:
			print "--------------------ERRROR ON PYGAME----------------------"
			print e

