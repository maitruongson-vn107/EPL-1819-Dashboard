import pandas as pd
from . import graph_connection as gc
import re
from tqdm import tqdm
from utils.constant import DB


def read_matches_data():
    matches_data = pd.read_csv("csv/england-premier-league-matches-2018-to-2019-stats.csv")
    sub_matches_data = matches_data[["timestamp", "date_GMT", "attendance",
                                     "home_team_name", "away_team_name", "referee", "game_week", "stadium_name",
                                     "total_goal_count", "total_goals_at_half_time"]]

    return matches_data, sub_matches_data


def create_matches_node_and_relationship(matches_data, sub_matches_data):
    for i in tqdm(range(len(sub_matches_data))):
        one_match_dict = dict(sub_matches_data.loc[i])

        home_team_dict = dict(matches_data[[
            "home_team_goal_count", "home_team_goal_count_half_time",
            "home_team_corner_count", "home_team_yellow_cards", "home_team_red_cards",
            "home_team_first_half_cards", "home_team_second_half_cards",
            "home_team_shots", "home_team_shots_on_target",
            "home_team_fouls", "home_team_possession", "team_a_xg"]].loc[i])

        away_team_dict = dict(matches_data[[
            "away_team_goal_count", "away_team_goal_count_half_time",
            "away_team_corner_count", "away_team_yellow_cards", "away_team_red_cards",
            "away_team_first_half_cards", "away_team_second_half_cards",
            "away_team_shots", "away_team_shots_on_target",
            "away_team_fouls", "away_team_possession", "team_b_xg"]].loc[i])

        # CREATE MATCHES NODE
        node_name = re.sub('[^a-zA-Z0-9 \n.]', '', one_match_dict["home_team_name"] + one_match_dict["away_team_name"]) \
            .replace(" ", "")

        create_match_query = f"CREATE ({node_name}: MATCH {{"
        for key in one_match_dict.keys():
            if key == "index":
                continue
            create_match_query += f"{str(key)}: \"{one_match_dict[key]}\", "
        create_match_query = create_match_query[:-2] + "})"
        gc.conn.query(create_match_query, db=DB)

        # CREATE HOME TEAM-MATCH RELATIONSHIP
        game_week = one_match_dict["game_week"]
        home_team_name = one_match_dict["home_team_name"]

        create_home_relationship_query = f"MATCH(t:TEAM), (m:MATCH) " \
                                         f"WHERE t.common_name = \"{home_team_name}\" " \
                                         f"AND m.home_team_name = \"{home_team_name}\" " \
                                         f"AND m.game_week = \"{game_week}\" " \
                                         f"MERGE (t)-[h:HOME {{"

        for key in home_team_dict.keys():
            create_home_relationship_query += f"{str(key)}: \"{home_team_dict[key]}\", "
        create_home_relationship_query = create_home_relationship_query[:-2] + "}]->(m) RETURN type(h), h.name"
        gc.conn.query(create_home_relationship_query, db=DB)

        away_team_name = one_match_dict["away_team_name"]
        create_away_relationship_query = f"MATCH(t:TEAM), (m:MATCH) " \
                                         f"WHERE t.common_name = \"{away_team_name}\" " \
                                         f"AND m.away_team_name = \"{away_team_name}\" " \
                                         f"AND m.game_week = \"{game_week}\" " \
                                         f"MERGE (t)-[h:AWAY {{"

        for key in away_team_dict.keys():
            create_away_relationship_query += f"{str(key)}: \"{away_team_dict[key]}\", "
        create_away_relationship_query = create_away_relationship_query[:-2] + "}]->(m) RETURN type(h), h.name"
        gc.conn.query(create_away_relationship_query, db=DB)
