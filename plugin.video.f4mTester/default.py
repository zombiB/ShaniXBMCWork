import xbmc, xbmcgui, xbmcaddon, xbmcplugin, re
import urllib, urllib2
import re, string
import threading
import os
import base64
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
import urlparse
import xbmcplugin
addon = Addon('plugin.video.f4mTester', sys.argv)
net = Net()

mode =None
play=False

#play = addon.queries.get('play', None)
paramstring=sys.argv[2]
#url = addon.queries.get('playurl', None)
print paramstring
if paramstring:
    paramstring="".join(paramstring[1:])
    params=urlparse.parse_qs(paramstring)
    print params
    url = params['url'][0]#
    name = params['name'][0]
    mode =  params['mode'][0]
    play=True

def playF4mLink(url,name,proxy=None,use_proxy_for_chunks=False):
    from F4mProxy import f4mProxyHelper
    player=f4mProxyHelper()
    #progress = xbmcgui.DialogProgress()
    #progress.create('Starting local proxy')
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)
    
    player.playF4mLink(url, name, proxy, use_proxy_for_chunks)
    return   
    
def GUIEditExportName(name):

    exit = True 
    while (exit):
          kb = xbmc.Keyboard('default', 'heading', True)
          kb.setDefault(name)
          kb.setHeading('Enter Url')
          kb.setHiddenInput(False)
          kb.doModal()
          if (kb.isConfirmed()):
              name  = kb.getText()
              #name_correct = name_confirmed.count(' ')
              #if (name_correct):
              #   GUIInfo(2,__language__(33224)) 
              #else: 
              #     name = name_confirmed
              #     exit = False
          #else:
          #    GUIInfo(2,__language__(33225)) 
          exit = False
    return(name)
    
