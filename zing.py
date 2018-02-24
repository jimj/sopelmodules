import random
from sopel.module import commands

@commands('zing')
def zing(bot, trigger):
    excitement = '!' * random.randint(0, 10)

    bot.say('ZING%s' % excitement)
