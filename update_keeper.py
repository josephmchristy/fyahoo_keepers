#! python

import csv

old_value = {}
new_value = {}
updated_value = {}

# Get dict of "old" values
with open('updated_keepers.csv', mode='r') as file:
    reader = csv.reader(file)
    old_value = {rows[0]: rows[1] for rows in reader}

# Get dict of "updated" draft values
with open('updated_keepers.csv', mode='r') as file:
    reader = csv.reader(file)
    new_value = {rows[2]: rows[3] for rows in reader}

# For all the players in the old value list
for player in old_value:
    # If the player has a 5th round value and they were not drafted and held (i.e. value != 6)
    if int(old_value.get(player)) == 5 and int(new_value.get(player) != 6):
        # Tyler Boyd and Tyler Higbee are now 7th round value
        if player == 'Tyler Boyd' or player == 'Tyler Higbee':
            value = 7
        # Set their values to 6
        else:
            value = 6
    # If they were FA pickups (not drafted), set value to 6
    elif new_value.get(player) is None:
        value = 6
    # Otherwise, change to new updated value
    else:
        value = new_value.get(player)
    # Add to dict
    updated_value[player] = value

# Append dict to csv file
fieldnames = ['Player', 'Value']
with open('updated_keepers(1).csv', mode='a') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    for player in updated_value:
        writer.writerow({fieldnames[0]: player, fieldnames[1]: updated_value[player]})


# print(updated_value)
