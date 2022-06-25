import pandas as pd
from . import graph_connection as gc
import re
from tqdm import tqdm
from utils.constant import DB


def read_teams_data():
    teams_data = pd.read_csv("csv/england-premier-league-teams-2018-to-2019-stats.csv")
    teams2_data = pd.read_csv("csv/england-premier-league-teams2-2018-to-2019-stats.csv")
    matches_data = pd.read_csv("csv/england-premier-league-matches-2018-to-2019-stats.csv")

    stadiums_data = matches_data[["home_team_name", "stadium_name"]].drop_duplicates()
    stadiums_data.columns = ["common_name", "stadium_name"]
    stadiums_data = stadiums_data.drop(stadiums_data.index[13])

    team_sub_data = teams_data[["team_name", "matches_played",
                                "league_position", "league_position_home", "league_position_away",
                                "wins", "wins_home", "wins_away",
                                "draws", "draws_home", "draws_away",
                                "losses", "losses_home", "losses_away",
                                "goals_scored", "goals_conceded", "goal_difference",
                                "goals_scored_home", "goals_scored_away",
                                "goals_conceded_home", "goals_conceded_away",
                                "goal_difference_home", "goal_difference_away"]]

    team2_sub_data = teams2_data[["team_name", "common_name", "country",
                                  "average_attendance_overall", "average_attendance_home", "average_attendance_away"]]

    team_full_data = pd.merge(team_sub_data, team2_sub_data, on="team_name")
    team_full_data = pd.merge(team_full_data, stadiums_data, on="common_name").sort_values('team_name').reset_index()
    team_full_data["points"] = team_full_data["wins"].astype(int) * 3 + team_full_data["draws"].astype(int)
    return team_full_data


def create_teams_node(team_full_data):
    for i in tqdm(range(len(team_full_data))):
        one_team_dict = dict(team_full_data.loc[i])
        node_name = re.sub('[^a-zA-Z0-9 \n.]', '', one_team_dict["team_name"]).replace(" ", "")
        query = f"CREATE ({node_name}: TEAM {{"
        for key in one_team_dict.keys():
            if key == "index":
                continue
            query += f"{str(key)}: \"{one_team_dict[key]}\", "
        query = query[:-2] + "})"
        gc.conn.query(query, db=DB)


