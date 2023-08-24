#! python

import openpyxl
import logging

logging.basicConfig(level=logging.DEBUG)


def getDraftResults(year):
    # os.chdir('.\\DraftResults')
    draft_wb = openpyxl.load_workbook('DraftResults.xlsx')
    draft_sheet = draft_wb[year]

    draft_results = []
    round_players = []
    # Iterate through rows of Excel Workbook
    for row in draft_sheet.iter_rows(min_row=1, min_col=1, max_col=3,
                                     values_only=True):

        # When the round changes
        if isinstance(row[0], str):
            # Update the current round
            curr_round = row[0].split()[1]
            curr_round = int(curr_round) - 1
            # Append players from current round into results list
            if round_players:
                draft_results.append(round_players)
                round_players = []

        # Insert players and owner into current round list
        if row[1] is not None:
            player = row[1].split("(")[0]
            owner = row[2].split(".")[0]
            round_players.append((player, owner))

    # Add the last round to the draft results
    if round_players:
        draft_results.append(round_players)

    # for round in draft_results:
    #     print(round)

    return draft_results
