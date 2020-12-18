#! python

import datetime
import logging
import getDraftResults
import ffyahoo

logging.basicConfig(level=logging.DEBUG)

players = {}
rosters = {}
draft_results = getDraftResults.getDraftResults('2014')
transactions = ffyahoo.getTransactions('2014')


# Input drafter players into player list
for player_cost, draft_round in enumerate(draft_results):
    for draft_player in draft_round:
        player_name = draft_player[0]
        owner_name = draft_player[1][:5]
        players[player_name] = {'owner': owner_name, 'cost': player_cost}


# Add Player (via add, waiver, or trade) Transaction
def addPlayer(transaction):
    owner_name = transaction['owner']
    player_name = transaction['player']

    # If player does not exist, create new player
    if player_name not in players:
        players[player_name] = {'owner': '', 'drop_date': None, 'cost': 5}

    # Update player's owner and cost
    player = players[player_name]
    player['owner'] = owner_name
    if transaction['type'] == 'waiver' and player['drop_date'] is not None:
        # If a player was dropped more than 3 days ago, they are not eligible to stay the same cost
        if transaction['date'] - datetime.timedelta(days=3) > player['drop_date']:
            transaction['type'] = 'add'
    if transaction['type'] == 'add':
        if player['cost'] > 5:
            player['cost'] = 5


# Drop Player Transaction
def dropPlayer(transaction):
    player_name = transaction['player']

    # Update player's owner and drop date
    player = players[player_name]
    player['owner'] = ''
    player['drop_date'] = transaction['date']


# Process Transactions
for transaction in reversed(transactions):
    if transaction['type'] == 'drop':
        dropPlayer(transaction)
    else:
        addPlayer(transaction)

# Add players to rosters
for curr_player in players:
    player = players[curr_player]
    if player['owner'] == '':
        continue
    if player['owner'] not in rosters:
        rosters[player['owner']] = [(curr_player, player['cost'])]
    else:
        rosters[player['owner']].append((curr_player, player['cost']))

# Print rosters
for roster in rosters:
    curr_roster = rosters[roster]
    print(roster)
    for player in curr_roster:
        print("Player: {}, Cost: {}".format(player[0], player[1]))
