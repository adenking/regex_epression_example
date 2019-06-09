import re
import pandas as pd

rx_dict = {
    'armor': re.compile(r'"melee" = (\d+)[ ,]+"bullet" = (\d+)[ ,]+"laser" = (\d+)[ ,]+"energy" = (\d+)[ ,]+"bomb" = (\d+)[ ,]+"bio" = (\d+)[ ,]+"rad" = (\d+)[ ,]+"fire" = (\d+)[ ,]+"acid" = (\d+)'),
    'name': re.compile(r'name = "([a-zA-Z ]+)"'),
    'end': re.compile(r'^/.+')
}


def _parse_line(line):
    """do a regex search per line"""

    for key, rx in rx_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    return None, None


def parse_file(filepath):
    """

    :param filepath:
    :return:
    """
    armor_matched = False
    name_matched = False
    data = []  # create an empty list to collect data
    with open(filepath, 'r') as file_object:
        for line in reversed(list(file_object)):
            key, match = _parse_line(line)
            if key == 'armor':
                melee = match.group(1)
                bullet = match.group(2)
                laser = match.group(3)
                energy = match.group(4)
                bomb = match.group(5)
                bio = match.group(6)
                rad = match.group(7)
                fire = match.group(8)
                acid = match.group(9)
                armor_matched = True
            if key == 'name':
                name = match.group(1)
                name_matched = True
            if key == 'end':
                if armor_matched is True and name_matched is True:
                    row = {
                        'melee': melee,
                        'bullet': bullet,
                        'laser': laser,
                        'energy': energy,
                        'bomb': bomb,
                        'bio': bio,
                        'rad': rad,
                        'fire': fire,
                        'acid': acid,
                        'name': name
                    }
                    data.append(row)
                armor_matched = False
                name_matched = False
    data = pd.DataFrame(data)

    data.set_index(['name', 'melee', 'bullet', 'laser', 'energy', 'bomb', 'bio', 'rad', 'fire', 'acid'], inplace=True)
    return data





filepath = 'C:\\Users\\adenk\\Documents\\Austation\\austation\\code\\modules\\clothing\\head\\helmet.dm'
data = parse_file(filepath)
filepath = 'C:\\Users\\adenk\\Documents\\Austation\\austation\\code\\modules\\clothing\\suits\\armor.dm'
data2 = parse_file(filepath)
filepath = 'C:\\Users\\adenk\\Documents\\Austation\\austation\\code\\modules\\clothing\\spacesuits\\hardsuit.dm'
data3 = parse_file(filepath)
filepath = 'C:\\Users\\adenk\\Documents\\Austation\\austation\\code\\modules\\clothing\\spacesuits\\miscellaneous.dm'
data4 = parse_file(filepath)
frames = [data, data2, data3, data4]
result = pd.concat(frames)

result.to_csv('C:\\Users\\adenk\\Documents\\data.csv')