from sopel.module import commands

@commands('zing')
def zing(bot, trigger):
    bot.reply('ZING!')
