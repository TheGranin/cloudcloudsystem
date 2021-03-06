'''
Created on Apr 12, 2013

@author: Simon
'''

import time

class ThreadSafeTimer():
	"""
	Simple class to keep track of time
	"""
	
	def __init__(self, sampleCount = 10):
		self.resTime = 0
		self.maxTime = 0
		self.avgTime = 0
		
		self.avgSamples = []
		self.sampleCount = sampleCount
		
		self.timer = 0
		self.lastTrack = 0
		self.numSamples = 0   
	def time(self, startTime, stopTime):
		trackTime = stopTime - startTime
		self._setMax(trackTime)
		self._newValueToAvg(trackTime)
		self.lastTrack = trackTime
        
	def _setMax(self, trackTime):
		if trackTime > self.maxTime:
			self.maxTime = trackTime
			
	def _newValueToAvg(self, trackTime):
		if len(self.avgSamples) > self.sampleCount:
			self.avgSamples.pop(0)
		else:
			self.numSamples += 1
			
		self.avgSamples.append(trackTime)
		
		
	def getNumSamples(self):
		return self.numSamples
		
	def calcAvg(self):
		numSamples = len(self.avgSamples)
		if (numSamples > 0):
			sampleAVG = 0
			for value in self.avgSamples:
				sampleAVG = sampleAVG + value
				
			return sampleAVG / numSamples
		return 0

	def getValues(self):
		return (self.lastTrack, self.maxTime, self.calcAvg())
		


if __name__ == '__main__':
	timer = Timer()        
	timer.time(time.time() * 1000, time.time() * 1000 + 3)
	print timer.calcAvg()
