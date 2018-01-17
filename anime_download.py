import sys
import os
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

sys.path.insert(0, './lib')

import api 

anime = api.API()

#url = "http://download.thinkbroadband.com/10MB.zip"

with open(os.path.join(__location__, 'lista.txt')) as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content] 

print content
for link in content:
    if anime.parse_zipshare(link):
        content = None
        
print content


url = "/d/TkJuObiw/46316/Code-Breaker_05_Kyoshiro-Anbient.mkv"
#dl = base + url

#anime.search_anime_anbient("kuro")


