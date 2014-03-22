# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin
import urllib2,urllib,cgi, re
import HTMLParser
import xbmcaddon
import json
import traceback
import os

__addon__       = xbmcaddon.Addon()
__addonname__   = __addon__.getAddonInfo('name')
__icon__        = __addon__.getAddonInfo('icon')
addon_id = 'plugin.video.shahidmbcnet'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonPath = xbmcaddon.Addon().getAddonInfo("path")
addonArt = os.path.join(addonPath,'resources/images')
 
mainurl='http://shahid.mbc.net'

def getMainUrl():
	rMain=mainurl
	#check setting and see if we have proxy define, ifso, use that
	isProxyEnabled=defaultCDN=selfAddon.getSetting( "isProxyEnabled" )
	proxyAddress=defaultCDN=selfAddon.getSetting( "proxyName" )
	if isProxyEnabled:#if its not None
		#print 'isProxyEnabled',isProxyEnabled,proxyAddress
		if isProxyEnabled=="true":
			#print 'its enabled'
			rMain=proxyAddress
		#else: #print 'Proxy not enable'
	return rMain
	
	
	

VIEW_MODES = {
    'thumbnail': {
        'skin.confluence': 500,
        'skin.aeon.nox': 551,
        'skin.confluence-vertical': 500,
        'skin.jx720': 52,
        'skin.pm3-hd': 53,
        'skin.rapier': 50,
        'skin.simplicity': 500,
        'skin.slik': 53,
        'skin.touched': 500,
        'skin.transparency': 53,
        'skin.xeebo': 55,
    },
}

def get_view_mode_id( view_mode):
	view_mode_ids = VIEW_MODES.get(view_mode.lower())
	if view_mode_ids:
		return view_mode_ids.get(xbmc.getSkinDir())
	return None

def addLink(name,url,iconimage):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def Colored(text = '', colorid = '', isBold = False):
	if colorid == 'ZM':
		color = 'FF11b500'
	elif colorid == 'EB':
		color = 'FFe37101'
	elif colorid == 'bold':
		return '[B]' + text + '[/B]'
	else:
		color = colorid
		
	if isBold == True:
		text = '[B]' + text + '[/B]'
	return '[COLOR ' + color + ']' + text + '[/COLOR]'	
	
def addDir(name,url,mode,iconimage	,showContext=False, showLiveContext=False,isItFolder=True,pageNumber=""):
#	print name
#	name=name.decode('utf-8','replace')
	h = HTMLParser.HTMLParser()
	name= h.unescape(name).decode("utf-8")
	#print ' printing name'
	rname=  name.encode("utf-8")
	#print rname
	#print iconimage
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(rname)
	if len(pageNumber):
		u+="&pagenum="+pageNumber
	ok=True
#	print iconimage
	liz=xbmcgui.ListItem(rname, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	#liz.setInfo( type="Video", infoLabels={ "Title": name } )

	if showContext==True:
		cmd1 = "XBMC.RunPlugin(%s&cdnType=%s)" % (u, "l3")
		cmd2 = "XBMC.RunPlugin(%s&cdnType=%s)" % (u, "xdn")
		cmd3 = "XBMC.RunPlugin(%s&cdnType=%s)" % (u, "ak")
		liz.addContextMenuItems([('Play using L3 Cdn',cmd1),('Play using XDN Cdn',cmd2),('Play using AK Cdn',cmd3)])
	
	if showLiveContext==True:
		cmd1 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "RTMP")
		cmd2 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "HTTP")
		liz.addContextMenuItems([('Play RTMP Steam (flash)',cmd1),('Play Http Stream (ios)',cmd2)])
	
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isItFolder)
	return ok
	


def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
				
	return param




def Addtypes():
	#2 is series=3 are links
	addDir('Channels' ,getMainUrl()+'/ar/channel-browser.html' ,2,addonArt+'/channels.png') #links #2 channels,3 series,4 video entry, 5 play
	addDir('Series' ,getMainUrl()+'/ar/series-browser.html' ,6,addonArt+'/serial.png')
	addDir('Streams' ,getMainUrl()+'/ar/series-browser.html' ,9,addonArt+'/stream.png')
	addDir('Settings' ,'Settings' ,8,addonArt+'/setting.png',isItFolder=False) ##
	return

