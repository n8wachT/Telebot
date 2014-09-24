#!/usr/bin/python
###################################################################
# HexBot - a heavily modified version of asdofindia's telegram bot#
#							          #
# Author: Firaenix, Hexane                                        #
###################################################################

from threading import Thread
from timeit import Timer
import lxml.html
import time
import sys
import glob
import traceback
import subprocess
import re
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool

import pluginComponent

pathtotg='../tg/'    #include trailing slash. I don't know if '~' notation works
lastmessage=''
proc=None
spacer = "_____________________"
globalGroup = ""
#Max number of queries to bot is 25
pool = ThreadPool(processes=100)
errorGroup = ""
errorPeer = "Error"


pluginCmds = []
plugins = []
helpString = 'All possible commands:'

#Is this referenced?
#this function somehow works in preventing duplicate messages
def mymessage(message):
	global lastmessage

	if (message == lastmessage):
		return True
	else:
		return False

def AI(group,peer,message):
	#uncomment for debug
	#if lastmessage is not None:
	#	print 'message is '+message+' and lastmessage is '+lastmessage+'\n

	try:
		if mymessage(message):
			return
		replyrequired=False
		reply=None
		if group is None:
			replyrequired=True
	#if (message[:3].lower()=="!wolf"):
	#	replyrequired=True

		reply= pluginComponent.callmodule(message)

		if reply is not None:
			msg(group,peer,reply)
	except Exception as e:
		print "Unexpected error occurred..."
                print e.message, e.args
                proc.stdin.write('msg '+peer.replace(' ','_')+' '+"Something went wrong..."+'\n\n'+e.message+"\n"+e.args)
	
			
def spam(message):
	if (message == lastmessage):
		return True
	else:
		return False

	
def msg(group,peer,message):
	global proc
	if (group is not None):
		#Returns message to specified user: peer
		#peer = peer.split(' ')[0] +" "+ peer.split(' ')[1].rstrip()

		message=peer + ": \n"+spacer+'\n'+ message
		#message = message.encode("UTF-8")
		peer=group.rstrip()
	if (not spam(message)):
		if(('\n' in message)or('\r' in message) or ('\r\n' in message)):
			
			try:
				tempfile='temp'
				temp=open(tempfile,'w')
				temp.write(message)
				temp.close()
				proc.stdin.write('send_text '+peer.replace(' ','_')+' '+tempfile.encode("UTF-8")+'\n')
			except Exception as e:
				print "Unexpected error occurred..."
				print e.message, e.args
				proc.stdin.write('msg '+peer.replace(' ','_')+' '+"Something went wrong..."+'\n\n'+e.message+"\n"+e.args)
		else:
			proc.stdin.write('msg '+peer.replace(' ','_')+' '+message+'\n')
		global lastmessage
		lastmessage=message

def bot():

	COLOR_RED="\033[0;31m"
	COLOR_REDB="\033[1;31m"
	COLOR_NORMAL="\033[0m"
	COLOR_GREEN="\033[32;1m"
	COLOR_GREY="\033[37;1m"
	COLOR_YELLOW="\033[33;1m"
	COLOR_BLUE="\033[34;1m"
	COLOR_MAGENTA="\033[35;1m"
	COLOR_CYAN="\033[36;1m"
	COLOR_LCYAN="\033[0;36m"
	COLOR_INVERSE="\033[7m"
	
	global pathtotg
	global proc
	proc=subprocess.Popen([pathtotg+'telegram','-k',pathtotg+'tg-server.pub'],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
	lastmessage=None
	multiline=False
	
	for line in iter(proc.stdout.readline,''):
		if multiline and line != None and message != None:
			message+=line
			message = message.decode("UTF-8")
			if line.endswith('[0m\n'):
				message=message.rstrip('[0m\n')
				multiline=False
		else:
			if ((COLOR_YELLOW+" is now online" in line) or (COLOR_YELLOW+" is now offline" in line) or (COLOR_YELLOW+": 0 unread" in line)):
				pass
			#Outputs all text chat
			#NECESSARY FOR PROCESSING COMMANDS, ETC.
			print line.rstrip()
		with open('output','a') as fil:
			fil.write(line)
			group=None
			peer=None
			message=None
				
			try:
                     	
				#A bad way of determining the peer name - if it is blue...
				if ((COLOR_BLUE+" >>>" in line) and (COLOR_BLUE+"[" in line) and ("!" in line)):
					#if you get change colour level errors, uncomment the below line, and comment the line below that.
					#peer=line.split(COLOR_REDB)[1].split(COLOR_RED)[0]			

					peer=line.split(COLOR_RED)[1].split(COLOR_NORMAL)[0]
					message=line.split(COLOR_BLUE+" >>> ")[1].split("\033")[0]
					if not line.endswith("[0m\n"):
						multiline=True
				if ((COLOR_GREEN+" >>>" in line) and ("!" in line)):
					group=line.split(COLOR_MAGENTA)[2].split(COLOR_NORMAL)[0]
					#For change colour level
					#peer=line.split(COLOR_REDB)[1].split(COLOR_RED)[0]

					peer=line.split(COLOR_RED)[1].split(COLOR_NORMAL)[0]
					message=line.split(COLOR_GREEN+" >>> ")[1].strip(COLOR_NORMAL).split("\033")[0]
					if not line.endswith("[0m\n"):
						multiline=True
				if ((COLOR_BLUE+" >>>" in line) and (COLOR_MAGENTA+"[" in line)):
					group=line.split(COLOR_MAGENTA)[2].split(COLOR_NORMAL)[0]
					globalGroup = group	
					
					#Splits the line to display the user name.
					#The username is displayed after the group name, separated my the letter 'm' Always,
					#Then strip the " [0" Which is displayed after the username.
					#rstrip() to remove final whitespace

					peer=line.split(group)[1].split('m')[2].strip(' [0').rstrip()

					message=line.split(COLOR_BLUE+" >>> ")[1].strip(COLOR_NORMAL).split("\033")[0]
					if not line.endswith("[0m\n"):
						multiline=True
				if COLOR_GREY+" *** Lost connection to server..." in line:
                                	#If the bot loses connection, restart the bot.
					subprocess.call('killall python; killall telegram; python bot.py')

			except IndexError:
				print "Error: Change colour levels"
		if( ((group is not None) or (peer is not None)) and (message is not None) and (not multiline)):
			#AI(group,peer,message)
			pool.apply_async(AI, (group, peer, message,))

	

def help():
	print helpString
	return helpString
	
def main():
	botthread = Thread(target = bot)
	botthread.start()

	#Writes current unix time to file
	unixtime = str(int(time.time()))
	f = open("unixfile","w")
	f.write(unixtime)
	f.close()
	
	#Pass in True as this is only called on First Run
	pluginComponent.getPlugins(True)

	botthread.join()

if __name__ == "__main__":
    main()

