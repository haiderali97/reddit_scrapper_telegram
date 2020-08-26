from bootstrap import updater, users_db
from random import choice 
import config as cfg 
import scrapper 
import os 
from tinydb import TinyDB, Query, where


def delete_sent(file):
        os.remove("images/"+file)

def scrape_callback(context):     
    subr = choice(cfg.subreddits)
    data = scrapper.fetch_image(subr, "hour")
    if data[0] == "null":
        pass
    else:        
        nameofImage, title, url, link, sub, subtype = data         
                
        users = users_db.search(where("subs").any([sub]))        

        if subtype == "image":            
            for user in users:
                chat_id = user['user_id']                
                updater.bot.send_photo(chat_id = chat_id, 
                                caption = f"{title}\n*Subreddit*:r/#{sub}\n[Link]({link})",
                                photo = open(f'images/{nameofImage}', 'rb'),
                                parse_mode = "MARKDOWN")

            delete_sent(nameofImage)
        elif subtype == "gallery":

            for user in users:
                chat_id = user['user_id']

                updater.bot.send_message(chat_id = chat_id,
                                caption = f'Gallery:{title}\n<a href={link}>link</a>\n',  
                                text = f"{nameofImage}\n",
                                parse_mode =  "HTML")
        else:
            for user in users:
                chat_id = user['user_id']

                updater.bot.send_message(chat_id = chat_id, 
                                text=f'{title}\n{url}\n*Subreddit*:r/#{sub}', 
                                parse_mode="MARKDOWN")        
    return True 
