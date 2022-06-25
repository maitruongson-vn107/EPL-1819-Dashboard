import data_loaders.graph_connection as gc
from utils.constant import DB


def getFixtures(game_week="All GWs"):
    if game_week == "All GWs":
        get_fixtures_gw_query = f"MATCH (t1: TEAM) -[h:HOME]-> (m: MATCH) <-[a: AWAY]- (t2:TEAM) " \
                                f"RETURN m.date_GMT, m.stadium_name, " \
                                f"m.home_team_name, m.away_team_name, " \
                                f"h.home_team_goal_count, a.away_team_goal_count " \
                                f"ORDER BY m.game_week, m.timestamp"
    else:
        get_fixtures_gw_query = f"MATCH (t1: TEAM) -[h:HOME]-> (m: MATCH {{game_week: \"{game_week}\"}}) <-[a: AWAY]- (t2:TEAM) " \
                                f"RETURN m.date_GMT, m.stadium_name, " \
                                f"m.home_team_name, m.away_team_name, " \
                                f"h.home_team_goal_count, a.away_team_goal_count " \
                                f"ORDER BY m.timestamp"

    query_results = gc.conn.query(get_fixtures_gw_query, db=DB)
    all_matches_details = []

    for rs in query_results:
        all_matches_details.append(dict(rs))
    return all_matches_details


print(len(getFixtures(game_week="All GWs")))


def getOneMatchByTeamNames(home_team_name: str, away_team_name: str):
    get_match_info_query = f"MATCH (t1:TEAM {{common_name: \"{home_team_name}\"}})" \
                           f" -[h:HOME]-> (m: MATCH) <-[a:AWAY]- " \
                           f"(t2:TEAM {{common_name: \"{away_team_name}\"}}) " \
                           f"RETURN m, h, a"
    query_results = gc.conn.query(get_match_info_query, db=DB)
    match_details = {}

    for rs in query_results:
        match_details.update(dict(rs["m"]))
        match_details.update(dict(rs["h"]))
        match_details.update(dict(rs["a"]))
    return match_details


def getAllMatchesByTeam(team_common_name: str):
    get_home_matches_query = f"match(t1:TEAM {{common_name: \"{team_common_name}\"}})-[h:HOME]->" \
                             f"(m:MATCH)<-[a:AWAY]-(t2:TEAM) " \
                             f"RETURN m.game_week, m.date_GMT, m.stadium_name, " \
                             f"m.home_team_name, m.away_team_name, " \
                             f"h.home_team_goal_count, a.away_team_goal_count"

    get_away_matches_query = f"match(t1:TEAM)-[h:HOME]->(m:MATCH)" \
                             f"<-[a:AWAY]-(t2:TEAM {{common_name: \"{team_common_name}\"}}) " \
                             f"RETURN m.game_week, m.date_GMT, m.stadium_name, " \
                             f"m.home_team_name, m.away_team_name, " \
                             f"h.home_team_goal_count, a.away_team_goal_count"

    home_rs = gc.conn.query(get_home_matches_query, db=DB)
    away_rs = gc.conn.query(get_away_matches_query, db=DB)

    all_matches = []
    for h_match in home_rs:
        all_matches.append(dict(h_match))
    for a_match in away_rs:
        all_matches.append(dict(a_match))

    all_matches = sorted(all_matches, key=lambda d: int(d["m.game_week"]))
    return all_matches


def getTeamBiggestWin(team_common_name: str):
    get_biggest_home_win_query = f"match(t1:TEAM {{common_name: \"{team_common_name}\"}})-[h:HOME]->" \
                                 f"(m:MATCH)<-[a:AWAY]-(t2:TEAM) " \
                                 f"RETURN m.date_GMT, m.stadium_name, " \
                                 f"m.home_team_name, m.away_team_name, " \
                                 f"h.home_team_goal_count, a.away_team_goal_count " \
                                 f"order by (toInteger(h.home_team_goal_count) - toInteger(a.away_team_goal_count)) " \
                                 f"desc limit 1"

    get_biggest_away_win_query = f"match(t1:TEAM)-[h:HOME]->(m:MATCH)" \
                                 f"<-[a:AWAY]-(t2:TEAM {{common_name: \"{team_common_name}\"}}) " \
                                 f"RETURN m.date_GMT, m.stadium_name, " \
                                 f"m.home_team_name, m.away_team_name, " \
                                 f"h.home_team_goal_count, a.away_team_goal_count " \
                                 f"order by (toInteger(a.away_team_goal_count) - toInteger(h.home_team_goal_count)) " \
                                 f"desc limit 1"

    home_biggest_win = dict(gc.conn.query(get_biggest_home_win_query, db=DB)[0])
    away_biggest_win = dict(gc.conn.query(get_biggest_away_win_query, db=DB)[0])

    return home_biggest_win, away_biggest_win


def getTeamBiggestLoss(team_common_name: str):
    get_biggest_home_loss_query = f"match(t1:TEAM {{common_name: \"{team_common_name}\"}})-[h:HOME]->" \
                                 f"(m:MATCH)<-[a:AWAY]-(t2:TEAM) " \
                                 f"RETURN m.date_GMT, m.stadium_name, " \
                                 f"m.home_team_name, m.away_team_name, " \
                                 f"h.home_team_goal_count, a.away_team_goal_count " \
                                 f"order by (toInteger(h.home_team_goal_count) - toInteger(a.away_team_goal_count)) " \
                                 f"limit 1"

    get_biggest_away_loss_query = f"match(t1:TEAM)-[h:HOME]->(m:MATCH)" \
                                 f"<-[a:AWAY]-(t2:TEAM {{common_name: \"{team_common_name}\"}}) " \
                                 f"RETURN m.date_GMT, m.stadium_name, " \
                                 f"m.home_team_name, m.away_team_name, " \
                                 f"h.home_team_goal_count, a.away_team_goal_count " \
                                 f"order by (toInteger(a.away_team_goal_count) - toInteger(h.home_team_goal_count)) " \
                                 f"limit 1"

    home_biggest_loss = dict(gc.conn.query(get_biggest_home_loss_query, db=DB)[0])
    away_biggest_loss = dict(gc.conn.query(get_biggest_away_loss_query, db=DB)[0])

    return home_biggest_loss, away_biggest_loss


def getTeamMostScoredMatch(team_common_name: str):
    get_most_scored_home_query = f"match(t1:TEAM {{common_name: \"{team_common_name}\"}})-[h:HOME]->" \
                                 f"(m:MATCH)<-[a:AWAY]-(t2:TEAM) " \
                                 f"RETURN m.date_GMT, m.stadium_name, " \
                                 f"m.home_team_name, m.away_team_name, " \
                                 f"h.home_team_goal_count, a.away_team_goal_count " \
                                 f"order by toInteger(h.home_team_goal_count) " \
                                 f"desc limit 1"

    get_most_scored_away_query = f"match(t1:TEAM)-[h:HOME]->(m:MATCH)" \
                                  f"<-[a:AWAY]-(t2:TEAM {{common_name: \"{team_common_name}\"}}) " \
                                  f"RETURN m.date_GMT, m.stadium_name, " \
                                  f"m.home_team_name, m.away_team_name, " \
                                  f"h.home_team_goal_count, a.away_team_goal_count " \
                                  f"order by toInteger(a.away_team_goal_count) " \
                                  f"desc limit 1"

    home_most_scored = dict(gc.conn.query(get_most_scored_home_query, db=DB)[0])
    away_most_scored = dict(gc.conn.query(get_most_scored_away_query, db=DB)[0])

    return home_most_scored, away_most_scored