if mode ==None:
    
    videos=[['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/bbc1/bbc1_1500.f4m','bbc1 (uk) 1500kbps'],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/bbc2/bbc2_1500.f4m','bbc2 (uk) 1500kbps'],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/bbc3/bbc3_1500.f4m','bbc3 (uk) 1500kbps'],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/bbc4/bbc4_1500.f4m','bbc4 (uk) 1500kbps'],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/cbbc/cbbc_1500.f4m','cbbc (uk) 1500kbps'],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/cbeebies/cbeebies_1500.f4m','cbeebeies (uk) 1500kbps'],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/parl/parl_1500.f4m','bbc parliment (uk) 1500kbps'],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/newsch/newsch_1500.f4m','bbc news (uk) 1500kbps'],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/bbc1/bbc1_1500.f4m|X-Forwarded-For=212.58.241.131','bbc1 (outside uk) 1500kbps'],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/bbc2/bbc2_1500.f4m|X-Forwarded-For=212.58.241.131','bbc2 (outside uk) 1500kbps'],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/bbc3/bbc3_1500.f4m|X-Forwarded-For=212.58.241.131','bbc3 (outside uk) 1500kbps'],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/bbc4/bbc4_1500.f4m|X-Forwarded-For=212.58.241.131','bbc4 (outside uk) 1500kbps'],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/cbbc/cbbc_1500.f4m|X-Forwarded-For=212.58.241.131','cbbc (outside uk) 1500kbps'],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/cbeebies/cbeebies_1500.f4m|X-Forwarded-For=212.58.241.131','cbeebeies (outside uk) 1500kbps'],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/parl/parl_1500.f4m|X-Forwarded-For=212.58.241.131','bbc parliment (outside uk) 1500kbps'],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/newsch/newsch_1500.f4m|X-Forwarded-For=212.58.241.131','bbc news (outside uk) 1500kbps'],
    ['http://nhkworld-hds-live1.hds1.fmslive.stream.ne.jp/hds-live/nhkworld-hds-live1/_definst_/livestream/nhkworld-live-128.f4m','nhk 128'],
    ['http://nhkworld-hds-live1.hds1.fmslive.stream.ne.jp/hds-live/nhkworld-hds-live1/_definst_/livestream/nhkworld-live-256.f4m','nhk 256'],
    ['http://nhkworld-hds-live1.hds1.fmslive.stream.ne.jp/hds-live/nhkworld-hds-live1/_definst_/livestream/nhkworld-live-512.f4m','nhk 512'],
    ['http://77.245.150.95/hds-live/livepkgr/_definst_/liveevent/livestream.f4m','Turkish'],
    ['http://88.157.194.246/live/ramdisk/zrtp1/HDS/zrtp1.f4m','j0anita'],
    ['http://ak.live.cntv.cn/z/cctv9_1@139238/manifest.f4m?hdcore=2.11.3&g=OUVOVEOVETYH','cntv.cn'],
    ['http://mlghds-lh.akamaihd.net/z/mlg17_1@167001/manifest.f4m?hdcore=2.11.3&g=TOFRPVFGXLFS','alibaba'],
    ['http://peer-stream.com/api/get_manifest.f4m?groupspec=G:0101010c050e6f72663200','streamtivi.com'],
    ['http://164.100.31.234/hds-live/livepkgr/_definst_/rstvlive.f4m','Rajya Sabha TV'],
    ['http://fmssv1.merep.com/hds-live/livepkgr/_definst_/liveevent/livestream.f4m?blnpc20130909042035_1061880273','media center'],
    ['http://fms01.stream.internetone.it/hds-live/livepkgr/_definst_/8fm/8fm1.f4m','Italy otto 8 FMTV'],
    ['http://88.150.239.241/hds-live/livepkgr/_definst_/liveevent/livestream.f4m','Son Araba'],
    ['http://202.162.123.172/hds-live/livepkgr/_definst_/liveevent/livestream4.f4m','Chine Live event 4'],
    ['http://zb.wyol.com.cn/hds-live/livepkgr/_definst_/wslhevent/hls_pindao_1_350.f4m','CCTV 1 China'],
    ['http://zb.zghhzx.net/hds-live/livepkgr/_definst_/wslhevent/hls_pindao_1_350.f4m','CCTV13 China'],
    ['http://zb.sygd.tv/hds-live/livepkgr/_definst_/wslhevent/hls_pindao_1_350.f4m','SYGD TV china'],
    ['http://zb.pudongtv.cn/hds-live/livepkgr/_definst_/wslhevent/hls_pindao_1_500.f4m','Pudong TV China'],
    ['http://88.150.239.241/hds-live/livepkgr/_definst_/liveevent/livestream.f4m','AKS TV Turkey'],
    ['http://fms.quadrant.uk.com/hds-live/livepkgr/_definst_/liveevent/livestream.f4m','Quadrant live streams UK'],
    ['http://cdn3.1internet.tv/hds-live11/livepkgr/_definst_/1tv-hd.f4m','1 HD cdn1 Russia'],
    ['http://cdn2.1internet.tv/hds-live/livepkgr/_definst_/1tv.f4m','1 HD cdn2 Russia'],
    ['http://193.232.151.135/hds-live-not-protected/livepkgr/_1099_/1099/1099-70.f4m','ndtv plus - proxy needed'],
    ['http://77.245.150.95/hds-live/livepkgr/_definst_/liveevent/livestream.f4m','something else']]
    
    #['http://dummy','Custom']]
    #print videos

    if 1==2:
        req = urllib2.Request('http://www.gzcbn.tv/app/?app=ios&controller=cmsapi&action=pindao')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        ##	print link

        s='title\":\"(.*?)\",\"stream\":\"(.*?)\"'
        #    
        match=re.compile(s).findall(link)
        i=0
        for i in range(len(match)):
            match[i]= (match[i][1].replace('\\/','/'),match[i][0])


        videos+=match #disabled for time being as these are not working
    #print videos
    for (file_link,name) in videos:
        liz=xbmcgui.ListItem(name)
        liz.setInfo( type="Video", infoLabels={ "Title": name} )
        #liz.setProperty("IsPlayable","true")
        u = sys.argv[0] + "?" + urllib.urlencode({'url': file_link,'mode':'play','name':name}) 
        print u
        
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)


   
    
elif mode == "play":
    print 'PLAying ',mode,url
    if not name=='Custom':
        playF4mLink(url,name)
    else:
        newUrl=GUIEditExportName('')
        if not newUrl=='':
            playF4mLink(newUrl,name)




if not play:
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)
    
 