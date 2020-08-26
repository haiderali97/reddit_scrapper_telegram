from telegram.ext import Updater, JobQueue
import config as cfg 

updater = Updater(token=cfg.token, use_context=True)
dispatcher = updater.dispatcher
jobs = JobQueue()
jobs.set_dispatcher(dispatcher=dispatcher)