def ShowSettings(Fromurl):
	selfAddon.openSettings()

def AddSeries(Fromurl,pageNumber=""):
#	print Fromurl
	req = urllib2.Request(Fromurl)
	req.add_header('User-Agent','Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	#print Fromurl
#	print "addshows"
#	match=re.compile('<param name="URL" value="(.+?)">').findall(link)
#	match=re.compile('<a href="(.+?)"').findall(link)
#	match=re.compile('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>').findall(link)
#	match =re.findall('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>', link, re.DOTALL|re.IGNORECASE)
#	match =re.findall('onclick="playChannel\(\'(.*?)\'\);".?>(.*?)</a>', link, re.DOTALL|re.IGNORECASE)
#	match =re.findall('<div class=\"post-title\"><a href=\"(.*?)\".*<b>(.*)<\/b><\/a>', link, re.IGNORECASE)
#	match =re.findall('<img src="(.*?)" alt=".*".+<\/a>\n*.+<div class="post-title"><a href="(.*?)".*<b>(.*)<\/b>', link, re.UNICODE)
	#regstring='<a href="(.*?)">[\s\t\r\n\f]*.*[\s\t\r\n\f]+.*[\s\t\r\n\f].*<img .*?alt="(.*?)" src="(.*?)"'
	regstring='<a href="(\/ar\/(show|series).*?)">\s.*\s*.*\s.*alt="(.*)" src="(.*?)" '
	match =re.findall(regstring, link)
	#print match
	#match=re.compile('<a href="(.*?)"targe.*?<img.*?alt="(.*?)" src="(.*?)"').findall(link)
	#print Fromurl


	for cname in match:
		addDir(cname[2] ,getMainUrl()+cname[0] ,4,cname[3])#name,url,img
	if mode==6:
		if not pageNumber=="":
			pageNumber=str(int(pageNumber)+1);#parseInt(1)+1;
		else:
			pageNumber="1";

		purl=getMainUrl()+'/ar/series-browser/autoGeneratedContent/seriesBrowserGrid~browse~-param-.sort-latest.pageNumber-%s.html' % pageNumber
		addDir('Next Page' ,purl ,6,'', False, True,pageNumber=pageNumber)		#name,url,mode,icon
	
#	<a href="http://www.zemtv.com/page/2/">&gt;</a></li>
#	match =re.findall('<a href="(.*)">&gt;<\/a><\/li>', link, re.IGNORECASE)
	
#	if len(match)==1:
#		addDir('Next Page' ,match[0] ,2,'')
#       print match
	
	return

def AddEnteries(Fromurl,pageNumber=0):
#	print Fromurl
	req = urllib2.Request(Fromurl)
	req.add_header('User-Agent','Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
#	print link
#	print "addshows"
#	match=re.compile('<param name="URL" value="(.+?)">').findall(link)
#	match=re.compile('<a href="(.+?)"').findall(link)
#	match=re.compile('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>').findall(link)
#	match =re.findall('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>', link, re.DOTALL|re.IGNORECASE)
#	match =re.findall('onclick="playChannel\(\'(.*?)\'\);".?>(.*?)</a>', link, re.DOTALL|re.IGNORECASE)
#	match =re.findall('<div class=\"post-title\"><a href=\"(.*?)\".*<b>(.*)<\/b><\/a>', link, re.IGNORECASE)
#	match =re.findall('<img src="(.*?)" alt=".*".+<\/a>\n*.+<div class="post-title"><a href="(.*?)".*<b>(.*)<\/b>', link, re.UNICODE)
#	print Fromurl
	match =re.findall('<a href="(\/ar\/episode.*?)">\s.*\s.*\s.*\s.*\s.*\s.*<img .*?alt="(.*?)" src="(.*?)".*\s.*.*\s.*.*\s.*.*\s.*.*\s.*.*\s.*\s*.*?>(.*?)<\/div>\s*.*?>(.*?)<\/div>', link, re.UNICODE)
#	print Fromurl

	#print match
	#h = HTMLParser.HTMLParser()
	
	#print match
	totalEnteries=len(match)
	for cname in match:
		finalName=cname[1];
		if len(finalName)>0: finalName+=' '
		finalName+=cname[3].replace('<span>','').replace('</span>','')
		
		#print 'a1'
		
		#if len(finalName)>0: finalName+=u" ";
		#print 'a2'
		if len(finalName)>0: finalName+=' '
		finalName+=cname[4]
		#print 'a3'
		#finalName+=cname[3]
		#print 'a4'
		
		addDir(finalName ,getMainUrl()+cname[0] ,5,cname[2],showContext=True,isItFolder=False)
		
		
	if totalEnteries==24:
		match =re.findall('<li class="arrowrgt"><a.*?this, \'(.*?(relatedEpisodeListingDynamic).*?)\'', link, re.UNICODE)
		if len(match)>0 or mode==7  :
			if not pageNumber=="":
				pageNumber=str(int(pageNumber)+1);#parseInt(1)+1;
			else:
				pageNumber="1";
			if mode==7:
				newurl=(Fromurl.split('pageNumber')[0]+'-%s.html')%pageNumber
			else:
				newurl=getMainUrl()+match[0][0]+'.sort-number:DESC.pageNumber-%s.html'%pageNumber;
			addDir('Next Page' ,newurl ,7,'', False, True,pageNumber=pageNumber)		#name,url,mode,icon
	
		
		
#	<a href="http://www.zemtv.com/page/2/">&gt;</a></li>
	#match =re.findall('<link rel=\'next\' href=\'(.*?)\' \/>', link, re.IGNORECASE)
	
	#if len(match)==1:
#		addDir('Next Page' ,match[0] ,3,'')
#       print match
	
	return
	
def AddChannels(liveURL):
	req = urllib2.Request(liveURL)
	req.add_header('User-Agent','Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
#	print link
#	match=re.compile('<param name="URL" value="(.+?)">').findall(link)
#	match=re.compile('<a href="(.+?)"').findall(link)
#	match=re.compile('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>').findall(link)
#	match =re.findall('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>', link, re.DOTALL|re.IGNORECASE)
#	match =re.findall('onclick="playChannel\(\'(.*?)\'\);".?>(.*?)</a>', link, re.DOTALL|re.IGNORECASE)
#	match =re.findall('<div class=\"post-title\"><a href=\"(.*?)\".*<b>(.*)<\/b><\/a>', link, re.IGNORECASE)
#	match =re.findall('<img src="(.*?)" alt=".*".+<\/a>\n*.+<div class="post-title"><a href="(.*?)".*<b>(.*)<\/b>', link, re.UNICODE)

	match =re.findall('<div class="subitem".*?id="(.*)">\s*.*\s*<a href="(.*?)".*\s.*\s*<.*src="(.*?)"', link,re.M)

	#print match
	#h = HTMLParser.HTMLParser()
	#print match
	for cname in match:
		chName=cname[1].split('/')[-1].split('.htm')[0]
		#print chName
		addDir(chName ,getMainUrl()+cname[1] ,3,cname[2], False, True,isItFolder=True)		#name,url,mode,icon

	return	
	

def AddStreams():
	match=getStreams();

	for cname in match:
		chName=cname[0]
		chUrl = cname[1]
		imageUrl = 'http://www.hdarabic.com/./images/'+cname[2]+'.jpg'
		#print imageUrl
		#print chName
		addDir(chName ,chUrl ,10,imageUrl, False, False,isItFolder=False)		#name,url,mode,icon

	return
	
def PlayStream(url, name):
	req = urllib2.Request(url)
	req.add_header('User-Agent','Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match =re.findall('file: "rtmp([^"]*)', link)

	rtmpLink=match[0]
	liveLink="rtmp%s app=live/ swfUrl=http://www.hdarabic.com/jwplayer.flash.swf pageUrl=http://www.hdarabic.com live=1 timeout=15"%rtmpLink
	print 'liveLink',liveLink

	listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ), path=liveLink )
	xbmc.Player().play( liveLink,listitem)


