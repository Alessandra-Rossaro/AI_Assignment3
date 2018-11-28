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

    n = 0  # counter to check the time elapsed and consiquently change the maxDepth
    maxDepth = 10
    minDepth = 3

    # def iterative_deepening_search(self,state):
    #     for depth in range(0, 10):
    #         result = minimax.search(state, self)
    #         #if result!=

    def get_action(self, state, last_action, time_left):
        self.last_action = last_action
        self.time_left = time_left  # in seconds
        global n
        global maxDepth
        global minDepth
        total_time = 300  # 5min = 5*60sec = 300sec
        interval = 2 ** n
        # update maxDepth
        if time_left < total_time / interval:
            n += 1
            maxDepth = max(maxDepth / interval, minDepth)

        return minimax.search(state, self)

    def successors(self, state):
        """The successors function must return (or yield) a list of
        pairs (a, s) in which a is the action played to reach the
        state s;"""
        actionsPlayer = state.get_current_player_actions()
        player_id = state.get_cur_player()
        listPairs = []
        for action in actionsPlayer:
            if state.is_action_valid(action):
                newState = state.copy()
                newState.apply_action(action)
                listPairs.append((action, newState))
        # if player == max (= me) order of list is decreasing, otherwise is increasing
        return sorted(listPairs, key=self.evaluate_successor, reverse=player_id == self.id)

    def evaluate_successor(self, element):
        return self.evaluate(element[1])

    """
  The cutoff function returns true if the alpha-beta/minimax
  search has to stop and false otherwise.
  """

    def cutoff(self, state, depth):
        global maxDepth
        if state.game_over_check():
            return True
        # check if you reached maxDepth
        if depth == maxDepth:
            return True
        else:
            return False

    """
  The evaluate function must return an integer value
  representing the utility function of the board.
  """

    def evaluate(self, state):
        my_id = self.id

        # FIRST FEATURE: difference between topBlack and topWhite
        countMine, countOtherPlayer = state.control_count()
        if my_id == 0:
            diff = countMine - countOtherPlayer
        else:
            diff = countOtherPlayer - countMine

        # SECOND FEATURE




        if state.game_over_check():
            if my_id == state.get_winner():
                return 1000
            else:
                return -1000

        else:
            return diff

    def how_many_stones_miss_and_admissible_cells(self, state):
        my_id = self.id
        other_id = 1 - my_id
        cur_player = state.get_cur_player()  #CHE DIFFERENZA C'E' TRA ID E CURR_PLAYER
        count_admissible_cells = 0
        for row in range(0, state.size):
            for col in range(0, state.size):
                if state.is_empty(row, col):  # if is empty
                    count_admissible_cells += 1
                else:
                    piece_type, owner = self.board[row][col].top()
                    if owner == other_id:
                        if piece_type != 2:  # 2 is the CAPSTONE
                            count_admissible_cells += 1

        return count_admissible_cells
