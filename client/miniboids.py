import pygame
import math
import time
import random
from pygame.locals import*
from config import *


screen_res = (704, 576)#(SCREEN_WIDTH, SCREEN_HEIGHT)


class Vector2D:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
	def __repr__(self):
		return "Vector(%s, %s)" % (self.x, self.y)
		
	def __add__(self, b):
		return Vector2D(self.x + b.x, self.y + b.y)
	
	def __sub__(self, b):
		return Vector2D(self.x - b.x, self.y - b.y)
	
	def __mul__(self, b):
		if type(b) == type(1.0):
			return Vector2D(self.x * b, self.y * b)
		raise "Can't do that yet"
	
	def __div__ (self, b):
		return Vector2D(self.x / b.x, self.y / b.y)
	
	def __abs__(self):
		return (abs(self.x), abs(self.y))
	
	def magnitude(self):
		return math.sqrt(self.x ** 2 + self.y ** 2)
	
	def normalized(self):
		m = self.magnitude()
		return Vector2D(self.x / m, self.y / m)
	
	def copy(self):
		return Vector2D(self.x, self.y)


class Boid(Vector2D):
	def __init__(self, screen):
		Vector2D.__init__(self, 0, 0)
		# Movement
		self.pos = Vector2D((screen.get_width()*random.random()), (screen.get_height()*random.random()))
		self.speed = Vector2D(100, 100)
		self.average_heading_flock = Vector2D(0, 0)
		self.avoid_collison_flock_member = Vector2D(0, 0)
		self.center_flock = Vector2D(0, 0)
		self.max_speed = 200.0
		self.min_speed = 120.0
		self.turn_speed = 23.8
		
		# Radius
		self.flock_radius = 70
		self.collision_radius = 15
		self.collision_radius_objects = 20
		self.collision_radius_other_boids = 25
		
		# Graphics
		self.radius = 4
		self.color = (0, 0, 255)
		self.color_in_flock = (255,255,255)
		self.color_not_in_flock = (0,0,255)
		self.tail_length = 10
		self.tail_stroke = 3
		
		# Status
		self.in_flock = False
		self.ignore_flock = False
	
	def update_vectors(self, boids, hoiks, objects):
		self.center_flock = Vector2D(0, 0)
		self.average_heading_flock = Vector2D(0, 0)
		self.avoid_collison_flock_member = Vector2D(0, 0)
		flock_members = 0
		collision_members = 0
		for other_boid in boids:
			if self.pos != other_boid.pos:
				dp1p2 = self.pos - other_boid.pos
				# Check for flock members
				if self.flock_radius + other_boid.radius >= dp1p2.magnitude():
					# Ignore flock if chased by hoik
					if not self.ignore_flock:
						self.center_flock = self.center_flock + other_boid.pos
					
					# Calculate average heading flock
					self.average_heading_flock = self.average_heading_flock + other_boid.speed
					flock_members += 1
					
					# Check for collision other boids
					if self.collision_radius_other_boids + other_boid.radius >= dp1p2.magnitude():
						collision_members += 1
						self.avoid_collison_flock_member = self.avoid_collison_flock_member + other_boid.pos
		
		# Flock behavior
		if flock_members != 0:
			self.in_flock = True
			# Ignore flock if chased by hoik
			if not self.ignore_flock:
				# Average center for flock
				self.center_flock.x = (self.center_flock.x / flock_members)
				self.center_flock.y = (self.center_flock.y / flock_members)
				self.center_flock.x = ((self.center_flock.x - self.pos.x)/40)
				self.center_flock.y = ((self.center_flock.y - self.pos.y)/40)
			
			# Average heading for flock
			self.average_heading_flock.x = (self.average_heading_flock.x / flock_members)
			self.average_heading_flock.y = (self.average_heading_flock.y / flock_members)
			self.average_heading_flock.x = ((self.average_heading_flock.x - self.speed.x)/40)
			self.average_heading_flock.y = ((self.average_heading_flock.y - self.speed.y)/40)
		else:
			self.in_flock = False
			
		# Flock collision
		if collision_members != 0:
			# Preventing collision course with other flock members
			self.avoid_collison_flock_member.x = (self.avoid_collison_flock_member.x / collision_members)
			self.avoid_collison_flock_member.y = (self.avoid_collison_flock_member.y / collision_members)
			self.avoid_collison_flock_member.x = (self.pos.x - self.avoid_collison_flock_member.x)
			self.avoid_collison_flock_member.y = (self.pos.y - self.avoid_collison_flock_member.y)
		
		# Calculate color for boid.(If not in flock turn to color_not_in_flock)
		if self.in_flock:
			self.color = self.color_in_flock
		elif not self.in_flock:
			self.color = self.color_not_in_flock
			



				
	def move(self, time_passed_seconds, screen):
		# Calculate new speed vector
		self.speed = self.speed + self.center_flock + self.average_heading_flock + self.avoid_collison_flock_member
		
		# If Boids moves to slow speed them up
		if ((abs(self.speed.x) + abs(self.speed.y)/2)) < self.min_speed:
			self.speed = self.speed * 1.3 
		
		# If Boids moves to fast slow them down
		if ((abs(self.speed.x) + abs(self.speed.y)/2)) > self.max_speed:
			self.speed = self.speed * 0.9 
		
		distx = time_passed_seconds * self.speed.x
		disty = time_passed_seconds * self.speed.y
		self.pos.x = self.pos.x + distx
		self.pos.y = self.pos.y + disty
		
		# Preventing collision wall
		if self.pos.x <= 0 + self.collision_radius:
			if self.speed.x < self.max_speed:
				self.speed.x += self.turn_speed
		if self.pos.y <= 0 + self.collision_radius:
			if self.speed.y < self.max_speed:
				self.speed.y += self.turn_speed
		if self.pos.x >= screen.get_width() - self.collision_radius:
			if self.speed.x > -self.max_speed:
				self.speed.x -= self.turn_speed
		if self.pos.y > screen.get_height() - self.collision_radius:
			if self.speed.y > -self.max_speed:
				self.speed.y -= self.turn_speed
		
		# If  actual collision to the wall
		if self.pos.x <= 0 + self.radius:
			self.speed.x = abs(self.speed.x)

		if self.pos.y <= 0 + self.radius:
			self.speed.y = abs(self.speed.y)

		if self.pos.x >= screen.get_width() - self.radius:
			self.speed.x = -abs(self.speed.x)

		if self.pos.y > screen.get_height() - self.radius:
			self.speed.y = -abs(self.speed.y)
		
	# Draw tail
	def draw_vec_from_self(self, screen):
		tail = self.speed.normalized()
		pygame.draw.line(screen, self.color, (self.pos.x, self.pos.y), (self.pos.x - tail.x * self.tail_length, self.pos.y - tail.y * self.tail_length), self.tail_stroke)
	
	# Draw self
	def draw(self, screen):
		self.draw_vec_from_self(screen)
		pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)
		


	
