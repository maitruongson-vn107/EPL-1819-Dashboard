import data_loaders.graph_connection as gc
from utils.constant import DB


def getTopScorers():
    get_top_scorers_query = "MATCH(p:PLAYER) RETURN p ORDER BY p.goals_overall DESC LIMIT 10"
    query_results = gc.conn.query(get_top_scorers_query, db=DB)
    top_scorers_list = []
    for player_record in query_results:
        player_data = player_record["p"]
        top_scorers_list.append((player_data["full_name"].split(" ")[-1],
                                 player_data["current_club"],
                                 int(player_data["goals_overall"])))
    return top_scorers_list


def getTeamTopScorers(team_common_name: str):
    get_top_scorers_query = f"MATCH(p:PLAYER)-->(t:TEAM {{common_name: \"{team_common_name}\"}}) " \
                            f"RETURN p ORDER BY p.goals_overall DESC LIMIT 10"
    query_results = gc.conn.query(get_top_scorers_query, db=DB)
    top_scorers_list = []
    for player_record in query_results:
        player_data = player_record["p"]
        top_scorers_list.append((player_data["full_name"],
                                 int(player_data["goals_overall"])))
    return top_scorers_list


def getTopAssists():
    get_top_assists_query = "MATCH(p:PLAYER) RETURN p ORDER BY p.assists_overall DESC LIMIT 10"
    query_results = gc.conn.query(get_top_assists_query, db=DB)
    top_assists_list = []
    for player_record in query_results:
        player_data = player_record["p"]
        top_assists_list.append((player_data["full_name"].split(" ")[-1],
                                 player_data["current_club"],
                                 int(player_data["assists_overall"])))
    return top_assists_list


def getTeamTopAssists(team_common_name: str):
    get_top_assists_query = f"MATCH(p:PLAYER)-->(t:TEAM {{common_name: \"{team_common_name}\"}}) " \
                            f"RETURN p ORDER BY p.assists_overall DESC LIMIT 10"
    query_results = gc.conn.query(get_top_assists_query, db=DB)
    top_assists_list = []
    for player_record in query_results:
        player_data = player_record["p"]
        top_assists_list.append((player_data["full_name"],
                                 int(player_data["assists_overall"])))
    return top_assists_list


def getTopCleanSheets():
    get_top_clean_sheets_query = "MATCH(p:PLAYER {position: \"Goalkeeper\"}) " \
                                 "RETURN p ORDER BY p.clean_sheets_overall DESC LIMIT 10"
    query_results = gc.conn.query(get_top_clean_sheets_query, db=DB)
    top_clean_sheets_list = []
    for player_record in query_results:
        player_data = player_record["p"]
        top_clean_sheets_list.append((player_data["full_name"].split(" ")[-1],
                                      player_data["current_club"],
                                      int(player_data["clean_sheets_overall"])))
    return top_clean_sheets_list


def getTeamAllPlayers(team_common_name: str):
    get_team_all_players_query = f"MATCH (p:PLAYER)-[r]->(t:TEAM {{common_name: \"{team_common_name}\"}})" \
                                 f"RETURN p, r"
    query_results = gc.conn.query(get_team_all_players_query, db=DB)
    players_list = []
    for player_rs in query_results:
        player_dict = {}
        player_dict.update(dict(player_rs['p']))
        player_dict.update(dict(player_rs['r']))
        players_list.append(player_dict)

    return players_list