def PlayShowLink ( url ): 
#	url = tabURL.replace('%s',channelName);

	line1 = "Finding stream"
	time = 500  #in miliseconds
	line1 = "Playing video Link"
	xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))

	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
#	print url


	#print "PlayLINK"
	playURL= match =re.findall('id  : "(.*?)",\s*pricingPlanId  : "(.*?)"', link)
	videoID=match[0][0]# check if not found then try other methods
	paymentID=match[0][1]
	playlistURL=getMainUrl()+"/arContent/getPlayerContent-param-.id-%s.type-player.pricingPlanId-%s.html" % ( videoID,paymentID)
	req = urllib2.Request(playlistURL)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	jsonData=json.loads(link)
	#print jsonData;
	url=jsonData["data"]["url"]
	#print url
	
	
	defaultCDN="Default"
	defaultCDN=selfAddon.getSetting( "DefaultCDN" )
	
	print 'default CDN',defaultCDN,cdnType
	changeCDN=""
	
	print 'tesing if cdn change is rquired'
	if cdnType=="l3" or (cdnType=="" and defaultCDN=="l3"):
		changeCDN="l3"
	elif cdnType=="xdn" or (cdnType=="" and defaultCDN=="xdn"):
		changeCDN="xdn"
	elif cdnType=="ak" or (cdnType=="" and defaultCDN=="ak"):
		changeCDN="ak"
	print 'changeCDN',changeCDN
	if len(changeCDN)>0:
		print 'Changing CDN based on critertia',changeCDN
		#http://l3md.shahid.net/web/mediaDelivery/media/12af648b9ffe4423a64e8ab8c0100701.m3u8?cdn=l3
		print 'url received',url
		playURL= re.findall('\/media\/(.*?)\.', url)
		url="http://%smd.shahid.net/web/mediaDelivery/media/%s.m3u8?cdn=%s" % (changeCDN,playURL[0],changeCDN)
		
		print 'new url',url
		line1 = "Using the CDN %s" % changeCDN
		time = 2000  #in miliseconds
		xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))

		
	cName=name
	listitem = xbmcgui.ListItem( label = str(cName), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ), path=url )
	#print "playing stream name: " + str(cName) 
	listitem.setInfo( type="video", infoLabels={ "Title": cName, "Path" : url } )
	listitem.setInfo( type="video", infoLabels={ "Title": cName, "Plot" : cName, "TVShowTitle": cName } )
	print 'playurl',url
	xbmc.Player().play( url,listitem)
	#print 'ol..'
	return
	
