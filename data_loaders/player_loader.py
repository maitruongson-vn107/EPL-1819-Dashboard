import pandas as pd
import graph_connection as gc
import re
from tqdm import tqdm
from utils.constant import DB


def read_players_data():
    players_data = pd.read_csv("../csv/england-premier-league-players-2018-to-2019-stats.csv")
    sub_players_data = players_data[["full_name", "birthday_GMT",
                                     "position", "current_club", "nationality",
                                     "goals_overall", "goals_home", "goals_away",
                                     "assists_overall", "assists_home", "assists_away",
                                     "penalty_goals", "penalty_misses",
                                     "clean_sheets_overall", "clean_sheets_home", "clean_sheets_away",
                                     "conceded_overall", "conceded_home", "conceded_away",
                                     "yellow_cards_overall", "red_cards_overall",
                                     "rank_in_league_top_attackers", "rank_in_league_top_midfielders", "rank_in_league_top_defenders"]]

    return players_data, sub_players_data


def create_players_node_and_relationship(players_data, sub_players_data):
    for i in tqdm(range(len(sub_players_data))):
        one_player_dict = dict(sub_players_data.loc[i])
        relationship_dict = dict(players_data[["minutes_played_overall", "minutes_played_home", "minutes_played_away",
                                               "appearances_overall", "appearances_home", "appearances_away",
                                               "rank_in_club_top_scorer"]].loc[i])
        # CREATE NEW PLAYER NODE
        node_name = re.sub('[^a-zA-Z0-9 \n.]', '', one_player_dict["full_name"]).replace(" ", "")
        create_player_query = f"CREATE ({node_name}: PLAYER {{"
        for key in one_player_dict.keys():
            if key == "index":
                continue
            try:
                num_value = float(one_player_dict[key])
                create_player_query += f"{str(key)}: {num_value}, "
            except:
                create_player_query += f"{str(key)}: \"{one_player_dict[key]}\", "
        create_player_query = create_player_query[:-2] + "})"
        gc.conn.query(create_player_query, db=DB)

        # CREATE NEW PLAYER - TEAM RELATIONSHIP
        current_club = one_player_dict["current_club"]
        create_relationship_query = f"MATCH (p:PLAYER),(t:TEAM) " \
                                    f"WHERE p.full_name = \"{one_player_dict['full_name']}\" " \
                                    f"AND p.birthday_GMT = \"{one_player_dict['birthday_GMT']}\" " \
                                    f"AND t.common_name = \"{current_club}\" " \
                                    f"MERGE (p)-[r:PLAYED_IN {{"
        for key in relationship_dict.keys():
            create_relationship_query += f"{str(key)}: \"{relationship_dict[key]}\", "
        create_relationship_query = create_relationship_query[:-2] + "}]->(t) RETURN type(r), r.name"
        gc.conn.query(create_relationship_query, db=DB)
