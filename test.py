# This test program is for finding the correct Regular expressions on a page to insert into the plugin template.
# After you have entered the url between the url='here' - use ctrl-v
# Copy the info from the source html and put it between the match=re.compile('here')
# press F5 to run if match is blank close and try again.

import urllib2,urllib,re,HTMLParser

def requestLink(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    link=link.replace('\n','')
    return link

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
#        if re.search('"success":false',link):
#                return 'NULL'
#        else:
#                return chname
        return chname

def getChannelInfo(rawData):
    match=re.compile('<channel name="(.+?)" icon="(.+?)">.+?<providers>(.+?)</providers>').findall(rawData)
    return match

#url='http://mymediaboxcreation.blogspot.pt/2014/03/channels.html'
#url='http://cdn.sporttvhdmi.com/iframes/Sporttv1-iframe1.php'
#url='http://www.tvdez.com/embed.php?c=sporttv&height=500&width=650'
url='http://www.gosporttv.com/'

link=requestLink(url)
match=re.compile('delete me').findall(link)
print match

##url2=match[0]
##link2=requestLink(url2)
##match2=re.compile('>var urls = new Array\((.+?)\)').findall(link2)
###print match2
##match3=re.compile('"(.+?)"').findall(match2[0])
###print match3
##
##url4=match3[0]
##link4=requestLink(url4)
##match4=re.compile('>var urls = new Array\((.+?)\)').findall(link4)
##print match4
##match5=re.compile('"(.+?)"').findall(match4[0])
##print match5

