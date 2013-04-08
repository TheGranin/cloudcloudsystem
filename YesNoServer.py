'''
Created on Apr 8, 2013

@author: Simon
'''

import web
import random


urls = ('/', 'index')

class index():
    def GET(self):
        randNum = random.randrange(0, 100);
        if (randNum < 70):
            return "GO FOR IT"
        else:
            return "DON't DO IT"

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()  