import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon

#TVs Portuguesas by Avenger 2014.

def CATEGORIES():
        addDir('Desporto',basepath,1,logopath)
                       
def INDEX(url):
        link=requestLink(url)
        match=re.compile('<channel (.+?)</channel>').findall(link)
        for rawData in match:
                channelInfo=getChannelInfo("<channel "+rawData+"</channel>")
                addDir(channelInfo[0],channelInfo[2],2,artPath+channelInfo[1])

def VIDEOLINKS(url,name):
        providers=getChannelProviders(url)
        for rawData in providers:
                provider=getProviderInfo(rawData)
                if provider[0]=='veetle':
                        veetleID=getVeetleId(provider[2])
                        if veetleID != 'NULL':
                                streamfile='plugin://plugin.video.veetle/?channel=' + veetleID
                                print "Added stream: " + streamfile
                                addLink(provider[1],streamfile,'')
                if provider[0]=='flash':
                        print "Flash Channel: " + provider[1] + " | " + provider[2]
                        link=requestLink(provider[2])
                        if re.search('var urls = new Array',link):
                                framedupla=re.compile('new Array.+?"(.+?)".+?"(.+?)"').findall(link)[0]
                                if framedupla[0]==framedupla[1]:
                                        print "1 stream only"
                                else:
                                        print "2 streams: " + framedupla[0] + " | " + framedupla[1]
                        else:
                                print "1 stream only"
                
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

def getChannelInfo(rawData):
    match=re.compile('<channel name="(.+?)" icon="(.+?)">.+?<providers>(.+?)</providers>').findall(rawData)
    return match[0]

def getChannelProviders(rawData):
    match=re.compile('<provider (.+?)/>').findall(rawData)
    return match

def getProviderInfo(rawData):
    match=re.compile('type="(.+?)" name="(.+?)" link="(.+?)"').findall(rawData)
    return match[0]

def getVeetleId(url):
        link=requestLink(url)
        match=re.compile('<iframe.+?src="http://veetle.com/index.php/widget/index/(.+?)/0/true/default/false"></iframe>').findall(link)
        idembed=match[0]
        print "ID embed: " + idembed
        try:
                chname=requestLink('http://fightnightaddons.x10.mx/tools/veet.php?id=' + idembed)
                chname=chname.replace(' ','')
                if re.search('DOCTYPE HTML PUBLIC',chname):
                        return 'NULL'
                print "ID final obtido pelo TvM."
        except:
                chname=requestLink('http://fightnight-xbmc.googlecode.com/svn/veetle/sporttvhdid.txt')
                print "ID final obtido pelo txt."
        print "ID final: " + chname
        link=requestLink('http://veetle.com/index.php/channel/ajaxStreamLocation/'+chname+'/flash')
        if re.search('"success":false',link):
                return 'NULL'
        else:
                return chname
        return chname
      
params=get_params()
url=None
name=None
mode=None
basepath="http://mymediaboxcreation.blogspot.pt/2014/03/channels.html"
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
if mode==None:
        mode=1
        url=basepath

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print "Mode 1:"+url
        INDEX(url)
        
elif mode==2:
        print "Mode 2: "+url
        VIDEOLINKS(url,name)



xbmcplugin.endOfDirectory(int(sys.argv[1]))
