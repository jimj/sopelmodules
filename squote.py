import requests
from bs4 import BeautifulSoup
from sopel.module import commands

_URL = 'https://www.marketwatch.com/investing/stock/%s'

@commands('squote')
def lookup(bot, trigger):
    ticker_symbol = trigger.group(2).upper()
    url = _URL % ticker_symbol

    response = requests.get(url, headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'})
    if response.status_code != 200:
        bot.say("Got HTTP %s trying to look up %s" % (response.status_code, ticker_symbol))
    else:
        soup = BeautifulSoup(response.text)
        info = lambda keyword: soup.find('meta', {'name': keyword})['content']

        name = info('name')
        price = info('price')
        delta = info('priceChange')
        percent = info('priceChangePercent')

        bot.say("%s (%s): %s %s %s" % (name, ticker_symbol, price, delta, percent))
