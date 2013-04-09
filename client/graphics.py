# -*- coding: utf-8 -*-
import pygame, os, random
from config import *
import thread
import time
from miniboids import *
from mutex import *

class Graphics(object):
	def __init__(self, dieFunction, number_of_segments):
		'''
		constructor
		'''
		self.dieFunction = dieFunction
		self.num_segs = number_of_segments
		self.mutex = Mutex()

	def run(self):
		'''
		starts the simple boids simulation
		'''
		pygame.display.init()
		pygame.font.init()
		x = random.randint(0, 1024 - SCREEN_WIDTH)
		y = random.randint(0, 800 - SCREEN_HEIGHT)
		os.environ['SDL_VIDEO_WINDOW_POS'] = str(x) + ',' + str(y)
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE, 32)
		s = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.SRCALPHA)   # per-pixel alpha
		
		# How many boids to simulate
		boids = []
		for x in range(random.randrange(5, 10)):        
			boids.append(Boid(self.screen))
	
			
		clock = pygame.time.Clock()
		SCREEN_COLOR = (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255))
		
		myFont = pygame.font.SysFont("None", 300)
		smallfont = pygame.font.SysFont("None", 30)
		color = ((SCREEN_COLOR[0] + 123)%255 , (SCREEN_COLOR[1] + 123) % 255 , (SCREEN_COLOR[2] + 123)%255 )
		
		#waiting for the number of segments to stabilize them selves
		time.sleep(10)
		thread.start_new_thread(self.mutex.run,(self.num_segs,))
		
		while(RUNNING):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.dieFunction()
					os._exit(0)
			
			pygame.draw.rect(self.screen, (SCREEN_COLOR), (0, 0, self.screen.get_width(), self.screen.get_height()))
			time_passed = clock.tick(30) # limit to x FPS 
			time_passed_seconds = time_passed / 1000.0

			
			if self.mutex.hasLock:
				self.screen.blit(myFont.render(str(int(self.num_segs())), 0, (color)), (10,10))
			
				self.screen.blit(smallfont.render(str(self.mutex.getlamportClock()), 0, (color)), (200,10))
				self.screen.blit(smallfont.render(str(self.mutex.hasLock), 0, (color)), (200,40))
			
			# Update boids
			for boid in boids:
				if self.mutex.hasLock:
					boid.update_vectors(boids,[], [])
					boid.move(time_passed_seconds, self.screen)
					
				boid.draw(self.screen)
					
			if not self.mutex.hasLock:
				s.fill((0,0,0,175))                         # notice the alpha value in the color
				self.screen.blit(s, (0,0))
			#pygame.draw.rect(self.screen, (0,0,0, 150), (0, 0, self.screen.get_width(), self.screen.get_height()))
				self.screen.blit(myFont.render(str(int(self.num_segs())), 0, (color)), (10,10))
				self.screen.blit(smallfont.render(str(self.mutex.getlamportClock()), 0, (color)), (200,10))
				self.screen.blit(smallfont.render(str(self.mutex.hasLock), 0, (color)), (200,40))
			pygame.display.update()



def num():
	'''
	Method for testing
	'''
	return 1            
		
if __name__ == "__main__":
	graf = Graphics(1, num)
	graf.run()
