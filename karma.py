from sopel.module import commands, rule

_IDX = 'item'
_VAL = 'value'

def id(str):
    return {'item': str}

def new(str, val):
    base = id(str)
    base.update({'value': val})
    return base

@commands('karma')
def karma(bot, trigger):
    karma = bot.mongodb.karma
    item = trigger.group(2)
    doc = karma.find_one(id(item))

    val = doc['value'] if doc else 0
    bot.say("%s: %d" % (item, val))

@rule('(.+)\+\+$')
def add_karma(bot, trigger):
    karma = bot.mongodb.karma
    item = trigger.group(1)
    adjust(karma, item)

@rule('(.+)--$')
def sub_karma(bot, trigger):
    karma = bot.mongodb.karma
    item = trigger.group(1)
    adjust(karma, item, -1)

def adjust(db, item, amount=1):
    doc = db.find_one(id(item))
    if doc:
        val = doc['value'] + amount
        db.update(doc, {'$set': {'value': val}})
    else:
        db.insert_one(new(item, amount))
