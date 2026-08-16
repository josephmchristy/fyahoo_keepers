#! python

import sys
import unittest
import datetime
from unittest.mock import MagicMock

# transactions.py imports ffyahoo at module level, which performs live Yahoo
# OAuth setup on import. Stub it so these tests can run without credentials;
# addPlayer/dropPlayer under test don't use ffyahoo.
sys.modules.setdefault('ffyahoo', MagicMock())

import transactions


class TransactionTests(unittest.TestCase):

    def setUp(self):
        self.players = {}

    # Test an add transaction on a brand new player
    def test_add(self):
        transaction_add = {'type': 'add', 'owner': 'John Doe',
                           'player': 'Add_Drop Player'}
        transactions.addPlayer(transaction_add, self.players)
        added_player = self.players[transaction_add['player']]
        self.assertEqual(added_player['owner'], 'John Doe')
        self.assertIsNone(added_player['drop_date'])
        self.assertEqual(added_player['cost'], 6)

    # Test a drop transaction
    def test_drop(self):
        self.players['Add_Drop Player'] = {'owner': 'John Doe',
                                            'drop_date': None, 'cost': 6}
        transaction_drop = {'date': datetime.date(2020, 12, 9),
                            'type': 'drop', 'owner': 'John Doe',
                            'player': 'Add_Drop Player'}
        transactions.dropPlayer(transaction_drop, self.players)
        dropped_player = self.players[transaction_drop['player']]
        self.assertEqual(dropped_player['owner'], '')
        self.assertEqual(dropped_player['drop_date'], datetime.date(2020, 12, 9))

    # Test a waiver transaction outside the 3-day grace period, which is
    # treated as a new add and reset to the base keeper cost
    def test_waiver(self):
        self.players['Waiver Player'] = {'owner': '',
                                          'drop_date': datetime.date(2020, 12, 8),
                                          'cost': 7}
        transaction_waiver = {'date': datetime.date(2020, 12, 12),
                              'type': 'waiver', 'owner': 'John Doe',
                              'player': 'Waiver Player'}
        transactions.addPlayer(transaction_waiver, self.players)
        added_player = self.players[transaction_waiver['player']]
        self.assertEqual(added_player['owner'], 'John Doe')
        self.assertEqual(added_player['cost'], 6)


if __name__ == '__main__':
    unittest.main()
