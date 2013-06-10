SauceConnectSetup
=================

A little Python script that automatically installs and sets up the Sauce Connect Java Utility tunnel.

This little Python script simply:
 - Downloads the Sauce Connect Java Utility from: http://saucelabs.com/downloads/Sauce-Connect-latest.zip
 - Unzips the download
 - Sets up the Sauce Connect Java Utility automatically. During setup the script:
   > Checks for the required open ports 80 & 443
   > Asks for the users Sauce username & API Key
   > Kicks off the Java utility with the authentication information

Prerequisite: Python 2.7.4 installed

To run this script, open a command prompt as Administrator, cd to the folder you downloaded the script, and execute it with either command:

  >SauceConnectSetup.py

or

  >python SauceConnectSetup.py
