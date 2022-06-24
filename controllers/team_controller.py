import data_loaders.graph_connection as gc


def getTeamsData():
    get_team_query = "MATCH(t:TEAM) return t"
    query_results = gc.conn.query(get_team_query, db="neo4j")
    teams_data = []
    for team_record in query_results:
        team_info = team_record["t"]
        teams_data.append(team_info)
    return teams_data


def getTeamInfo(team_common_name: str):
    get_team_info_query = f"MATCH (t: TEAM {{ common_name: \"{team_common_name}\" }}) " \
                          f"return t"
    query_results = gc.conn.query(get_team_info_query, db="neo4j")
    team_info = dict(query_results[0]["t"])
    return team_info


def getTeamPlayersInfo(team_common_name: str):
    get_team_players_query = f"MATCH (: TEAM {{ common_name: \"{team_common_name}\" }}) -- (p: PLAYER) return p"
    query_results = gc.conn.query(get_team_players_query)
    team_players = []
    for player_record in query_results:
        player_info = dict(player_record["p"])
        team_players.append(player_info)
    return team_players