import argparse, thread
from cache import *
from display import *
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
			#TODO UPDATE IN FUTURE
			#self.send_header('Location','http://0.0.0.0:'+ ServersPorts[random.randint(0,2)])
			raise web.seeother("http://vg.no")
		
	def reqWorkResp(self):
		"""
		Request an answer from the C3 server
		"""
		response = urllib2.urlopen(C3Server)
		return response.read()


	def getBestImage(self, date):
		"""
		Finds the image that best represent the cloudiness over a hour and the meidan over that cloudiness 
		"""
		pictures = []
		fifteenMinutes = datetime.timedelta(minutes=15)
		median = 0.0
		
		tupleData = cache.getImageAndCloudniess(date) 
		if tupleData == -1:
			return -1
		
		pictures.append(tupleData)
		
		for x in [-2,2,-1,1]:
			tmpdate = date + (x * fifteenMinutes)
			tupleData = cache.getImageAndCloudniess(tmpdate) 
			if tupleData == -1:
				continue

			pictures.append(tupleData)
			median += tupleData[1]

		median = median/len(pictures)
		bestValue = 100.0
		for image in pictures:
			if abs(image[1] - median) < bestValue:
				tupleData = image
				bestValue = image[1]
		
		bestImage = tupleData[0]
		if bestImage == None:
			bestImage = cache.getImage(tupleData[2])
		return (bestImage, median)



		
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-s", type = int ,help = "Which server number are you", default = "1")
	args = parser.parse_args()

	display = Display()
	thread.start_new_thread(display.run, (cache, ))
	app = web.application(urls, globals())
	app.run()   
	
