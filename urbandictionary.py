import json
import random
import requests
from sopel.module import commands

_URL = 'http://api.urbandictionary.com/v0/define?term=%s'

@commands('udict')
def lookup(bot, trigger):
    url = _URL % trigger.group(2)

    response = requests.get(url)
    if response.status_code != 200:
        bot.say("No definition found")
    else:
        definitions = json.loads(response.text)
        definitions = definitions['list']
        num_defs = len(definitions)
        bot.say("Found %d definitions, picking one." % num_defs)

        choice = random.randint(0, num_defs - 1)
        choice = definitions[choice]
        bot.say('%s: %s' % (choice['word'], choice['definition']))