def getStreams():
	return [('SemSem','http://www.hdarabic.com/semsem.php','semsem_tv'),
	('Al Arabiya','http://www.hdarabic.com/alarabiya.php','alarabiya'),
	('France 24','http://www.hdarabic.com/f24.php','f24'),
	('France 24 English','http://www.hdarabic.com/f24.php','f24'),
	('France 24 France','http://www.hdarabic.com/f24.php','f24'),
	('Al hiwar','http://www.hdarabic.com/alhiwar.php','alhiwar'),
	('Skynews','http://www.hdarabic.com/skynews.php','skynews'),
	('Skynews English','http://www.hdarabic.com/skynews.php','skynews'),
	('BBC Arabic','http://www.hdarabic.com/bbc.php','bbc'),
	('Al mayadeen','http://www.hdarabic.com/almayaden.php','almayaden'),
	('TAHA','http://www.hdarabic.com/taha.php','taha'),
	('National Wild','http://www.hdarabic.com/national_wild.php','national_wild'),
	('HODHOD','http://www.hdarabic.com/hod_hod.php','hod_hod'),
	('Karamesh','http://www.hdarabic.com/karamesh.php','karamesh'),
	('Qatar','http://www.hdarabic.com/qatar.php','qatar'),
	('Tunisia 2','http://www.hdarabic.com/tunisia_2.php','tv_tunisia2'),
	('Sama Dubai','http://www.hdarabic.com/sama_dubai.php','Sama-dubai'),
	('B4U plus','http://www.hdarabic.com/b4u+.php','b4u+'),
	('B4U Aflam','http://www.hdarabic.com/b4u_aflam.php','b4u_aflam'),
	('Saudi Sport','http://www.hdarabic.com/saudi_sport.php','saudi_sport'),
	('Dubai Sport','http://www.hdarabic.com/dubai_sport.php','dubai-sport'),
	('Dubai Sport 3','http://www.hdarabic.com/dubai_sport_3.php','dubai-sport'),
	('Dubai Racing','http://www.hdarabic.com/dubai_racing.php','dubai_racing'),
	('Oman','http://www.hdarabic.com/oman.php','oman_tv'),
	('Dubai','http://www.hdarabic.com/dubai.php','dubai'),
	('Play Hekayat','http://www.hdarabic.com/play_hekayat.php','play_hekayat'),
	('Watan','http://www.hdarabic.com/watan.php','watan'),
	('Watan Plus','http://www.hdarabic.com/watan_plus.php','watan_plus'),
	('Fox Movie','http://www.hdarabic.com/fox_movie.php','fox_movies'),
	('ART Cinema ','http://www.hdarabic.com/art.php','art'),
	('ART Hekayat','http://www.hdarabic.com/art_hekayat.php','art_hekayat'),
	('ART Hekayat 2','http://www.hdarabic.com/art_hekayat_2.php','art_hekayat_2'),
	('Melody Aflam','http://www.hdarabic.com/melody_aflam.php','melodytv'),
	('Melody Classic','http://www.hdarabic.com/melody_classic.php','melodytv'),
	('Melody Hits','http://www.hdarabic.com/melody_hits.php','melodytv'),
	('Melody Drama','http://www.hdarabic.com/melody_drama.php','melodytv'),
	('Mehwar','http://www.hdarabic.com/mehwar.php','mehwar'),
	('Mehwar 2','http://www.hdarabic.com/mehwar2.php','mehwar2'),
	('Talaki','http://www.hdarabic.com/talaki.php','talaki'),
	('Syria News','http://www.hdarabic.com/syria_news.php','syria_news'),
	('Oscar Drama','http://www.hdarabic.com/oscar_drama.php','oscar_drama'),
	('Cima','http://www.hdarabic.com/cima.php','cima'),
	('Cairo Cinema','http://www.hdarabic.com/cairo_cinema.php','cairo_cinema'),
	('Cairo Film','http://www.hdarabic.com/cairo_film.php','cairo_film'),
	('Cairo Drama','http://www.hdarabic.com/cairo_drama.php','cairo_drama'),
	('IFilm Arabic','http://www.hdarabic.com/ifilm.php','ifilm'),
	('IFilm English','http://www.hdarabic.com/ifilm.php','ifilm'),
	('IFilm Farsi','http://www.hdarabic.com/ifilm.php','ifilm'),
	('Gladiator','http://www.hdarabic.com/gladiator.php','gladiator'),
	('ESC1','http://www.hdarabic.com/esc1.php','al_masriya_eg'),
	('ESC2','http://www.hdarabic.com/esc2.php','masriaesc2'),
	('Panorama Film','http://www.hdarabic.com/panorama_film.php','panorama_film'),
	('TF1','http://www.hdarabic.com/tf1.php','tf1'),
	('M6 Boutique','http://www.hdarabic.com/m6.php','m6'),
	('TV5','http://www.hdarabic.com/tv5.php','tv5_monde_europe'),
	('Guilli','http://www.hdarabic.com/guilli.php','guilli'),
	('Libya','http://www.hdarabic.com/libya.php','libya'),
	('Assema','http://www.hdarabic.com/assema.php','assema'),
	('Libya Awalan','http://www.hdarabic.com/libya_awalan.php','libya_awalan'),
	('RTM Tamazight','http://www.hdarabic.com/tamazight.php','tamazight'),
	('Al maghribiya','http://www.hdarabic.com/maghribiya.php','maghribiya'),
	('Sadissa','http://www.hdarabic.com/sadissa.php','sadisa'),
	('A3','http://www.hdarabic.com/a3.php','a3'),
	('Algerie 4','http://www.hdarabic.com/algerie_4.php','algerie_4'),
	('Algerie 5','http://www.hdarabic.com/algerie5.php','algerie5'),
	('Al Nahar Algerie','http://www.hdarabic.com/nahar_algerie.php','nahar_algerie'),
	('Chorouk TV','http://www.hdarabic.com/chorouk.php','chorouk'),
	('El Beit Beitak','http://www.hdarabic.com/beitak.php','beitak'),
	('Insen','http://www.hdarabic.com/insen.php','insen'),
	('Nesma','http://www.hdarabic.com/nesma.php','rouge'),
	('Tounsiya','http://www.hdarabic.com/tounsiya.php','tounsiya'),
	('Aghanina','http://www.hdarabic.com/aghanina.php','aghanina'),
	('Nojoom','http://www.hdarabic.com/nojoom.php','nojoom'),
	('Funoon','http://www.hdarabic.com/funoon.php','funoon'),
	('Mazazik','http://www.hdarabic.com/mazazik.php','mazazik'),
	('Mazzika','http://www.hdarabic.com/mazzika.php','logo-mazzika'),
	('Power Turk','http://www.hdarabic.com/power_turk.php','power_turk'),
	('Al Haneen','http://www.hdarabic.com/alhaneen.php','alhaneen'),
	('Heya','http://www.hdarabic.com/heya.php','heya'),
	('CBC','http://www.hdarabic.com/cbc.php','cbc'),
	('CBC Extra','http://www.hdarabic.com/cbc_extra.php','cbc_extra'),
	('CBC Drama','http://www.hdarabic.com/cbc_drama.php','cbc_drama'),
	('CBC Sofra','http://www.hdarabic.com/cbc_sofra.php','cbc_sofra'),
	('Al Hayat 2 TV ','http://www.hdarabic.com/hayat_2.php','hayat_2'),
	('Dream 1','http://www.hdarabic.com/dream1.php','dream1'),
	('Nile Comedy','http://www.hdarabic.com/nile_comedy.php','nile_comedy'),
	('Nile News','http://www.hdarabic.com/nile_news.php','nile_news'),
	('Nile Family','http://www.hdarabic.com/nile_family.php','nile_family'),
	('Rotana Cinema','http://www.hdarabic.com/rotana_cinema.php','rotana_cinema'),
	('Rotana Clip','http://www.hdarabic.com/rotana_clip.php','rotana_clip'),
	('Rotana Classic','http://www.hdarabic.com/rotana_classic.php','rotana_classic'),
	('ANB','http://www.hdarabic.com/anb.php','anb'),
	('Arabica ','http://www.hdarabic.com/arabica.php','arabica-tv'),
	('MTV Arabia','http://www.hdarabic.com/mtv_arabia.php','mtv_arabia'),
	('MBC','http://www.hdarabic.com/mbc.php','mbc'),
	('MBC 2','http://www.hdarabic.com/mbc2.php','mbc2'),
	('MBC 3','http://www.hdarabic.com/mbc3.php','mbc3'),
	('MBC Action','http://www.hdarabic.com/mbc_action.php','mbc_action'),
	('MBC Max','http://www.hdarabic.com/mbc_max.php','mbc_max'),
	('MBC Drama','http://www.hdarabic.com/mbc_drama.php','mbc_drama'),
	('MBC Masr','http://www.hdarabic.com/mbc_masr.php','mbc_masr'),
	('MBC Masr Drama','http://www.hdarabic.com/mbc_masr_drama.php','mbc_masr_drama'),
	('MBC Bollywood','http://www.hdarabic.com/mbc_bollywood.php','mbc_bollywoodl'),
	('Wanasah','http://www.hdarabic.com/wanasah.php','wanasah'),
	('Nahar +2','http://www.hdarabic.com/nahar_+2.php','nahar+2'),
	('Nahar Sport','http://www.hdarabic.com/nahar_sport.php','al_nahar_sport'),
	('LBC Europe','http://www.hdarabic.com/lbc.php','lbc'),
	('Tele Liban','http://www.hdarabic.com/teleliban.php','teleliban'),
	('Syria ','http://www.hdarabic.com/syria.php','syria'),
	('Sama Syria ','http://www.hdarabic.com/sama_syria.php','sama_syria'),
	('MBC Maghreb','http://www.hdarabic.com/mbc_maghreb.php','mbc_maghreb'),
	('Abu Dhabi Sport','http://www.hdarabic.com/abu_dhabi_sport.php','abu_dhabi_sporti'),
	('Abu Dhabi','http://www.hdarabic.com/abu_dhabi.php','abudhabi'),
	('LBC','http://www.hdarabic.com/lbc.php','lbc'),
	('LBC Drama','http://www.hdarabic.com/lbc_drama.php','lbc_drama'),
	('LDC','http://www.hdarabic.com/ldc.php','ldc'),
	('AL Sharqia','http://www.hdarabic.com/sharqia.php','sharqia'),
	('Orient News','http://www.hdarabic.com/orient_news.php','orientnews'),
	('Al Alam','http://www.hdarabic.com/alalam.php','alalam'),
	('Nabaa ','http://www.hdarabic.com/nabaa.php','nabaa_tv_sa'),
	('Baghdadia 2','http://www.hdarabic.com/baghdad2.php','baghdad2'),
	('Kaifa','http://www.hdarabic.com/kaifa.php','kaifa'),
	('Suna Nabawiya','http://www.hdarabic.com/sunah.php','sunah'),
	('Iqrae','http://www.hdarabic.com/iqra.php','iqra'),
	('Rahma','http://www.hdarabic.com/rahma.php','rahma'),
	('Al Maaref','http://www.hdarabic.com/almaaref.php','almaaref'),
	('Sirat','http://www.hdarabic.com/sirat.php','sirat'),
	('Al Afassi','http://www.hdarabic.com/afasi.php','afasi'),
	('Ctv Coptic','http://www.hdarabic.com/ctv_coptic.php','ctv_eg'),
	('Sat7','http://www.hdarabic.com/sat7.php','sat7'),
	('Sat7 Kids','http://www.hdarabic.com/sat7_kids.php','sat7_kids'),
	('Aghapy','http://www.hdarabic.com/aghapy.php','aghapy_tv'),
	('Noursat','http://www.hdarabic.com/nour_sat.php','nour_sat'),
	('Miracle','http://www.hdarabic.com/miracle.php','miracle'),
	('Royali Somali','http://www.hdarabic.com/royali_somali.php','royali_somali'),
	('Somali Channel','http://www.hdarabic.com/somali_channel.php','somali_channel'),
	('Baraem','http://www.hdarabic.com/baraem.php','baraem_95x64'),
	('Space Power','http://www.hdarabic.com/space_power.php','space_power'),
	('Majd Kids','http://www.hdarabic.com/majd_kids.php','majd_kids'),
	('Majd Kids 2','http://www.hdarabic.com/majd_kids.php','majd_kids'),
	('Majd Roda','http://www.hdarabic.com/almajd.php','almajd'),
	('Majd Taghrid','http://www.hdarabic.com/almajd.php','almajd'),
	('Ajyal','http://www.hdarabic.com/ajyal.php','ajyal'),
	('ANN','http://www.hdarabic.com/ann.php','ann_95x44')]


	
