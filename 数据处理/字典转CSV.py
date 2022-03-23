import csv

my_list = [{'players.vis_name': 'Khazri', 'players.role': 'Midfielder', 'players.country': 'Tunisia',
            'players.last_name': 'Khazri', 'players.player_id': '989', 'players.first_name': 'Wahbi',
            'players.date_of_birth': '08/02/1991', 'players.team': 'Bordeaux'},
           {'players.vis_name': 'Khazri', 'players.role': 'Midfielder', 'players.country': 'Tunisia',
            'players.last_name': 'Khazri', 'players.player_id': '989', 'players.first_name': 'Wahbi',
            'players.date_of_birth': '08/02/1991', 'players.team': 'Sunderland'},
           {'players.vis_name': 'Lewis Baker', 'players.role': 'Midfielder', 'players.country': 'England',
            'players.last_name': 'Baker', 'players.player_id': '9574', 'players.first_name': 'Lewis',
            'players.date_of_birth': '25/04/1995', 'players.team': 'Vitesse'}
           ]


# write nested list of dict to csv
def nestedlist2csv(my_list, out_file):
    with open(out_file, 'w') as f:  # 问题： 这里用wb写入会报错
        writer = csv.writer(f, dialect='excel')
        fieldnames = list(my_list[0].keys())  # solve the problem to automatically write the header
        print(fieldnames)
        print(type(fieldnames))
        writer.writerow(fieldnames)

        # for row in my_list:
        #     writer.writerow(list(row.values()))


nestedlist2csv(my_list, '11.csv')
