import urllib2
import argparse
import random
import Image
import cStringIO
import json
from config import *
from datetime import *
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):

	#Handler for the GET requests
	def do_GET(self):
		work = self.reqWorkResp()
		
		if work == "YES":
			
			#Caluclate the cloudiness for that time
			print self.path
			date = datetime.strptime(self.path, "/%Y/%m/%d/%H%M")
			image, cloudValue = self.getBestImage(date)

			print "CC =", cloudValue
	
	
			self.send_response(200)
			self.send_header('Content-type','jpg')
			self.send_header('x-CC',cloudValue)
			self.end_headers()

			
			self.wfile.write(image)
			print "Request complete"
			
		else:
			self.send_response(303)
			
			#UPDATE IN FUTURE
			#self.send_header('Location','http://0.0.0.0:'+ ServersPorts[random.randint(0,2)])
			self.send_header('Location','http://0.0.0.0:8080')
			self.end_headers()

		
	def reqWorkResp(self):
		response = urllib2.urlopen(C3Server)
		return response.read()
	
	
	def calculateCloudiness(self, image):
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
		
	def getImage(self, date):
		response = urllib2.urlopen(C2Server+ date.strftime("%Y/%m/%d/wcam0_%Y%m%d_%H%M.jpg") )
		return response.read()

	def getBestImage(self, date):
		pictures = []

		fifteenMinutes = timedelta(minutes=15)
		median = 0.0
		
		for x in xrange(-2,3):
			tmpdate = date + (x * fifteenMinutes)
			image = self.getImage(tmpdate)
			
			
			CC = self.calculateCloudiness(image)
			pictures.append((image, CC))
			median += CC

			
		median = median/5
		bestPicture = ""
		bestValue = 100.0
		for image in pictures:
			if abs(image[1] - median) < bestValue:
				bestPicture = image[0]
				bestValue = image[1]
				
		return (bestPicture, median)
		

	#
	def address_string(self):
		host, port = self.client_address[:2]
		#return socket.getfqdn(host)
		return host
		
		
		
if __name__ == '__main__':
	try:
		#Setting up the correct arguments
		parser = argparse.ArgumentParser()
		parser.add_argument("-p", "--port", type = int ,help = "which port should the server run on", default = "8080")
		args = parser.parse_args()
		
		
		server = HTTPServer(('', args.port), myHandler)
		print 'Started httpserver on port' , args.port


		#Wait forever for incoming http requests
		server.serve_forever()

	except KeyboardInterrupt:
		print '^C received, shutting down the web server'
		server.socket.close()
