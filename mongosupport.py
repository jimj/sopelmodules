from pymongo import MongoClient

import sopel.module

def setup(bot):
    mongoclient = MongoClient()
    bot.mongodb = mongoclient.ircbot

@sopel.module.commands('findone')
@sopel.module.require_admin
def findone(bot, trigger):
    collection = bot.mongodb[trigger.group(2)]
    doc = collection.find_one()
    bot.reply('found %s' % doc)
