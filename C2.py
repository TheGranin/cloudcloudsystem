import web
        
urls = (
  '/(.*)', 'index'
)

#Type of url
#http://vvnas00:9909/2003/03/22/wcam0_20030322_0000.jpg

class index:
    def GET(self, name):
      web.header("Content-Type","jpg")
      return open(name,"rb").read()
  

if __name__ == "__main__": 
    app = web.application(urls, globals())
    app.run()   