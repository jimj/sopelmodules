import random
import re

from sopel.module import commands, example

#Matches: <@+nickNames123>
_NICKNAME = '(<[^\s]+>)'

@commands('quote')
def quote(bot, trigger):
    quotes = bot.mongodb.quotes
    input = trigger.group(2) if trigger.group(2) else ''

    quotable = re.findall(_NICKNAME, input)

    if quotable:
        who, quote = parse_quotable_params(input)
        store_quote(quotes, who, quote)
        bot.reply('quote stored.')
    else:
        nick, search = parse_search_params(input)
        bot.say(get_random_quote(quotes, nick, search))

def parse_search_params(params):
    param_re = '(?P<nick>\w+)?\s?(?P<search>\/.*\/)?$'
    params = re.match(param_re, params)

    if params:
        search = params.group('search')
        if search:
            search = search.strip().replace('/','')
        return (params.group('nick'), search)
    else:
        return (None, None)

def parse_quotable_params(params):
    param_re = '(?P<realname>\w+)?\s*[\d:]{0,5}\s*(?P<quote><.*)'
    params = re.match(param_re, params)

    quoted = [params.group('realname')] if params.group('realname') else []
    quote = params.group('quote')

    nicks = re.findall(_NICKNAME, quote)
    if  nicks:
        nicks = [re.subn(r'[@<>+]', '', n)[0] for n in nicks]
        quoted = [nick.lower() for nick in set(quoted + nicks)]

    return (quoted, quote)

def get_random_quote(quotes, nick, search):
    query = {}
    if nick:
        query['nick'] = nick.lower()
    if search:
        query['quote'] = re.compile(search, re.IGNORECASE)

    ids = quotes.find(query, [])
    num_quotes = ids.count()

    if num_quotes == 0:
        return "No quotes found."

    quote = random.randint(0, num_quotes - 1)

    quote = quotes.find({'_id': ids[quote]['_id']}, ['quote'])
    return quote[0]['quote']

def store_quote(quotes, quoted, quote):
    quote_doc = {
        'nick': quoted,
        'network': 'slashnet',
        'quote': quote
    }

    quotes.insert(quote_doc)
