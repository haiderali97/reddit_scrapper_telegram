from bootstrap import updater, dispatcher, jobs,  users_db 
from telegram.ext import CommandHandler, CallbackQueryHandler, Filters
from tinydb import TinyDB, Query, where
from tinydb.operations import set
import en
import config as cfg 
import random 
import scrapper 
import job 

#Is a custom operation for tinydb to append to list
def append(list_name, value):
    def transform(doc):
        doc[list_name].append(value)
    return transform  

#Is a custom operation for tinydb to delete from list
def delete(list_name, value):
    def transform(doc):
        doc[list_name].remove(value)
    return transform 

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
    try:
        sub = update.message.text.split(" ")[1]       
    except:
        return available(update, context)        

    #check if sub is valid  
    if sub != 'all' and sub not in cfg.subreddits:
        updater.bot.send_message(update.effective_user.id, en.no_subreddit)
        return False

    if sub == 'all':
        users_db.update( set("subs", cfg.subreddits), where("user_id") == update.effective_user.id  )
        text = en.subscribed_to_all
    else:            
        #Check if user is already subscribed 
        users = users_db.search((where('user_id') == update.effective_user.id) & ( where("subs").any([sub]) ) )
        if users:
            updater.bot.send_message(update.effective_user.id, en.already_subbed)
            return False 

        users_db.update(append('subs', sub), where("user_id") == update.effective_user.id)     
        text = en.subscribed_to.format(sub = sub)    

    updater.bot.send_message(update.effective_user.id, text, parse_mode = "MARKDOWN")
        
def unsubscribe(update, context):
    try:
        sub = update.message.text.split(" ")[1]       
    except:
        return available(update, context)
        
    #check if sub is valid  
    if sub != 'all' and sub not in cfg.subreddits:        
        return False

    if sub == 'all':
        users_db.update( set("subs", []), where("user_id") == update.effective_user.id  )
        text = en.unsub_from_all
    else:            
        #Check if user is already subscribed 
        users = users_db.search((where('user_id') == update.effective_user.id) & ( where("subs").any([sub]) ) )
        if not users:
            updater.bot.send_message(update.effective_user.id, en.not_subbed)
            return False 

        users_db.update(delete('subs', sub), where("user_id") == update.effective_user.id)     
        text = en.unsub_from.format(sub = sub)    

    updater.bot.send_message(update.effective_user.id, text, parse_mode = "MARKDOWN")    

jobs.run_repeating(job.scrape_callback, interval = 60, first = 0)
jobs.start()

dispatcher.add_handler( CommandHandler('start', start, filters=Filters.private) )
dispatcher.add_handler( CommandHandler('available', available, filters=Filters.private) )
dispatcher.add_handler( CommandHandler('subscribe', subscribe, filters=Filters.private) )
dispatcher.add_handler( CommandHandler('unsubscribe', unsubscribe, filters=Filters.private) )

updater.start_polling()
updater.idle()
