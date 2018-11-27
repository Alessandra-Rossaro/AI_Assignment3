from agent import AlphaBetaAgent
import minimax
from math import inf


"""
Agent skeleton. Fill in the gaps.
"""


class MyAgent(AlphaBetaAgent):
    """
  This is the skeleton of an agent to play the Tak game.
  """
    # def iterative_deepening_search(self,state):
    #     for depth in range(0, 10):
    #         result = minimax.search(state, self)
    #         #if result!=

    def get_action(self, state, last_action, time_left):
        self.last_action = last_action
        self.time_left = time_left
        # qui aggiorna max depth
        return minimax.search(state, self)




    def successors(self, state):
        """The successors function must return (or yield) a list of
        pairs (a, s) in which a is the action played to reach the
        state s;"""
        actionsPlayer = state.get_current_player_actions()
        playerId = state.get_cur_player()
        listPairs = []
        for action in actionsPlayer:
            if state.is_action_valid(action):
                newState = state.copy()
                newState.apply_action(action)
                listPairs.append((action, newState))
        # if player == max (= me) order of list is decreasing, otherwise is increasing
        return sorted(listPairs, key=self.evaluate_successor, reverse=playerId == self.id)

    def evaluate_successor(self, element):
        return self.evaluate(element[1])

    """
  The cutoff function returns true if the alpha-beta/minimax
  search has to stop and false otherwise.
  """

    def cutoff(self, state, depth):
        if state.game_over_check():
            return True
        if depth == 1:
            return True
        else:
            return False

        # qui controlla se hai raggiunto max depth ( variabile di questa classe)

    """
  The evaluate function must return an integer value
  representing the utility function of the board.
  """

    def evaluate(self, state):
        myId = self.id
        countMine, countOtherPlayer = state.control_count()
        if myId == 0:
            diff = countMine - countOtherPlayer
        else:
            diff = countOtherPlayer - countMine
        if state.game_over_check():
            if myId == state.get_winner():
                return 1000
            else:
                return -1000

        else:
            return diff
