import random


class Person:
    def __init__(self, name):
        self.name = name


class Player(Person):
    Base_team_name = ['A', 'B']
    Count_team_A = 0
    Count_team_B = 0

    def __init__(self, name):
        super().__init__(name)
        self.team = None
        self.set_team()

    def set_team(self):
        this_team = random.choices(Player.Base_team_name, weights=(11 - Player.Count_team_A, 11 - Player.Count_team_B),
                                   k=1)
        if this_team[0] == 'A':
            Player.Count_team_A += 1
        else:
            Player.Count_team_B += 1

        self.team = this_team[0]

    def get_info(self):
        return "Name of player: {} | Team: {}".format(self.name, self.team)


list_name_of_players = ["حسین", "مازیار", "اکبر", "نیما", "مهدی", "فرهاد", "محمد", "خشایار", "میلاد", "مصطفی", "امین",
                        "سعید", "پویا", "پوریا", "رضا", "علی", "بهزاد", "سهیل", "بهروز", "شهروز", "سامان", "محسن"]

list_of_players = []
for name in list_name_of_players:
    list_of_players.append(Player(name))

for player in list_of_players:
    print(player.get_info())

# If need to check the count of each team please uncomment the following line
# print(Player.Count_team_A, Player.Count_team_B)


