# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin
import urllib2,urllib,cgi, re
import HTMLParser
import xbmcaddon
import json
import traceback
import os
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP



def PlayStream(sourceSoup, urlSoup, name, url):
	#url = urlSoup.url.text
	playpath=urlSoup.playpath.text
	pageurl = urlSoup.pageurl.text
	
	#req = urllib2.Request(newURL)
	#req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
	#req.add_header('Referer',newURL)
	#response = urllib2.urlopen(req)
	#link=response.read()
	#response.close()
	#print link
	#match =re.findall('url:\s*\'(.*?(code).*?)\'', link)
	#print match
	#if len(match)==0:
	#	return False
	#match=match[0][0]
	liveLink= sourceSoup.rtmpstring.text;

	print 'rtmpstring',liveLink
	liveLink=liveLink%(playpath,pageurl)
	print 'liveLink',liveLink
	listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ), path=liveLink )
	xbmc.Player().play( liveLink,listitem)


