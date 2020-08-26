from bootstrap import updater, dispatcher, jobs 
from telegram.ext import CommandHandler, CallbackQueryHandler, Filters
from tinydb import TinyDB, Query, where
import en
import config as cfg 
import random 

users_db = TinyDB("users.json")

#Is a custom operation for tinydb 
def append(list_name, value):
    def transform(doc):
        doc[list_name].append(value)
    return transform 

def scrape_callback(context):     
    subr = random.choice(cfg.subreddits)
    print(subr)

def start(update, context):
    x = users_db.search(where('user_id') == update.effective_user.id)
    #user does not exist in the database
    if not x:
        users_db.insert({ "user_id" : update.effective_user.id, "subs" : [] })

    updater.bot.send_message(
        chat_id = update.effective_user.id,
        text = en.start,
        parse_mode = "MARKDOWN"
    )

def available(update, context):
    subrs = ""
    for sub in cfg.subreddits:
        subrs = f"{subrs}\n{sub}"

    updater.bot.send_message(
        chat_id = update.effective_user.id,
        text = en.available.format(subreddits = subrs),
        parse_mode = "MARKDOWN" 
    )

def subscribe(update, context):
    sub = update.message.text.split(" ")[1]        
    if sub not in cfg.subreddits:
        updater.bot.send_message(update.effective_user.id, en.no_subreddit)
        return False
    users_db.update(
        append('subs', sub),
        where("user_id") == update.effective_user.id
    ) 
    
    

jobs.run_repeating(callback, interval = 60, first = 0)
#jobs.start()

dispatcher.add_handler( CommandHandler('start', start, filters=Filters.private) )
dispatcher.add_handler( CommandHandler('available', available, filters=Filters.private) )
dispatcher.add_handler( CommandHandler('subscribe', subscribe, filters=Filters.private) )


updater.start_polling()
updater.idle()
