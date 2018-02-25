import random
import unittest
from mock import Mock
from sopel.module import commands

@commands('zing')
def zing(bot, trigger):
    excitement = '!' * random.randint(0, 10)

    bot.say('ZING%s' % excitement)

class ZingTest(unittest.TestCase):
    def test_exictement_must_vary(self):
        mock_bot = Mock()
        mock_trigger = Mock()
        zings_to_gather = 20
        unique_excitements_to_expect = 5

        for i in range(0, zings_to_gather):
            zing(mock_bot, mock_trigger)

        #Gather the arguments to 'bot.say' via the Mock
        #then measure how many ! are attached to each zing.
        zings = list(map(lambda call: call[0][0], mock_bot.say.call_args_list))
        excitement_levels = set(map(lambda zing: len(zing) - zing.find('!'), zings))

        self.assertTrue(len(excitement_levels) >= unique_excitements_to_expect)
