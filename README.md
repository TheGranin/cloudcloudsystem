cloudcloudsystem
================

assignment 2 inf-3203


Server Frontend:
/server contains the code for the server frontend
run python Serverfrontend.py to run the code

cache.py: Contains wrapper code for functions where in memory caching is used
dispaly.py: Code to be runned in threads to dispaly server information
limitedSizeDict.py: A last inn first out list, with limited size given in the contstructer
Serverfrontend.py: The handler for the server. Starts incomming requests in threads, Run this file
test.py: Test script to check if a server can be contacted
threadSafeTimer.py: A helper class to measure time, in a thread envoirement


Clients:
/client contains the code for the client to run
run python Client.py to run the code

Client.py: 	Contains the code to run the client, as well as the pygame code used for displaying information
			The display code runs in a seperate thead from the server request code
Timer.py	A helper class to measure time


Setup:
config.py: 	A file with some web addresses to backends servers and some helper functions
			Must be placed here as both the client and server is dependent on the file