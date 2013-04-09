import argparse
import datetime

from cache import *

import web
        
urls = (
	'/(.*)', 'index'
)

cache = Cache(imageCacheSize, ccCacheSize)


class index:
	"""
	Class for server communication, will handle any incomming request
	"""


	def GET(self, path):
		"""
		Handler for the GET requests
		"""
	
		work = self.reqWorkResp()
		if work == "YES":
			
			try:
				date = datetime.datetime.strptime(path, "%Y/%m/%d/%H%M")
				date = roundTime(date,roundTo=15*60)
			except Exception as e:
				print e
				raise web.badrequest()
			
			tupleData = self.getBestImage(date)

			if tupleData == -1:
				raise web.notfound()

				
			image, cloudValue = tupleData
			print "CC =", cloudValue
	

			web.header("Content-Type","jpg")
			web.header('x-CC',cloudValue)
			print "Request complete"
			return image
			
			
		else:
			#Redirect the client
			#UPDATE IN FUTURE
			#self.send_header('Location','http://0.0.0.0:'+ ServersPorts[random.randint(0,2)])
			raise web.seeother("http://vg.no")
		
	def reqWorkResp(self):
		"""
		Request an answer from the C3 server
		"""
		response = urllib2.urlopen(C3Server)
		return response.read()


		
	def getImageAndCloudniess(self,date):
		"""
		Function that gets the image and returns a tuple of the image and cloudiness if the image exists, if not -1
		"""
		image = cache.getImage(date)
		if image == -1:
			return -1
		
		CC = cache.calculateCloudiness(image)
		return (image,CC)

	def getBestImage(self, date):
		"""
		Finds the image that best represent the cloudiness over a hour and the meidan over that cloudiness 
		"""
		pictures = []
		fifteenMinutes = datetime.timedelta(minutes=15)
		median = 0.0
		
		tupleData = self.getImageAndCloudniess(date) 
		if tupleData == -1:
			return -1
		
		pictures.append(tupleData)
		
		for x in [-2,2,-1,1]:
			tmpdate = date + (x * fifteenMinutes)
			tupleData = self.getImageAndCloudniess(tmpdate) 
			if tupleData == -1:
				continue

			pictures.append(tupleData)
			median += tupleData[1]

		median = median/len(pictures)
		bestPicture = ""
		bestValue = 100.0
		for image in pictures:
			if abs(image[1] - median) < bestValue:
				bestPicture = image[0]
				bestValue = image[1]
				
		return (bestPicture, median)
		



		
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-s", type = int ,help = "Which server number are you", default = "1")
	args = parser.parse_args()

	app = web.application(urls, globals())
	app.run()   
	
