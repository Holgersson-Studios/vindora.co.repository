"""
	Vindora
	Holgersson
"""
import sys
import xbmcaddon
import os
import xbmc
import xbmcgui
import time
import urllib2
import json
import hashlib
import urllib
import atexit
from xml.etree import ElementTree
import socket
REMOTE_SERVER = "www.google.com"

try:
	# see if we can resolve the host name -- tells us if there is
	# a DNS listening
	host = socket.gethostbyname(REMOTE_SERVER)
	# connect to the host -- tells us if the host is actually
	# reachable
	s = socket.create_connection((host, 80), 2)
	print "......--------- HALLELUJA!!!!"
except:
	print "......--------- FUCK FUCK FUCK FUCK!!!!"
	# HOME
	# xbmc.executebuiltin("XBMC.ActivateWindow(10000)")
	# ACCESS POINT
	xbmc.executebuiltin("XBMC.ActivateWindow(10000)")
	xbmc.executebuiltin('XBMC.Notification("Not Connected to the holy Internet"," Please establish a connection to the Internet.", 6000)')
	xbmc.sleep(1000000000000000000)
	


#plugin constants
__plugin__ = "Vindora"
__author__ = "Holgersson-Studios GmbH"
__settings__ = xbmcaddon.Addon(id='plugin.program.vindora.co')

my_addon = xbmcaddon.Addon('plugin.program.vindora.co')
addon_dir = xbmc.translatePath( my_addon.getAddonInfo('path') )
sys.path.append(os.path.join( addon_dir, 'resources', 'lib' ) )

SETTINGS = sys.modules[ "__main__" ].__settings__



vindora_src = "http://storage.googleapis.com/vindoras_final/screener"
vindora_th = "http://appdev.milchglas-media.de/vindora/videos/xbmcth/"
url = "http://appdev.milchglas-media.de/vindora/php_vindora/getvindora.php?userid="





class updateArgs:

	def __init__(self, *args, **kwargs):

		for key, value in kwargs.iteritems():
			if value == 'None':
				kwargs[key] = None
			else:
				kwargs[key] = urllib.unquote_plus(kwargs[key])
		self.__dict__.update(kwargs)



class LoginFTW:
	
	def __init__(self, *args, **kwargs):
		self.status = 0
		self.settings = {}
		self.settings['username'] = SETTINGS.getSetting("username_ftw")
		self.settings['password'] = SETTINGS.getSetting("password_ftw")

	def checkLogin(self):

		if self.settings['username'] == '' or self.settings['password'] == '':
			self.resp = xbmcgui.Dialog().yesno("No username/password set!","Vindora.tv requires you to be logged in to view", \
			"videos.  Would you like to log-in now?")
			if self.resp:
				self.respLogin = SETTINGS.openSettings()
				if self.respLogin:
					self.settings['username'] = SETTINGS.getSetting("username_ftw")
					self.settings['password'] = SETTINGS.getSetting("password_ftw")
					return self.settings['username'], self.settings['password']
				else:
					xbmc.executebuiltin('XBMC.Notification("Thanks"," Now enjoy Vindora.co", 2000)')
					return '', ''
			else:
				xbmc.executebuiltin('XBMC.Notification("Please Login:","An advanced user account is required to view content.", 3000)')
				#sys.exit()
				xbmc.sleep(3000)
				xbmc.executebuiltin('XBMC.Notification("OK!"," Now I will shutdown the System", 3000)')
				xbmc.sleep(3000)
				xbmc.executebuiltin("xbmc.ShutDown")
		else:
			return self.settings['username'], self.settings['password']
			
	def hashPassword(self, password):
		return hashlib.sha512(password).hexdigest()
		
class grabFTW:
	
	def __init__(self, *args, **kwargs):
		self.settings = {}
		self.settings['username'], self.settings['password'] = LoginFTW().checkLogin()
		self.settings['passHash'] = LoginFTW().hashPassword(self.settings['password'])
		self.urlString = 'http://appdev.milchglas-media.de/vindora/php_vindora/mailtest.php?userid=' + self.settings['username'] + '&password=' + self.settings['passHash']
		self.urlSENDOUT = 'http://appdev.milchglas-media.de/vindora/php_vindora/from_kodi.php?function_in=' + self.settings['username']
		self.urlRECEIVE = 'http://appdev.milchglas-media.de/vindora/php_vindora/to_kodi.php?function_return=' + self.settings['username']

	def getHTML(self, url): 
		self.currenturl = url
		htmlSource = None
		print "[FTW] Finding URL: "+self.currenturl
		htmlSource = urllib.urlopen(url).read()
		print "[FTW] Got URL."
		return htmlSource

	def getCredentials(self):

		hulluh = self.getHTML(self.urlString)
		return hulluh
		if hulluh == "TRUE":
			return hulluh
		else:	
			self.resp = xbmcgui.Dialog().ok("Username does not exists","Vindora.tv requires you to be signed up in to view", \
			"videos.  Please sign-up now on www.vindora.tv!")

	def getStatus(self):
		hulluhStatus = self.getHTML(self.urlRECEIVE)
		return hulluhStatus

	def clearStatus(self):
		clrStatus = self.getHTML(self.urlSENDOUT)
		return clrStatus

	

 
