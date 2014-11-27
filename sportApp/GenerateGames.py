__author__ = 'Niklas Aronsson'
import logging
import datetime
import random
from sportApp.models import Game, Player

logger = logging.getLogger('GenerateGames')


class GenerateGames(object):
    """
    Generates a list of games given a list of Players. Each player will play once against the other.
    """
    def __init__(self, player_list, division, start_date, tournament):
        self.player_list = list(player_list)
        self.division = division
        self.start_date = start_date
        self.tournament_id = tournament
        logger.info("GenerateGames __init__ with {0} players for div: {1} tournament id: {2}".format(
            len(self.player_list), division.name, self.tournament_id))
        self.generated_games = []
        self._generate_games_list()

    def _increment_date(self, date):
        """
        Returns the next week day.

        :param date:
        :return:
        """
        next_day = date + datetime.timedelta(days=1)
        if next_day.isoweekday() in [6, 7]:
            next_day = next_day + datetime.timedelta(days=8 - next_day.isoweekday())
        return next_day

    def _generate_games_list(self):
        current_date = self.start_date
        logger.info("Players in current division:")
        for p in self.player_list:
            logger.info(u"{0}".format(p.name))

        # TODO: Make the games as martins excel-sheet. then remove this at the start of the next
        # TODO: tournament
        if len(self.player_list) == 8:
            index_list = [[0, 1], [2, 3], [4, 5], [6, 7],
                          [0, 2], [1, 3], [4, 6], [5, 7],
                          [0, 3], [1, 2], [4, 7], [5, 6],
                          [0, 4], [1, 5], [2, 6], [3, 7],
                          [0, 5], [1, 6], [2, 7], [3, 4],
                          [0, 6], [1, 7], [2, 4], [3, 5],
                          [0, 7], [1, 4], [2, 5], [3, 6]]
        else:
            index_list = [[0, 1], [2, 3], [4, 5],
                          [0, 2], [1, 3], [4, 6],
                          [0, 3], [1, 2], [5, 6],
                          [0, 4], [1, 5], [2, 6],
                          [0, 5], [1, 6], [3, 4],
                          [0, 6], [2, 4], [3, 5],
                          [1, 4], [2, 5], [3, 6]]
        counter = 1
        for home_index, away_index in index_list:
            g = Game(home_player=self.player_list[home_index],
                     away_player=self.player_list[away_index],
                     division=self.division, date=current_date)
            g.save()
            self.generated_games.append(g)
            if not counter % 2:
                logger.info("Date counter: {0} increment date".format(counter))
                current_date = self._increment_date(current_date)
            counter += 1
        return

        # Remove the above later!

        for i, player in enumerate(self.player_list):
            opponents = self.player_list[i + 1:]
            if opponents:
                for o in opponents:
                    logger.info(u"Adding game: {0} vs {1}".format(player.name, o.name))
                    dates.append(current_date)
                    g = Game(home_player=player, away_player=o, division=self.division, date=current_date)
                    g.save()
                    self.generated_games.append(g)
                    game_counter += 1
                    if not game_counter % 2:
                        # calculate next game date.
                        current_date = current_date + datetime.timedelta(days=1)
                        if current_date.isoweekday() in [6, 7]:
                            current_date = current_date + datetime.timedelta(days=8 - current_date.isoweekday())
            else:
                logger.info("No remaining matches")
            current_date = current_date + datetime.timedelta(days=1)
        #shuffle the list
        for i in range(5):
           random.shuffle(self.generated_games)
        for i, game in enumerate(self.generated_games):
            game.date = dates[i]
            game.save()
        #print self.generated_games
