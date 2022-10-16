
import urllib.request
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import os
import sys
import json
import tqdm

if __name__ == '__main__':
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

    # chaper_url="https://downloads.khinsider.com/game-soundtracks/album/minecraft"
    chaper_url=sys.argv[1]
    req = urllib.request.Request(url=chaper_url, headers=headers)  
    html=urllib.request.urlopen(req).read().decode("utf-8",errors="ignore")
    soup = BeautifulSoup(html, 'html.parser')

    audio_list=[]

    album_name=soup.select("h2")[0].get_text()

    img_num=0
    try:
        img_num=int(sys.argv[2])
    except:
        pass
    img_url=soup.select("body table div a img")[img_num].get("src")
    # img_url=""
    # for img_tag in soup.select("body table div a"):
    #     img_url=img_tag.get("href")
    #     break


    for song_url_tag in tqdm.tqdm(soup.select("td.playlistDownloadSong a")):
        try:
            hostname=urlparse(chaper_url).hostname
            song_url=urlparse(chaper_url).scheme+"://"+hostname+song_url_tag.get("href")
            song_req = urllib.request.Request(url=song_url, headers=headers)  
            song_html=urllib.request.urlopen(song_req).read().decode("utf-8",errors="ignore")
            song_soup = BeautifulSoup(song_html, 'html.parser')
            song_name=song_soup.find(id="pageContent").find_all(align="left")[1].select("b")[1].get_text()
            
            song_file_url1=song_soup.select("span.songDownloadLink")[0].parent.get("href")
            # song_file_url2=song_soup.select("span.songDownloadLink")[1].parent.get("href")


            song_dict={ 'name':song_name,\
                        'artist':album_name,\
                        'url':song_file_url1,\
                        'cover':img_url}
            audio_list.append(song_dict)


        except:
            pass

    audio_json=json.dumps(audio_list)
    with open(album_name+'.txt',"w") as f:
        f.write(audio_json)
        pass
    # import ipdb
    # ipdb.set_trace()
