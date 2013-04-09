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
			path = self.path.split('/')
			if len(path) < 5:
				print "Invalid request"
				self.send_response(400)
				self.end_headers()
				return
			  
			year = path[1]
			month = path[2]
			day = path[3]
			time = path[4]
			
			#self.calculateCloudiness(year, month, day, time)
			self.send_response(200)
			self.send_header('Content-type','jpg')
			
			image, cloudValue = self.getBestImage(year, month, day, time)

			print "CC =", cloudValue
			self.send_header('x-CC',cloudValue)
			self.end_headers()

			
			self.wfile.write(image)
			return
		else:
			self.send_response(303)
			
			#UPDATE IN FUTURE
			#self.send_header('Location','http://0.0.0.0:'+ ServersPorts[random.randint(0,2)])
			self.send_header('Location','http://0.0.0.0:8080')
			self.end_headers()

			return
		
	def reqWorkResp(self):
		response = urllib2.urlopen(C3Server)
		return response.read()
	
	
	def calculateCloudiness(self, image):
		try:
			#print "IMAGE", image
			
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
						Nbw += 1;
					else:
						N+=1
			if ( Nbright > ( 626*266 )*0.4 ):
				CC = 100.0 - Nbw*100.0/(626*266);
			else:
				CC = 0.0; 
			return CC; 
		except IOError:
			print "cannot convert", infile
		
	def getImage(self, year, month, day, time):
		req = "wcam0_" + year + month + day +"_"+ time + ".jpg"
		response = urllib2.urlopen(C2Server+ year +"/"+ month + "/" + day + "/" + req )
		return response.read()

	def getBestImage(self,year,month,day,clock):
		pictures = []
		realDate = datetime(int(year), int(month), int(day), int(clock[0:2]), int(clock[2:4]))
		fifteenMinutes = timedelta(minutes=15)
		median = 0.0
		
		for x in xrange(-2,3):
			date = realDate + (x * fifteenMinutes)
			image = self.getImage(str(date.year), date.strftime("%m"), date.strftime("%e"), date.strftime("%H%M"))
			
			
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
		
		
		
		
		
		
try:
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