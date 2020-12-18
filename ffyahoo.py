#! python

import xml.etree.ElementTree as ET
import re
import datetime

from yahoo_oauth import OAuth2

oauth = OAuth2(None, None, from_file='private.json')

if not oauth.token_is_valid():
    oauth.refresh_access_token()

url = "https://fantasysports.yahooapis.com/fantasy/v2"
game_league_ids = {
    '2014': ('331', '635114'),
    '2015': ('348', '521087'),
    '2016': ('359', '691742'),
    '2017': ('371', '675894'),
    '2018': ('380', '966146'),
    '2019': ('390', '655835'),
    '2020': ('399', '414682')
}

# Get the roster for a team
req_url = url + "/team/" + "399.l.414682.t.2/roster/players"
r = oauth.session.get(req_url)
xmlstring = r.text
xmlstring = re.sub(' xmlns="[^"]+"', '', xmlstring, count=1)
root = ET.fromstring(xmlstring)
for player in root.iter('player'):
    player_name = player.find('name')
    player_fullname = player_name.find('full')
    print(player_fullname.text)

# Get the transactions for the league
req_url = url + "/league/399.l.414682/transactions"
r = oauth.session.get(req_url)
xmlstring = r.text
xmlstring = re.sub(' xmlns="[^"]+"', '', xmlstring, count=1)
root = ET.fromstring(xmlstring)
transactions_list = []
for transaction in root.iter('transaction'):
    # For all add/drop or trade transactions
    transaction_type = transaction.find('type').text
    if transaction_type != 'commish':
        # Get the transaction date
        transaction_timestamp = transaction.find('timestamp').text
        transaction_date = datetime.date.fromtimestamp(int(transaction_timestamp))
        # For each player in the transaction
        players = transaction.find('players')
        for player in players:
            transaction_data = player.find('transaction_data')
            # Get the player's name
            player_name = player.find('name')
            p_transaction_name = player_name.find('full').text
            # Get the transaction type (add, drop, or trade)
            p_transaction_type = transaction_data.find('type').text
            # If a player is added via trade or add, get the new owner and check for waiver
            if p_transaction_type == 'trade' or p_transaction_type == 'add':
                p_transaction_owner = transaction_data.find('destination_team_name').text[0:5]
                p_source_type = transaction_data.find('source_type').text
                if p_source_type == 'waivers':
                    p_transaction_type = 'waiver'
            # If a player is dropped, remove the owner
            else:
                p_transaction_owner = ''
            # Add player transaction data to the transactions list
            p_transaction = {'date': transaction_date, 'type': p_transaction_type,
                             'owner': p_transaction_owner, 'player': p_transaction_name}
            transactions_list.append(p_transaction)

counter = 0
for transaction in transactions_list:
    counter += 1
    if transaction['type'] == 'trade':
        print(transaction)
