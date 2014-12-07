import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon
import streams

#TV Desporto by krazyakr 2014.

def CATEGORIES():
        link = requestLink(basepath)
        categories = getCategories(link)
        for category in categories:
                addDir(category[1], basepath+category[0], 1, None)
                       
def INDEX(url):
        link=requestLink(url)
        events = getEvents(link)
        for rawData in events:
                addDir(rawData[0],rawData[1],2,None)

def STREAMS(url,name):
        providers=getChannelProviders(url)
        i = 1
        for rawData in providers:
                addDir('Link ' + str(i),rawData,3,None)
                i = i + 1

def PLAYSTREAM(url,name):
        streams.playStreamV2(url)
        
def VIDEOLINKS(url,name):
        providers=getChannelProviders(url)
        for rawData in providers:
                provider=getProviderInfo(rawData)
                streams.addStream(provider)

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


def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('IsPlayable', 'true')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
def requestLink(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link=link.replace('\n','')
        return link

def getCategories(rawData):
        match=re.compile('<div id="matchmenu">(.+?)</div>').findall(rawData)
        match2 = re.compile('<li class=.+?> <a href="(.+?)">(.+?)</a> </li>').findall(match[0])
        return match2

def getEvents(rawData):
        match=re.compile('<h3>(.+?)</div>').findall(rawData)
        events = []
        for rawData in match:
                broadcasttime=re.compile('<span class="matchtime">(.+?)</span>').findall(rawData)
                broadcastname=re.compile('<a.+?alt="(.+?)".+?</a>').findall(rawData)
                if len(broadcasttime) > 0:
                        events.append([broadcasttime[0] + ' - ' + broadcastname[0],rawData])
                else:
                        events.append([broadcastname[0],rawData])
        return events
        
def getChannelInfo(rawData):
    match=re.compile('<channel name="(.+?)" icon="(.+?)">.+?<providers>(.+?)</providers>').findall(rawData)
    return match[0]

def getChannelProviders(rawData):
        broadcastlinks=re.compile('<a.+?target=.+?href=\'(.+?)\'.+?</a>').findall(rawData)
        links = []
        for link in broadcastlinks:
                links.append(basepath + link)
        return links

def getProviderInfo(rawData):
    match=re.compile('type="(.+?)" source="(.+?)" name="(.+?)" link="(.+?)"').findall(rawData)
    return match[0]
      
params=get_params()
url=None
name=None
mode=None
#basepath="http://mymediaboxcreation.blogspot.pt/2014/03/channels.html"
basepath="http://firstrowpt.eu"
logopath="http://1.bp.blogspot.com/-j2_59w602G4/Uxn94vbEWII/AAAAAAAAEuo/TLqufuESJBo/s1600/logotipo.jpg"
artPath=xbmcaddon.Addon(id='plugin.video.tvdesporto').getAddonInfo('path') + "/resources/art/"

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

# Start with the channels - No categories to show
#if mode==None:
#        mode=1
#        url=basepath

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print "Mode 1:"+url
        INDEX(url)

#elif mode==2:
#        print "Mode 2: "+url
#        VIDEOLINKS(url,name)
        
elif mode==2:
        print "Mode 2: "+url
        STREAMS(url,name)

elif mode==3:
        print "Mode 3: "+url
        PLAYSTREAM(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
