import numpy as np
import matplotlib.pyplot as plt


class Game(object):
    def __init__(self, id, prob_head):
        self._id = id
        self._rnd = np.random
        self._rnd.seed(id)
        self._probHead = prob_head  # probability of flipping a head
        self._countWins = 0  # number of wins, set to 0 to begin

    def simulate(self, n_of_flips):

        count_tails = 0  # number of consecutive tails so far, set to 0 to begin

        # flip the coin 20 times
        for i in range(n_of_flips):

            # in the case of flipping a heads
            if self._rnd.random_sample() < self._probHead:
                if count_tails >= 2:  # if the series is ..., T, T, H
                    self._countWins += 1  # increase the number of wins by 1
                count_tails = 0  # the tails counter needs to be reset to 0 because a heads was flipped

            # in the case of flipping a tails
            else:
                count_tails += 1  # increase tails count by one

        return CoinOutcomes(self)

    def get_reward(self):
        # calculate the reward from playing a single game
        return 100 * self._countWins - 250


class SetOfGames:
    def __init__(self, prob_head, n_games):
        self._gameRewards = []  # create an empty list where rewards will be stored

        # simulate the games
        for n in range(n_games):
            # create a new game
            game = Game(id=n, prob_head=prob_head)
            # simulate the game with 20 flips
            game.simulate(20)
            # store the reward
            self._gameRewards.append(game.get_reward())


class CoinOutcomes:
    def __init__(self, simulated_cohort):
        # extracts outcomes of a simulated cohort
        self._simulatedCohort = simulated_cohort

    def get_sample_path(self):
        # sample path
        n_rewards = SamplePathSupport.SamplePathBatchUpdate("Expected Reward", 0)

        # update sample path
        for obs in self._simulatedCohort.get_game_rewards():
            n_rewards.record(obs, 1)

        return n_rewards

FigSupport.graph_histogram(observations=game.get_reward)

# run trail of 1000 games to calculate expected reward
games = SetOfGames(prob_head=0.5, n_games=1000)
