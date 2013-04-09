import web
        
urls = (
	'/(.*)', 'index'
)

#Type of url
#http://vvnas00:9909/2003/03/22/wcam0_20030322_0115.jpg

class index:
	def GET(self, name):
		try:
			image = open(name,"rb").read()
		except Exception:
			raise web.notfound()
		
		web.header("Content-Type","jpg")
		return image 
  

if __name__ == "__main__": 
	app = web.application(urls, globals())
	app.run()   