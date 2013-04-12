import urllib2
import Image
import cStringIO
import collections
from config import *
from limitedSizeDict import LimitedSizeDict


class Cache():
	"""
	An in memory cache wrapper. Responsible to get the external data, only meant to be used for the Serverfrontend
	"""
	def __init__(self, imageCacheSize = 50, ccCacheSize = 50000):
		self.ildict = LimitedSizeDict(imageCacheSize)
		self.cldict = LimitedSizeDict(ccCacheSize)
		self.ilDictHitMiss = collections.deque(maxlen=100)
		self.clDictHitMiss = collections.deque(maxlen=100)

	def calculateCloudiness(self, image):
		"""
		Calculates the cloudiness in a image in %, if something went wrong -1 is instead returned
		Formula given by the assignment text
		"""
		
		try:
			
			buff = cStringIO.StringIO()
			buff.write(image)
			buff.seek(0)
			img = Image.open(buff)

			pix = img.load()
			
			Nbw = 0;
			N = 0; 
			Nbright = 0; 
			CC = 0.0
			
			for i in xrange(0,626):
				for j in xrange(0,266):
					r,g,b = pix[i, j]
					if( ( r + b + g ) > 160 ): 
						Nbright += 1
					if ( b > ( (r + g) / 1.9 ) ):
						Nbw += 1
					else:
						N+=1
			if ( Nbright > ( 626*266 )*0.4 ):
				CC = 100.0 - Nbw*100.0/(626*266)
			else:
				CC = 0.0 
				
			
			return CC 
		except IOError:
			print "cannot convert", infile
			return -1

	def getImageAndCloudniess(self,date):
		"""
		Function that gets the image and returns a tuple of the image and cloudiness if the image exists, if not -1
		"""
		if date in self.cldict:
			self.clDictHitMiss.append(1)
			return None, self.cldict[date], date
		

		image = self.getImage(date)
		if image == -1:
			return -1
		
		CC = self.calculateCloudiness(image)
		self.clDictHitMiss.append(0)
		self.cldict[date] = CC
		return (image,CC, date)
		
	def getImage(self, date):
		"""
		Returns the image from the image server
		"""
		if date in self.ildict:
			self.ilDictHitMiss.append(1)
			return self.ildict[date]
		try:
			response = urllib2.urlopen(C2Server+ date.strftime("%Y/%m/%d/wcam0_%Y%m%d_%H%M.jpg") )
			image = response.read()
			self.ildict[date] = image
			self.ilDictHitMiss.append(0)
			return image
		except Exception as e:
			print e
			print "ERROR: Could not connect to the server or the image is not there"
			return -1
	



if __name__ == '__main__':
	cache = Cache()
	date = datetime.datetime.strptime("/2003/03/22/0600", "/%Y/%m/%d/%H%M")
	img = cache.getImage(date)
	print cache.calculateCloudiness(img)