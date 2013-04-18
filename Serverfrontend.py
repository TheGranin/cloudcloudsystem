import argparse, thread
from cache import *
from display import *
import BaseHTTPServer
import SocketServer



global cache
cache = Cache(imageCacheSize, ccCacheSize)
display = Display()
timer = ThreadSafeTimer(99)
timer2 = ThreadSafeTimer(99)


thread.start_new_thread(display.run, (cache,timer, timer2, timer3))
serverNumber = 0

class myHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	"""
	Class for server communication, will handle any incomming request
	"""
	
	def do_GET(self):
		"""
		Handler for the GET requests
		"""
		#print self.get_header()
		startTime = time.time() * 1000
		
		tile = self.headers.get('x-tile')
		work = self.reqWorkResp(serverNumber , tile)

		if "YES" in work:
			try:
				date = datetime.datetime.strptime(self.path, "/%Y/%m/%d/%H%M")
				date = roundTime(date,roundTo=15*60)
			except Exception as e:
				self.send_response(400)
				self.end_headers()
				return
			
			tupleData = self.getBestImage(date)

			if tupleData == -1:
				self.send_response(404)
				self.end_headers()
				return

				
			image, cloudValue = tupleData
			#print "CC =", cloudValue
	
			self.send_response(200)
			self.send_header('Content-type','jpg')
			self.send_header('x-CC',cloudValue)
			self.end_headers()

			self.wfile.write(image)
			#print "Request complete"
			timer.time(startTime, time.time()*1000)
			
		else:
			#Redirect the client
			self.send_response(303)
			server = getRandomServer()
			self.send_header('Location', server[0] + ":" +str(server[1]))
			self.end_headers()
			#TODO UPDATE IN FUTURE
			#self.send_header('Location','http://0.0.0.0:'+ ServersPorts[random.randint(0,2)])
		
	def reqWorkResp(self,servernumber = 1 ,tile = "tile-2-2"):
		"""
		Request an answer from the C3 server
		 MUST HAVE  at the end servernumber=3&client=tile-1-2
		"""
		try:
			response = urllib2.urlopen(C3Server +"servernumber=" + str(serverNumber) +"&client="+ str(tile) )
			return response.read()
		except Exception as e:
			print "C3 Server error"
			print e


	def getBestImage(self, date):
		"""
		Finds the image that best represent the cloudiness over a hour and the meidan over that cloudiness 
		"""
		startTime = time.time() * 1000
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
		
		timer2.time(startTime, time.time()*1000)
		return (bestImage, median)
		
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
		parser.add_argument("-s", "--serverNumber" ,type = int ,help = "Which server number are you", default = "1")
		args = parser.parse_args()
		serverNumber = args.serverNumber
		server = ThreadedHTTPServer(('', args.port), myHandler)
		print 'Started httpserver on port' , args.port
    
		#Wait forever for incoming http requests
		server.serve_forever()
	except KeyboardInterrupt:
		print '^C received, shutting down the web server'
		server.socket.close()
