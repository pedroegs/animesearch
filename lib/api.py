# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 20:02:33 2017

@author: pedroegs
"""
from bs4 import BeautifulSoup as bs
import urllib2 as ulib
import re
import os 
import sys
import time

__location__ = os.path.realpath(os.getcwd())

class API:
    anbient_base = "https://www.anbient.com"
    zipshare_base = "http://www51.zippyshare.com"
    
    def get_html(self,link):
        response = ulib.urlopen(link)
        page = response.read()
        html = bs(page)
        return html
    
    def parse_zipshare(self,link):
        html = self.get_html(link)
        #print html.prettify
        path = None
        script = html('script',{"type":"text/javascript"})
        for elem in script:
            if "'dlbutton'" in str(script):
                path = str(script)
                break
        
        #print path
        tentativas = 5
        while tentativas > 0:
            try:
                 aux = re.search("document\.getElementById\('dlbutton'\)\.href =(.+?);", path).group(1)
                 num_code = re.search("\((.+?)\)",aux).group(1)
                 print num_code
                 number = eval(num_code)
                 print number
                 aux = re.sub("\((.+?)\)",str(number),aux)
                 aux = re.sub('"',"",aux)
                 aux = re.sub('\+',"",aux)
                 aux = re.sub(' ',"",aux)
                 aux = re.sub('/pd/','/d/',aux)
                 break
            except AttributeError as e:
                tentativas = tentativas - 1
                print e
                print "erro em parse_zipshare tenando novamente em 5s ..."
                time.sleep(5)
                aux = "nops"
        
        if tentativas != 0:
            url = self.zipshare_base + aux
            print url
            retorno = self.download(url)
        else:
            retorno = False
        
        return retorno
        
    def download(self,url):
        print url
        tentativas = 5
        retorno = True
        while tentativas > 0:
            try:
                file_name = url.split('/')[-1]
                u = ulib.urlopen(url)
                f = open(os.path.join(__location__, 'dls/'+file_name), 'wb')
                meta = u.info()
                print meta
                if not meta.getheaders("Content-Length"):
                    opener = ulib.build_opener()
                    for cookie in meta.getheaders("Set-Cookie"):
                        opener.addheaders.append(('Cookie', str(cookie).split(';')[0] ))
                        print cookie
                   
                    #cookie = str([0])
                                      
                    u = opener.open(url)
                    meta = u.info()
                    print "meta 2"
                    print meta
                file_size = int(meta.getheaders("Content-Length")[0])
                break
            except Exception as e:
                tentativas = tentativas - 1
                print e
                print "ocorreu um erro , tentando novamente em 5s"
                time.sleep(5)
        
        if tentativas != 0:
            try:
                print ("Downloading: %s Bytes: %s" % (file_name, file_size) )
                
                file_size_dl = 0
                block_sz = 8192
                while True:
                    buffer = u.read(block_sz)
                    if not buffer:
                        break
                
                    file_size_dl += len(buffer)
                    f.write(buffer)
                    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
                    status = status + chr(8)*(len(status)+1)
                    print (status)
            except:
                retorno = False
                print "ocorreu um erro em download no link : %s"%(url)
            finally:
                f.close()
        else:
            retorno = False
        
        return retorno
    
    def search_anime_anbient(self,name):
        print "https://www.anbient.com/search?search_api_views_fulltext=%s"%(name)
        html = self.get_html("https://www.anbient.com/search?search_api_views_fulltext=%s"%(name))   
        hrefs = html('div',{'class' : 'panel-pane pane-views-panes pane-search-panel-pane-1'})[0].find_all("h2")

        links = []
        for link in hrefs:
            aux = (link.find('a')['href'],link.find('a').getText())
            links.append(aux)
            
        for index,(link,name) in enumerate(links):
            print str(index) + " => " + name
       
        while True:
            try:
                number=int(raw_input('digite o numero do anime que voce quer baixar:'))
                if number >= len(links) or number < 0:
                    print "valor digitado invalido"
                else:
                    break
            except ValueError:
                print "o valor nao é um numero"
        print "voce escolheu baixar o anime : " + str(links[number][1])
        self.parse_anbient(links[number][0])
    
    def parse_anbient(self,url):
        url = self.anbient_base + url
        print url
        html = self.get_html(url)
        print html.prettify()
        servers = html.select('div[class*="servidor"]')
        print servers
        for index,line in enumerate(servers):
            print str(index) + str(line['class'])
            