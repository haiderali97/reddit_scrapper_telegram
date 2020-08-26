from telegram.ext import Updater, JobQueue
from tinydb import TinyDB, Query, where
import config as cfg 

updater = Updater(token=cfg.token, use_context=True)
dispatcher = updater.dispatcher
jobs = JobQueue()
jobs.set_dispatcher(dispatcher=dispatcher)

users_db = TinyDB("users.json")
images_db = TinyDB("images.json")