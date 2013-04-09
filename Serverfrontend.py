import argparse
import BaseHTTPServer
import SocketServer

from cache import *


cache = Cache(imageCacheSize, ccCacheSize)


class myHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	"""
	Class for server communication, will handle any incomming request
	"""


	def do_GET(self):
		"""
		Handler for the GET requests
		"""
	
		work = self.reqWorkResp()
		if work == "YES":
			
			try:
				date = datetime.datetime.strptime(self.path, "/%Y/%m/%d/%H%M")
				date = roundTime(date,roundTo=15*60)
			except Exception as e:
				print e
				self.send_response(400)
				self.end_headers()
				return
			
			tupleData = self.getBestImage(date)

			if tupleData == -1:
				self.send_response(404)
				self.end_headers()
				return
				
			image, cloudValue = tupleData
			print "CC =", cloudValue
	
			self.send_response(200)
			self.send_header('Content-type','jpg')
			self.send_header('x-CC',cloudValue)
			self.end_headers()

			self.wfile.write(image)
			print "Request complete"
			
		else:
			#Redirect the client
			self.send_response(303)
			#UPDATE IN FUTURE
			#self.send_header('Location','http://0.0.0.0:'+ ServersPorts[random.randint(0,2)])
			self.send_header('Location','http://vg.no')
			self.end_headers()

		
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
		

	#The request handler issues a inverse name lookup in order to display 
	#the client name in the log, this always fails and has a huge delay overrides it
	def address_string(self):
		host, port = self.client_address[:2]
		#return socket.getfqdn(host)
		return host
		

#Class to make the basehttpserver able to server threads
class ThreadedHTTPServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
	pass

		
if __name__ == '__main__':
	try:
		#Setting up the correct arguments
		parser = argparse.ArgumentParser()
		parser.add_argument("-p", "--port", type = int ,help = "which port should the server run on", default = "8080")
		parser.add_argument("-s", type = int ,help = "Which server number are you", default = "1")
		args = parser.parse_args()

		server = ThreadedHTTPServer(('', args.port), myHandler)
		print 'Started httpserver on port' , args.port
		
		#Wait forever for incoming http requests
		server.serve_forever()

	except KeyboardInterrupt:
		print '^C received, shutting down the web server'
		server.socket.close()
