import urllib2

#http://vvnas00:9909/2003/03/22/wcam0_20030322_0115.jpg
response = urllib2.urlopen("http://tile-5-1:8080/2003/03/22/0600")
#response = urllib2.urlopen("http://129.242.22.192:8080/2003/03/22/0600")
response.read()
print "YAY"
