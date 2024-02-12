table_b_dict = dict()
table_b_dict['Spain'] = {}
table_b_dict['Portugal'] = {}
table_b_dict['Iran'] = {}
table_b_dict['Morocco'] = {}

list_of_matches = [
    "Iran_Spain",
    "Iran_Portugal",
    "Iran_Morocco",
    "Spain_Portugal",
    "Spain_Morocco",
    "Portugal_Morocco"
]
dict_of_matches = {}
for match in list_of_matches:
    dict_of_matches[match] = input()

for key, val in dict_of_matches.items():
    team1, team2 = key.split("_")
    point_team1, point_team2 = map(int, val.split("-"))

    # calc wins, draws, losses and points
    if point_team1 > point_team2:
        table_b_dict[team1]['wins'] = table_b_dict[team1].get('wins', 0) + 1
        table_b_dict[team2]['losses'] = table_b_dict[team2].get('losses', 0) + 1
        table_b_dict[team1]['points'] = table_b_dict[team1].get('points', 0) + 3
    elif point_team1 < point_team2:
        table_b_dict[team1]['losses'] = table_b_dict[team1].get('losses', 0) + 1
        table_b_dict[team2]['wins'] = table_b_dict[team2].get('wins', 0) + 1
        table_b_dict[team2]['points'] = table_b_dict[team2].get('points', 0) + 3
    else:
        table_b_dict[team1]['draws'] = table_b_dict[team1].get('draws', 0) + 1
        table_b_dict[team2]['draws'] = table_b_dict[team2].get('draws', 0) + 1
        table_b_dict[team1]['points'] = table_b_dict[team1].get('points', 0) + 1
        table_b_dict[team2]['points'] = table_b_dict[team2].get('points', 0) + 1

    # calc goal difference
    table_b_dict[team1]['goal_difference'] = table_b_dict[team1].get('goal_difference', 0) + point_team1 - point_team2
    table_b_dict[team2]['goal_difference'] = table_b_dict[team2].get('goal_difference', 0) + point_team2 - point_team1

# create final list
final_list = []
for key, val in table_b_dict.items():
    final_list.append((key,
                       val.get('wins', 0),
                       val.get('losses', 0),
                       val.get('draws', 0),
                       val.get('goal_difference', 0),
                       val.get('points', 0)))

# sort final list points, wins, team name in descending order
final_list.sort(key=lambda x: (-x[-1], -x[1], x[0]))

# print final list with formatting "Spain  wins:{} , loses:{} , draws:{} , goal difference:{} , points:{}"
for team in final_list:
    print(
        f"{team[0]}  wins:{team[1]} , loses:{team[2]} , draws:{team[3]} , goal difference:{team[4]} , points:{team[5]}")
