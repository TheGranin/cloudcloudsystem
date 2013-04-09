import urllib2
#http://vvnas00:9909/2003/03/22/wcam0_20030322_0115.jpg

response = urllib2.urlopen("http://0.0.0.0:8080/2003/03/22/0600")
response.read()
	