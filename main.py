
import urllib.request
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import wget
import os
import sys

if __name__ == '__main__':
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

    # chaper_url="https://downloads.khinsider.com/game-soundtracks/album/minecraft"
    chaper_url=sys.argv[1]
    req = urllib.request.Request(url=chaper_url, headers=headers)  
    html=urllib.request.urlopen(req).read().decode("utf-8",errors="ignore")
    soup = BeautifulSoup(html, 'html.parser')

    foldname=soup.select("h2")[0].get_text()
    try:
        os.mkdir(foldname)
    except:
        pass
    os.chdir(os.path.join(os.getcwd(),foldname))

    # import ipdb
    # ipdb.set_trace()

    for img_tag in soup.select("body table div a"):
        img_url=img_tag.get("href")
        # import ipdb
        # ipdb.set_trace()
        wget.download(img_url)

    for song_url_tag in soup.select("td.playlistDownloadSong a"):
        try:
            hostname=urlparse(chaper_url).hostname
            song_url=urlparse(chaper_url).scheme+"://"+hostname+song_url_tag.get("href")
            song_req = urllib.request.Request(url=song_url, headers=headers)  
            song_html=urllib.request.urlopen(song_req).read().decode("utf-8",errors="ignore")
            song_soup = BeautifulSoup(song_html, 'html.parser')
            os.system("wget "+song_soup.select("span.songDownloadLink")[0].parent.get("href"))
            os.system("wget "+song_soup.select("span.songDownloadLink")[1].parent.get("href"))
            # wget.download(song_soup.select("span.songDownloadLink")[0].parent.get("href"))
            # wget.download(song_soup.select("span.songDownloadLink")[1].parent.get("href"))

        except:
            pass

    # import ipdb
    # ipdb.set_trace()
