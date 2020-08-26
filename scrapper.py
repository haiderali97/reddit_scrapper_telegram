import praw
import config as cfg
import calendar
import datetime
import requests
import shutil
from tinydb import TinyDB, Query, where


db = TinyDB("images.json")

reddit = praw.Reddit(client_id=cfg.r_client_id,
                     client_secret=cfg.r_client_secret,
                     password=cfg.r_password,
                     user_agent="noodboiftw",
                     username=cfg.r_username)

#print("#####"*5,reddit.user.me(),"#####"*10,"\n")#REMOVABLE #OKAY BUT WHY?

def download_image(param, img):
    response = requests.get(param, stream=True)
    with open(f'images/{img}', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
        del response
        return img


def fetch_image(sub, time):
    now = datetime.datetime.now()
    current = (f"{now.day}-{now.month}-{now.year}")
    ctime = (f"{now.hour}:{now.minute}:{now.second}")
    wday = (datetime.datetime.today().weekday())
    subreddit = reddit.subreddit(sub).top(time)
    for post in subreddit:
        url = post.url
        title = post.title
        link = "www.reddit.com"+post.permalink
        URLS = Query()
        if (db.contains(URLS.url == url)):    
            print("#####"*5,"DUPLICATED","#####"*10)
            return ["null"]
        else:
            nameofImage = str(sub)+str(now.minute)+str(now.second)+(url[-4:])
            if url.endswith("jpg") or url.endswith("png"):
                if nameofImage.endswith("jpg") or nameofImage.endswith("png"):
                    download_image(url, nameofImage)
                    subtype = "image"
            elif "gallery" in url:
                subtype = "gallery"
            else:
                nameofImage = str(url)
                subtype = "gif/video"
            db.insert({"url":f"{url}","time":f"{ctime}","subreddit" : sub})
            return [str(nameofImage), title, url, link, sub, subtype]