class XBMCPlayer(xbmc.Player):
	def __init__(self, *args):
		print "................................WHOT?"
		pass
 
	def onPlayBackStarted(self):
		print "................................START"
		print "................................TOTAL SECONDS:  " + str(xbmc.Player().getTotalTime())
		# Sende an PHP
		
 
	def onPlayBackPaused(self):
		print "................................PAUSED"
		# if paused load new video
		

 
	def onPlayBackResumed(self):
		print "................................RESUMED"
 
	def onPlayBackEnded(self):
		print "................................ENDED"
 
	def onPlayBackStopped(self):
		print "................................STOPPED"


		# Sende an PHP

		
		#atexit.register(self.goodbye, adjective='nice', name='Vindora.co')
		#xbmc.executebuiltin("XBMC.Container.Update(path,replace)")
		xbmc.executebuiltin("XBMC.ActivateWindow(10000)")
		#xbmc.executebuiltin("XBMC.ActivateWindow(WINDOW_DIALOG_NETWORK_SETUP)")
		xbmc.sleep(1000000000000000)
	#def goodbye(name, adjective):
	#	print 'Goodbye, %s, it was %s to meet you.' % (name, adjective)
		



		

 
player = XBMCPlayer(xbmc.PLAYER_CORE_DVDPLAYER)

if grabFTW().getCredentials() == "TRUE":
			response = urllib2.urlopen(url + grabFTW().settings['username'])
			
			data = json.loads(response.read())
			
			playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
			
			pl = xbmc.PlayList(1)

			pl.clear()
			
			s = 0
			#print "urlvalues"
			for s in data:
				#print "THE NEW RESPONSE HERE: ************************************* " + url + grabFTW().settings['username']
				video = vindora_src + "/" + s['videourl']

				listitem = xbmcgui.ListItem("'" + s['videoname'] + "'", thumbnailImage=vindora_th + s['xbmcth'])
				listitem.setInfo('video', {'Title': "'" + s['videoname'] + "'", 'Genre': "'" + s['category'] + "'"})
				xbmc.PlayList(1).add(url=video, listitem=listitem)
				

				print "this is the vid " + video
				#xbmc.executebuiltin("xbmc.playercontrol(RepeatAll)")
				xbmc.executebuiltin("xbmc.playercontrol(RepeatOne)")
			if grabFTW().getStatus() != "STP":

				player.play(pl)

			print "----------------------------xoxoxo-----"
			while player.isPlaying():
				
				if grabFTW().getStatus() == "PLNWVD":
					print "CLEAR______THE____STATUS_____:   " + grabFTW().clearStatus()

					response = urllib2.urlopen(url + grabFTW().settings['username'])
			
					data = json.loads(response.read())
					pl.clear()
			
					s = 0
					
					for s in data:
						print "THE NEW RESPONSE HERE: ************************************* " + url + grabFTW().settings['username']
						video = vindora_src + "/" + s['videourl']

						listitem = xbmcgui.ListItem("'" + s['videoname'] + "'", thumbnailImage=vindora_th + s['xbmcth'])
						listitem.setInfo('video', {'Title': "'" + s['videoname'] + "'", 'Genre': "'" + s['category'] + "'"})
						xbmc.PlayList(1).add(url=video, listitem=listitem)
				

						#print "this is the vid " + video
					#xbmc.executebuiltin("xbmc.playercontrol(RepeatAll)")
					xbmc.executebuiltin("xbmc.playercontrol(RepeatOne)")
			
					player.play(pl)
				

				if grabFTW().getStatus() == "RBT":
					print "REBOOT______THE____PI_____AND__CLEAR___STATUS:   " + grabFTW().clearStatus()
					xbmc.executebuiltin('XBMC.Notification("OK!"," Now I will reboot the System", 3000)')
					xbmc.sleep(3000)
					xbmc.executebuiltin("xbmc.Reboot")

				if grabFTW().getStatus() == "NTWRK":
					print "GO_TO______THE____NETWORK___STATUS:   " + grabFTW().clearStatus()
					xbmc.executebuiltin("XBMC.RunScript(service.openelec.settings)")

				if grabFTW().getStatus() == "STP":
					print "GO_TO______THE____HOME___SCREEN:   "
					print "CLEAR______THE____STATUS:   " + grabFTW().clearStatus()
					xbmc.executebuiltin("xbmc.playercontrol(Stop)")
					xbmc.executebuiltin("xbmc.playercontrol(Stop)")

				if grabFTW().getStatus() == "SHTDWN":
					print "STOP______AND_SHUT_DOWN:   "
					print "CLEAR______THE____STATUS:   " + grabFTW().clearStatus()
					xbmc.executebuiltin("xbmc.playercontrol(Stop)")
					xbmc.sleep(8000)
					xbmc.executebuiltin("xbmc.ShutDown")

					


				
				totaltime = xbmc.Player().getTotalTime()
				playedtime = xbmc.Player().getTime()
				por = totaltime - 15

				print "_____________TOTALTIME : " + str(totaltime)
				print "_____________PLAYED-TIME : " + str(playedtime)
				print "_____________POINT OF RETURN : " + str(por)

				#if playedtime >= por:
				#	print "SEEK SEEK SEEK SEEK SEEK SEEK"
				#	#xbmc.Player().seekTime(10)

				xbmc.sleep(10000)
			
			
			

			
			

 
monitor = xbmc.Monitor()
 
while True:
	if monitor.waitForAbort(1): # Sleep/wait for abort for 1 second.
		break # Abort was requested while waiting. Exit the while loop.



		
		

