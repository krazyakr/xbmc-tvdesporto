# -*- coding: utf-8 -*-
# This test program is for finding the correct Regular expressions on a page to insert into the plugin template.
# After you have entered the url between the url='here' - use ctrl-v
# Copy the info from the source html and put it between the match=re.compile('here')
# press F5 to run if match is blank close and try again.

import urllib2,urllib,re,HTMLParser

user_agent = 'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36'

def addLink(name,url,iconimage):
    print name + " | " + url + " | " + iconimage
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

url = "http://www.streamify.tv/resources/scripts/streamifyEmbed.js"
link = requestLink(url)


