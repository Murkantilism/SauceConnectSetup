#@author: Deniz Ozkaynak - Created: 05/30/2013 - Last Updated: 05/30/2013
# Automatically installs the Sauce Connect Java utility to
# create a secure tunnel to the Sauce Cloud.

import subprocess, urllib, os, zipfile, sys
import time

# Get a list of all open ports and make sure 80 & 443 are not proxied.
def checkPorts():
	print "Getting list of open ports..."
	listOfPorts = subprocess.check_output('netstat -a | find "LISTENING"', shell=True)
	if('80' in listOfPorts):
		print "Port 80 open"
	else:
		print "Port 80 is NOT open"
		
	if('443' in listOfPorts):
		print "Port 443 open"
	else:
		print "Port 443 is NOT open"

# Download & unzip the Sauce Connect Java utility
def downloadSauceConnect():
	print "Downloading Sauce Connect..."
	# The URL address of the Sauce Connect download
	URL = 'http://saucelabs.com/downloads/Sauce-Connect-latest.zip'
	# The directory we want to download the zip to (current working dir)
	myDir = os.getcwd()
	
	name = os.path.join(myDir, 'temp.zip')
	
	# Try to retrieve the zip file
	try:
		name, hdrs = urllib.urlretrieve(URL, name)
		print "Download Complete."
	except IOError, e:
		print "Can't retrieve %r to %r: %s" % (URL, myDir, e)
		return
	
	print "Unzipping Sauce Connect..."
	# Try to open the zip file
	try:
		myZip = zipfile.ZipFile(name)
	except zipfile.error, e:
		print "Bad zipfile (from %r): %s" % (URL, e)
		return
	
	# Extract the contents of the zip file
	myZip.extractall()
	# Close/delete the zip file
	myZip.close()
	os.unlink(name)
	print "Unzip Complete. Starting Sauce Connect tunnel..."
	
# Start the Sauce Connect tunnel
def startSauceConnect():
	# First kill any pre-existing Sauce Connect tunnels
	harakiri()	
	# Get the Sauce username from the user
	SauceUsername = raw_input("\nEnter your Sauce Username: ")
	# Get the Sauce API key from the user
	SauceAPIKey = raw_input("Enter your Sauce API Key: ")
	
	print "\nSpawning Sauce Connect Daemon..."
	print "Proving P = NP..."
	# Run the Java utility via a Daemon
	subprocess.Popen('java -jar Sauce-Connect.jar ' + SauceUsername + " " + SauceAPIKey, creationflags=8, close_fds=True)
	print "Sauce Connect Tunnel Daemon successfully created!"
	
	# Once Sauce Connect has started, keep the connection fresh
	keepSauceFresh(SauceUsername, SauceAPIKey)

# Keep the Sauce Connect Tunnel connection fresh. The login credentials are 
# passed so the user doesn't have to re-login at midnight every day.
def keepSauceFresh(SauceUsername, SauceAPIKey):
	# Do nothing until it is midnight
	while(not("00:00:00" in time.ctime())):
		pass # Do nothing
	
	# Once it is midnight, kill the Sauce Connect Tunnel
	print "NIGHTLY MIDNIGHT REFRESH: Sauce Connect Tunnel Restarting..."
	harakiri()
	
	# Once the process is killed, restart the tunnel
	restartSauceConenct(SauceUsername, SauceAPIKey)

# [HELPER] Kill the Sauce Connect Tunnel nightly at 12AM
def harakiri():
	os.system('taskkill /f /im java.exe')

# [HELPER] Restarts the Sauce Connect Tunnel with the saved login credentials
def restartSauceConenct(SauceUsername, SauceAPIKey):
	# Restart the Tunnel
	subprocess.Popen('java -jar Sauce-Connect.jar ' + SauceUsername + " " + SauceAPIKey, creationflags=8, close_fds=True)
	# Keep Sauce Fresh!
	keepSauceFresh(SauceUsername, SauceAPIKey)

# The main invocation method
def SauceConnectSetup():
	checkPorts()
	downloadSauceConnect()
	startSauceConnect()
	
SauceConnectSetup()