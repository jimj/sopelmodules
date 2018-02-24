import requests
from bs4 import BeautifulSoup
from sopel.module import commands

_URL = 'https://www.bloomberg.com/quote/%s:US'

@commands('squote')
def lookup(bot, trigger):
    ticker_symbol = trigger.group(2).upper()
    url = _URL % ticker_symbol

    response = requests.get(url)
    if response.status_code != 200:
        bot.say("Got HTTP %s trying to look up %s" % (response.status_code, ticker_symbol))
    else:
        soup = BeautifulSoup(response.text)
        info = lambda keyword: soup.find('meta', itemprop=keyword)['content']

        name = info('name')
        price = info('price')
        delta = info('priceChange')
        percent = info('priceChangePercent')

        bot.say("%s (%s): %s %s %s" % (name, ticker_symbol, price, delta, percent))
