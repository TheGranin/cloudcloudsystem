from pygame.locals import *
import pygame
import os
#from cache import Cache 

class Display():
	def __init__(self):
		self.running = True
		self.started = False
		self.avgIM = 0
		self.avgCC = 0
		self.prosent = 0
	def caclucateAvg(self, cache):
		cc = 0
		im = 0
		if len(cache.clDictHitMiss) < 100 or len(cache.ilDictHitMiss) < 100:
			self.prosent = (len(cache.clDictHitMiss) + len(cache.ilDictHitMiss))/2
			return cc,im
		self.started = True
		for i in cache.clDictHitMiss:
			im += i
		for i in cache.ilDictHitMiss:
			cc += i
		return cc, im
			
	def run(self, cache, timer):
		try:
			pygame.display.init()
			pygame.font.init()
			clock = pygame.time.Clock()
			os.environ['SDL_VIDEO_WINDOW_POS'] = str(0) + ',' + str(0)
			self.screen = pygame.display.set_mode((300, 300))
			self.fontType = pygame.font.SysFont("None", 40)
			self.fontType2 = pygame.font.SysFont("None", 20)
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
				self.screen.blit(self.fontType.render("Avg Image Hit: "+ str(self.avgIM), 0, (255,0,0)), (10,10))
				self.screen.blit(self.fontType.render("Avg Cloud Hit: "+ str(self.avgCC), 0, (255,0,0)), (10,50))
				resTime, maxTime, avgTime = timer.getValues()
				self.screen.blit(self.fontType2.render(str("CUR: %4dms  Max: %4dms"  % (resTime, maxTime)), 0, (255,0,0)), (10,190))
				self.screen.blit(self.fontType2.render(str("AVG(%d): %4dms" % (timer.getNumSamples(), avgTime)), 0, (255,0,0)), (10,210))
				pygame.display.flip()
		except Exception as e:
			print "--------------------ERRROR ON PYGAME----------------------"
			print e