#print "i am here"
params=get_params()
url=None
name=None
mode=None
linkType=None
pageNumber=None

try:
	url=urllib.unquote_plus(params["url"])
except:
	pass
try:
	name=urllib.unquote_plus(params["name"])
except:
	pass
try:
	mode=int(params["mode"])
except:
	pass

try:
	pageNumber=params["pagenum"]
except:
	pageNumber="";

args = cgi.parse_qs(sys.argv[2][1:])
cdnType=''
try:
	cdnType=args.get('cdnType', '')[0]
except:
	pass


print 	mode,pageNumber

try:
	if mode==None or url==None or len(url)<1:
		print "InAddTypes"
		Addtypes()

	elif mode==2:
		print "Ent url is "+name,url
		AddChannels(url)

	elif mode==3 or mode==6:
		print "Ent url is "+url
		AddSeries(url,pageNumber)

	elif mode==4 or mode==7:
		print "Play url is "+url
		AddEnteries(url,pageNumber)

	elif mode==5:
		PlayShowLink(url)
	elif mode==8:
		print "Play url is "+url,mode
		ShowSettings(url)
	elif mode==9:
		print "Play url is "+url,mode
		AddStreams();
	elif mode==10:
		print "Play url is "+url,mode
		PlayStream(url,name);
except:
	print 'somethingwrong'
	traceback.print_exc(file=sys.stdout)
	

if (not mode==None) and mode>1:
	view_mode_id = get_view_mode_id('thumbnail')
	if view_mode_id is not None:
		print 'view_mode_id',view_mode_id
		xbmc.executebuiltin('Container.SetViewMode(%d)' % view_mode_id)
if not ( mode==5 or mode==10):
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

