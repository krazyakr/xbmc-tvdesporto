# -*- coding: utf-8 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon
import sys

user_agent = 'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36'

def addLink(name,url,iconimage):
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty('IsPlayable', 'true')
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    return ok

def requestLink(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    link=link.replace('\n','')
    return link

def abrir_url_tommy(url,referencia,form_data=None,erro=True):
    print "A fazer request tommy de: " + url
    from t0mm0.common.net import Net
    net = Net()
    try:
        if form_data==None:link = net.http_GET(url,referencia).content
        else:link= net.http_POST(url,form_data=form_data,headers=referencia).content.encode('latin-1','ignore')
        return link

    except urllib2.HTTPError, e:
        if erro==True and activado==False:
            mensagemok('TV Desporto',str(urllib2.HTTPError(e.url, e.code, "Erro na página.", e.hdrs, e.fp)))
            sys.exit(0)
    except urllib2.URLError, e:
        if erro==True and activado==False:
            mensagemok('TV Desporto',"Erro na página.")
            sys.exit(0)

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
    #if re.search('"success":false',link):
    #    return 'NULL'
    #else:
    #    return chname
    return chname

def addStream(provider):
    if provider[0]=='veetle':
        veetleID=getVeetleId(provider[3])
        if veetleID != 'NULL':
            streamfile='plugin://plugin.video.veetle/?channel=' + veetleID
            print "Added stream: " + streamfile
            addLink(provider[2],streamfile,'')
    if provider[0]=='flash':
        print "Flash Channel: " + provider[1] + " | " + provider[2] + " | " + provider[3]
        link=requestLink(provider[3])
        if re.search('var urls = new Array',link):
            framedupla=re.compile('new Array.+?"(.+?)".+?"(.+?)"').findall(link)[0]
            if framedupla[0]==framedupla[1]:
                streamfile = getFlashStreamUrl(provider[1],framedupla[0],False)
                if streamfile!='': addLink(provider[2],streamfile,'')
            else:
                streamfile = getFlashStreamUrl(provider[1],framedupla[0],False)
                if streamfile!='': addLink(provider[2]+" #1",streamfile,'')
                streamfile = getFlashStreamUrl(provider[1],framedupla[1],False)
                if streamfile!='': addLink(provider[2]+" #2",streamfile,'')
        else:
            streamfile = getFlashStreamUrl(provider[1],provider[3],False)
            if streamfile!='': addLink(provider[2],streamfile,'')

def playStream(provider):
    if provider[0]=='veetle':
        veetleID=getVeetleId(provider[3])
        if veetleID != 'NULL':
            streamfile='plugin://plugin.video.veetle/?channel=' + veetleID
            print "Added stream: " + streamfile
            print streamfile
            addLink('Play',streamfile,'')
    if provider[0]=='flash':
        print "Flash Channel: " + provider[1] + " | " + provider[2] + " | " + provider[3]
        link=requestLink(provider[3])
        if re.search('var urls = new Array',link):
            framedupla=re.compile('new Array.+?"(.+?)".+?"(.+?)"').findall(link)[0]
            if framedupla[0]==framedupla[1]:
                streamfile = getFlashStreamUrl(provider[1],framedupla[0],False)
                if streamfile!='':
                    print streamfile
                    addLink('Play',streamfile,'')
            else:
                streamfile = getFlashStreamUrl(provider[1],framedupla[0],False)
                if streamfile!='':
                    print streamfile
                    addLink('Play #1',streamfile,'')
                streamfile = getFlashStreamUrl(provider[1],framedupla[1],False)
                if streamfile!='':
                    print streamfile
                    addLink('Play #2',streamfile,'')
        else:
            streamfile = getFlashStreamUrl(provider[1],provider[3],False)
            if streamfile!='':
                print streamfile
                addLink('Play',streamfile,'')
    
def getFlashStreamUrl(source,url_frame,content):
    print "getFlashStreamUrl: url_frame = " + url_frame
    
    if content==False:
        link = requestLink(url_frame)
    else:
        link = content

    # Clean up garbage
    link=link.replace('<title>Zuuk.net</title>','<title>zuuk.net</title>').replace('http://s.zuuk.net/300x250.html','').replace('www.zuuk.net\/test.php?ch=','').replace('cdn.zuuk.net\/boi.php','').replace('cdn.zuuk.net\/stats.php','').replace('cdn.zuuk.net/boi.php','').replace('cdn.zuuk.net/stats.php','').replace('<p><script language="JavaScript"> setTimeout','<p><script language="JavaScript">setTimeout')
    
    if re.search('ucaster', link):
        print "Stream: ucaster"
        ucaster=re.compile("channel='(.+?)',.+?></script>").findall(link)
        if not ucaster: ucaster=re.compile('flashvars="id=.+?&s=(.+?)&g=1&a=1&l=').findall(link)
        if not ucaster: ucaster=re.compile('src="/ucaster.eu.php.+?fid=(.+?)" id="innerIframe"').findall(link)
        if not ucaster: ucaster=re.compile('flashvars="id=.+?&amp;s=(.+?)&amp;g=1').findall(link)
        if not ucaster: ucaster=re.compile("flashvars='id=.+?&s=(.+?)&").findall(link)
        if not ucaster: ucaster=re.compile('flashvars="id=.+?id=.+?&amp;s=(.+?)&amp;g=1').findall(link)
        if not ucaster: ucaster=re.compile('channel="(.+?)".+?g="1"').findall(link)

        for chname in ucaster:
            embed='http://www.ucaster.eu/embedded/' + chname + '/1/600/430'
            try:
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                print html
                swf=re.compile('SWFObject.+?"(.+?)",').findall(html)[0]
                flashvars=re.compile("so.addParam.+?'FlashVars'.+?'(.+?);").findall(html)[0]
                flashvars=flashvars.replace("')","&nada").split('l=&')
                if flashvars[1]=='nada':
                    nocanal=re.compile("&s=(.+?)&").findall(flashvars[0])[0]
                    chid=re.compile("id=(.+?)&s=").findall(html)[0]
                else:
                    nocanal=re.compile("&s=(.+?)&nada").findall(flashvars[1])[0]
                    chid=re.compile("id=(.+?)&s=").findall(html)[1]
                nocanal=nocanal.replace('&','')
            except:
                nocanal=chname
                print link
                chid=re.compile("flashvars='id=(.+?)&s").findall(link)[0]
                swf=re.compile("true' src='http://www.ucaster.eu(.+?)'").findall(link)[0]
            link=requestLink('http://www.ucaster.eu:1935/loadbalancer')
            rtmpendereco=re.compile(".*redirect=([\.\d]+).*").findall(link)[0]
            streamurl='rtmp://' + rtmpendereco + '/live playPath=' + nocanal + '?id=' + chid + ' swfVfy=1 conn=S:OK live=true swfUrl=http://www.ucaster.eu' + swf + ' pageUrl=' + embed
            return streamurl

    elif re.search('mips', link):
        print "Stream: mips"
        mips=re.compile("channel='(.+?)',.+?></script>").findall(link)
        if not mips: mips=re.compile('channel="(.+?)",.+?></script>').findall(link)
        if not mips: mips=re.compile('<iframe src="/mips.tv.php.+?fid=(.+?)" id="innerIframe"').findall(link)
        for chname in mips:
            embed='http://www.mips.tv/embedplayer/' + chname + '/1/500/400'
            ref_data = {'Referer': url_frame,'User-Agent':user_agent}
            html= abrir_url_tommy(embed,ref_data)
            swf=re.compile('SWFObject.+?"(.+?)",').findall(html)[0]
            flashvars=re.compile("so.addParam.+?'FlashVars'.+?'(.+?);").findall(html)[0]
            flashvars=flashvars.replace("')","&nada").split('l=&')
            if flashvars[1]=='nada':
                nocanal=re.compile("&s=(.+?)&e=").findall(flashvars[0])[0]
                chid=re.compile("id=(.+?)&s=").findall(html)[0]
            else:
                nocanal=re.compile("&s=(.+?)&nada").findall(flashvars[1])[0]
                chid=re.compile("id=(.+?)&s=").findall(html)[1]
            nocanal=nocanal.replace('&','')
            link=requestLink('http://www.mips.tv:1935/loadbalancer')
            rtmpendereco=re.compile(".*redirect=([\.\d]+).*").findall(link)[0]
            streamurl='rtmp://' + rtmpendereco + '/live/ playPath=' + nocanal + '?id=' + chid + ' swfVfy=1 live=true timeout=15 conn=S:OK swfUrl=http://www.mips.tv' + swf + ' pageUrl=' + embed
            return streamurl

    elif re.search('zuuk.net', link):
        print "Stream: zuuk.net"
        if re.search("<div id='mediaspace'>",link):
            try:
                info=re.compile("<div id='mediaspace'>"+'<script language="javascript".+?' + "document.write.+?unescape.+?'(.+?)'").findall(link)[0]
                _info = urllib.unquote(info)
                zuuk = re.compile('<script.+?type="text/javascript".+?src="(.+?)">').findall(_info)[0]
                return getFlashStreamUrl(source,zuuk,_info)
            except RuntimeError as e:
                print "except: " + e.strerror
        elif re.search('<script type="text/javascript">var urls = new Array',link):
            zuuk=re.compile('new Array.+?"(.+?)",').findall(link)[0]
            _link = requestLink(zuuk)
            print zuuk
            print _link
            try:
                info=re.compile("<div id='mediaspace'>"+'<script language="javascript".+?' + "document.write.+?unescape.+?'(.+?)'").findall(_link)[0]
                _info = urllib.unquote(info)
                zuuk = re.compile('<script.+?type="text/javascript".+?src="(.+?)">').findall(_info)[0]
                return getFlashStreamUrl(source,zuuk,_info)
            except RuntimeError as e:
                print "except: " + e.strerror
        else:
            try: zuuk = re.compile('<iframe.+?src="(.+?)".+?/iframe>').findall(link)[0]
            except: zuuk = re.compile("<iframe.+?src='(.+?)'.+?/iframe>").findall(link)[0]
            return getFlashStreamUrl(source,zuuk,False)

    elif re.search('ezcast.tv', link):
        print "Stream: ezcast.tv"
        chname = re.compile('<script.+?channel="(.+?)".+?/script>').findall(link)[0]
        embed = "http://www.ezcast.tv/embedded/"+chname+"/1/650/500"
        ref_data = {'Referer': url_frame,'User-Agent':user_agent}
        html= abrir_url_tommy(embed,ref_data)
        link=requestLink('http://www.ezcast.tv:1935/loadbalancer')
        rtmpendereco=re.compile(".*redirect=([\.\d]+).*").findall(link)[0]
        idnum=re.compile("'FlashVars'.+?id=(.+?)&s=.+?&").findall(html)[0]
        chnum=re.compile("'FlashVars'.+?id=.+?&s=(.+?)&").findall(html)[0]
        streamurl='rtmp://' + rtmpendereco + '/live playPath=' + chnum + '?id=' + idnum + ' swfUrl=http://www.ezcast.tv/static/scripts/eplayer.swf live=true conn=S:OK swfVfy=1 timeout=14 pageUrl=' + embed
        return streamurl

    elif re.search('tugastream.com', link):
        print "Stream: tugastream.com"
        tugastream=re.compile('<iframe.+?src="(.+?)".+?/iframe>').findall(link)[0]
        return getFlashStreamUrl(source,tugastream,False)
    
    else:
        print "<<<<< Provider not supported >>>>>>"
        print link
        print "<<<<< Provider not supported >>>>>>"
    
    return ''
