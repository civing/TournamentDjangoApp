__author__ = 'Niklas Aronsson'
from collections import namedtuple
import random
import logging

logger = logging.getLogger('StandingsTable')


def create_player_data_dict(player_id):
    return {"id": player_id,
            "points": 0,
            "goals": 0,
            "won": 0,
            "lost": 0,
            "draw": 0,
            "goals_against": 0,
            "games_played": 0}


class StandingsTable(object):
    """
    An object corresponding to the current status in the standings table.
    """
    def __init__(self, tournament_id):
        self.player_data = {}
        self.games = []
        self.tournament_id = tournament_id
        self.player_data_tuple = namedtuple("playerData",
                                            "name id points games_played games_won games_" +
                                            "draw games_lost goals goals_against")

    def _get_data_dict_from_game_list(self, game_list):
        player_data = {}
        for game in game_list:
            away_score_to_add = 0
            home_score_to_add = 0
            if game.home_player.name not in player_data:
                player_data[game.home_player.name] = create_player_data_dict(game.home_player.id)
            if game.away_player.name not in player_data:
                player_data[game.away_player.name] = create_player_data_dict(game.away_player.id)
            if not game.played:
                continue

            if game.wo_home or game.wo_away:
                # If both players have done W0 award them no points and a -5 goal difference.
                if game.wo_home and not game.wo_away:
                    away_score_to_add = 2
                    player_data[game.home_player.name]["goals_against"] += 5
                    player_data[game.away_player.name]["won"] += 1
                    player_data[game.home_player.name]["lost"] += 1
                elif game.wo_away and not game.wo_home:
                    home_score_to_add = 2
                    player_data[game.away_player.name]["goals_against"] += 5
                    player_data[game.home_player.name]["won"] += 1
                    player_data[game.away_player.name]["lost"] += 1
                else:
                    player_data[game.away_player.name]["goals_against"] += 5
                    player_data[game.home_player.name]["goals_against"] += 5
                    player_data[game.away_player.name]["lost"] += 1
                    player_data[game.home_player.name]["lost"] += 1

            else:
                if game.home_score == game.away_score:
                    away_score_to_add = 1
                    home_score_to_add = 1
                    player_data[game.away_player.name]["draw"] += 1
                    player_data[game.home_player.name]["draw"] += 1
                elif game.home_score > game.away_score:
                    home_score_to_add = 2
                    player_data[game.away_player.name]["lost"] += 1
                    player_data[game.home_player.name]["won"] += 1
                elif game.away_score > game.home_score:
                    away_score_to_add = 2
                    player_data[game.away_player.name]["won"] += 1
                    player_data[game.home_player.name]["lost"] += 1
                player_data[game.home_player.name]["goals"] += game.home_score
                player_data[game.away_player.name]["goals"] += game.away_score
                player_data[game.home_player.name]["goals_against"] += game.away_score
                player_data[game.away_player.name]["goals_against"] += game.home_score

            player_data[game.home_player.name]["points"] += home_score_to_add
            player_data[game.away_player.name]["points"] += away_score_to_add
            player_data[game.home_player.name]["games_played"] += 1
            player_data[game.away_player.name]["games_played"] += 1
        return player_data

    def _return_named_tuples_from_game_list(self, game_list):
        """
        Given list of played games this method calculates every players stats and returns a
        list of the "playerData" named tuple. This will typically later be sorted somewhere else.

        :param game_list:
        :return: a list of playerData named tuples.
        """
        logger.info("Get player statistics from a list of games.")
        player_data = self._get_data_dict_from_game_list(game_list)
        player_data_list = []
        for player_name, player_stats in player_data.items():
            player_data_list.append(self._make_named_tuple_from_player_dict(player_name, player_stats))
        return player_data_list

    def get_standings_for_games(self, game_list):
        """
        Calculates the standings for all the players included in the specified games. Returns an unordered list
        of the playerData named tuple.

        :param game_list: List of games.
        :return: A list of the playerData named tuple.
        """

        return self._return_named_tuples_from_game_list(game_list)

    def _make_named_tuple_from_player_dict(self, player_name, player_dict):
        return self.player_data_tuple._make([player_name,
                                             player_dict["id"],
                                             player_dict["points"],
                                             player_dict['games_played'],
                                             player_dict['won'],
                                             player_dict['draw'],
                                             player_dict['lost'],
                                             player_dict['goals'],
                                             player_dict['goals_against']])

    def add_game(self, game):
        if game.played:
            self.games.append(game)

    def update(self):
        """
        Saves player data from all the played games in self.player_data

        :return:
        """

        self.player_data = self._get_data_dict_from_game_list(self.games)

    def get_standing(self):
        logger.info("Get standing with {0} games played.".format(len(self.games)))
        result_list = []
        if not self.player_data:
            self.update()
        available_points = sorted(set([p['points'] for p in self.player_data.values()]), reverse=True)
        for point_value in available_points:
            users = [k for k, v in self.player_data.items() if self.player_data[k]['points'] == point_value]
            logger.info("There are {1} players with {0} points".format(point_value, len(users)))
            current_users = []
            for u in users:
                logger.info(u"Add user data for: {0}".format(u))
                # TODO: Clean up!
                current = self.player_data[u]
                current_users.append(self.player_data_tuple._make([u,
                                                                   current["id"],
                                                                   current["points"],
                                                                   current['games_played'],
                                                                   current['won'],
                                                                   current['draw'],
                                                                   current['lost'],
                                                                   current['goals'],
                                                                   current['goals_against']]))
            current_users.reverse()
            sorted_list = self.get_ranking_for_players(current_users)
            if sorted_list:
                result_list.extend(sorted_list)
            else:
                result_list.extend(current_users)
        return result_list

    def _sort_items(self, named_tuple_list):
        """
        Sort the items in the named tuple according to:

        goal difference
        goals made

        or if that fails make it random.

        :param named_tuple_list:
        :return:
        """
        goal_difference = [p.goals - p.goals_against for p in named_tuple_list]
        logger.info("Sort rankings on goal diff / goal made.")
        if len(set(goal_difference)) != 1:
            logger.info("Sort items on goal difference")
            return named_tuple_list.sort(key=lambda x: x.goals - x.goals_against, reverse=True)
        else:
            goals_made = [p.goals for p in named_tuple_list]
            if len(goals_made) == len(set(goals_made)):
                logger.info("Goal difference is equal. Sort items on goals made")
                return named_tuple_list.sort(key=lambda x: x.goals, reverse=True)
            else:
                logger.info("Goal difference and goals made is equal. Shuffle!")
                return random.shuffle(named_tuple_list)

    def get_ranking_for_players(self, player_data_list):
        """
        Checks which of the players is ranked higher. Treat each list as a subset of the table.

        :param player_list: list of player id's.

        :return:
        """
        logger.info("Get rankings for players.")
        # Get games which only current players have played.
        uid_list = [p.id for p in player_data_list]
        current_games = [g for g in self.games if (g.home_player.id in uid_list and g.away_player.id in uid_list)]
        for g in current_games:
            logger.info(u'Checking game "{0}" vs "{1}"'.format(g.home_player.name.rstrip(), g.away_player.name.rstrip()))
        current_games_data = self.get_standings_for_games(current_games)
        # Check if there are all players are internally ranked. this only happens if all have played each other.
        if len(current_games) != len(player_data_list):
            logger.info("Unable to use internal table to rank players. All games have not been played.")
            return self._sort_items(player_data_list)
        if not current_games_data:
            logger.info("There are no played games for these players. Rank using goal difference.")
            return self._sort_items(current_games_data)
        else:
            logger.info("Sort player list on points.")
            current_games_data.sort(key=lambda x: x.points, reverse=True)
            point_list = [d.points for d in current_games_data]
            if len(point_list) != len(set(point_list)):
                logger.info("Current game data contains players with equal points.")
                return self._sort_items(current_games_data)
            else:
                logger.info("Current game data contains no players with equal points. Use internal rank.")
                sorted_list = []
                for player in current_games_data:
                    sorted_list.extend([p for p in player_data_list if p.id == player.id])
                return sorted_list
