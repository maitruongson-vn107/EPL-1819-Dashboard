from . import graph_connection as gc
from .team_loader import read_teams_data, create_teams_node
from .player_loader import read_players_data, create_players_node_and_relationship
from .matches_loader import read_matches_data, create_matches_node_and_relationship
from utils.constant import DB


def reset_graphs():
    query = "MATCH(n) DETACH DELETE n"
    gc.conn.query(query, db=DB)


def main():
    reset_graphs()
    print("DATA LOADER START: ")

    team_data = read_teams_data()
    create_teams_node(team_data)

    players_data, sub_players_data = read_players_data()
    create_players_node_and_relationship(players_data, sub_players_data)

    matches_data, sub_matches_data = read_matches_data()
    create_matches_node_and_relationship(matches_data, sub_matches_data)\


