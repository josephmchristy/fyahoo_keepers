#! python

import unittest
import datetime

import transactions


class PlayerTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.empty_player = transactions.Player()
        cls.arg_player = transactions.Player('Arg Player', 'John Doe',
                                             datetime.date.today(), 7)

    @classmethod
    def tearDownClass(cls):
        del cls.empty_player
        del cls.arg_player

    # Test class constructor with no arguments
    def test_empty(self):
        self.assertEqual(self.empty_player.name, '')
        self.assertEqual(self.empty_player.owner, '')
        self.assertIsNone(self.empty_player.drop_date)
        self.assertEqual(self.empty_player.cost, 5)

    # Test class constructor with arguments
    def test_args(self):
        self.assertEqual(self.arg_player.name, 'Arg Player')
        self.assertEqual(self.arg_player.owner, 'John Doe')
        self.assertEqual(self.arg_player.drop_date, datetime.date.today())
        self.assertEqual(self.arg_player.cost, 7)


class transactiontests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.transaction_add = {'type': 'add',
                               'owner': 'John Doe',
                               'player': 'Add_Drop Player'}
        cls.transaction_drop = {'date': datetime.date(2020, 12, 9),
                                'type': 'drop',
                                'owner': 'John Doe',
                                'player': 'Add_Drop Player'}
        cls.transaction_waiver = {'date': datetime.date(2020, 12, 12),
                                  'type': 'waiver',
                                  'owner': 'John Doe',
                                  'player': 'Waiver Player'}

    @classmethod
    def tearDownClass(cls):
        del cls.transaction_add
        del cls.transaction_drop

    # Test an add transaction
    def test_add(self):
        transactions.addPlayer(self.transaction_add)
        added_player = transactions.players[self.transaction_add['player']]
        self.assertEqual(added_player.name, 'Add_Drop Player')
        self.assertEqual(added_player.owner, 'John Doe')
        self.assertEqual(added_player.cost, 5)

    # Test a drop transaction
    def test_drop(self):
        transactions.dropPlayer(self.transaction_drop)
        dropped_player = transactions.players[self.transaction_drop['player']]
        self.assertEqual(dropped_player.owner, '')
        self.assertEqual(dropped_player.drop_date, datetime.date(2020, 12, 9))

    # Test a waiver transaction
    def test_waiver(self):
        waiverPlayer = transactions.Player('Waiver Player', 'John Doe', datetime.date(2020, 12, 8), 7)
        transactions.players.update({waiverPlayer.name: waiverPlayer})
        transactions.addPlayer(self.transaction_waiver)
        added_player = transactions.players[self.transaction_waiver['player']]
        self.assertEqual(added_player.owner, 'John Doe')
        self.assertEqual(added_player.cost, 5)


if __name__ == '__main__':
    unittest.main()
