# -*- coding: utf-8 -*-
###########################################################################
# Displays a rude message                                                 #
# Author: Hexane                                                          #
###########################################################################

def help():
        return "!finger: spread hatred across the chat"

def do():
	str1 = u""".........................../´/) 
		  ....................,/¯../ 
		  .................../..../ 
		  ............./´¯/'...'/´¯`·¸ 
		  ........../'/.../..../......./¨¯\ 
		  ........('(...´...´.... ¯~/'...') 
		  .........\.................'...../ 
		  ..........\............... _.·´ 
		  ............\..............( 
		  ..............\.............\..."""
	#qtmessage = u"\n........................./´¯/)\n......................,/¯..//\n...................../..../ /\n............./´¯/'...'/´¯¯`·¸\n........../'/.../..../......./¨¯\\n........('(...´(..´......,~/'...')\n.........\.................\/..../\n..........''...\.......... _.·´\n............\..............(\n..............\............./\\n"
	return str1

def getCmd():
	return ["!finger"]

def getArgs():
	return 0

def hasEncodings():
	return True
