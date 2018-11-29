from agent import AlphaBetaAgent
from myqueue import Queue
import minimax
import math
import tak
import mystack

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

    def __init__(self):
        self.n = 0  # counter to check the time elapsed and consequently change the maxDepth
        self.maxDepth = 3
        self.minDepth = 2
        self.behaviour = False
        self.adversaryPlacedCapstones = []  # inside there are (x,y) elements
        self.total_time = 300  # 5min = 5*60sec = 300sec

    def get_action(self, state, last_action, time_left):
        self.last_action = last_action
        self.time_left = time_left  # in seconds
        interval = 2 ** (self.n + 1)
        interval2 = 2 ** self.n

        if state.turn <= 2 * (state.size - 1):
            self.behaviour = True
        else:
            self.behaviour = False
            # update maxDepth
            if time_left <= self.total_time / interval:
                self.n += 1
                self.maxDepth = max(self.maxDepth / interval2, self.minDepth)

        if state.turn <= 2 * (state.size - 1):
            self.behaviour = True
        else:
            self.behaviour = False

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

        if self.behaviour == True:
            if depth == 1:
                return True
            else:
                return False
        # check if you reached maxDepth
        if depth == self.maxDepth:
            return True
        else:
            return False

    """
  The evaluate function must return an integer value
  representing the utility function of the board.
  """

    def evaluate(self, state):

        myId = self.id
        otherId = 1 - myId

        # FIRST FEATURE: difference between topBlack and topWhite
        weightDiff = 150/state.size**2
        countMine, countOtherPlayer = state.control_count()
        if myId == 0:
            diff = countMine - countOtherPlayer
        else:
            diff = countOtherPlayer - countMine

        # SECOND FEATURE
        weightCountAdmissibleCells = 150/state.size**2
        countAdmissibleCellsMyId = self.how_many_stones_miss_and_admissible_cells(state, myId)
        countAdmissibleCellsOtherId = self.how_many_stones_miss_and_admissible_cells(state, otherId)
        """
        # THIRD FEATURE and FOURTH FEATURE
        weightDistanceDoneToGoal = 350 / state.size
        weightDistanceDoneToGoalWithStack = 350 / state.size
        minDistanceFromGoal, minDistanceFromGoalWithStack = self.myCheck_H_V_path(myId, state)
        distanceDoneToGoalMyId = state.size - minDistanceFromGoal
        distanceDoneToGoalWithStackMyId = state.size - minDistanceFromGoalWithStack

        minDistanceFromGoal, minDistanceFromGoalWithStack = self.myCheck_H_V_path(otherId, state)
        distanceDoneToGoalOtherId = state.size - minDistanceFromGoal
        distanceDoneToGoalWithStackOtherId = state.size - minDistanceFromGoalWithStack
        """



        if state.game_over_check():
            if myId == state.get_winner():
                return 1000
            else:
                return -1000

        else:
            return weightDiff * diff \
                   + weightCountAdmissibleCells * countAdmissibleCellsMyId - weightCountAdmissibleCells * countAdmissibleCellsOtherId
                   #+ weightDistanceDoneToGoal * distanceDoneToGoalMyId - weightDistanceDoneToGoal * distanceDoneToGoalOtherId \
                   #+ weightDistanceDoneToGoalWithStack * distanceDoneToGoalWithStackMyId - weightDistanceDoneToGoalWithStack * distanceDoneToGoalWithStackOtherId


    def how_many_stones_miss_and_admissible_cells(self, state, player):
        myId = player
        otherId = 1 - myId
        countAdmissibleCells = 0
        firstCapstoneFound = True
        for row in range(0, state.size):
            for col in range(0, state.size):
                if state.is_empty(row, col):  # if is empty
                    countAdmissibleCells += 1
                else:
                    piece_type, owner = state.board[row][col].top()
                    if owner == otherId:
                        if piece_type != tak.CAP_STONE:  #
                            if state.size < 5 and piece_type != tak.STANDING_STONE:
                                countAdmissibleCells += 1
                        else:
                            if firstCapstoneFound:
                                self.adversaryPlacedCapstones.clear()
                                firstCapstoneFound = False
                            self.adversaryPlacedCapstones.append((row, col))

        return countAdmissibleCells

    def myCheck_H_V_path(self, player, state):
        minDistanceFromGoalLR, minDistanceFromGoalWithStackLR = self.myCheck_horizontal_path(player, state)
        minDistanceFromGoalUD, minDistanceFromGoalWithStackUD = self.myCheck_vertical_path(player, state)
        return min(minDistanceFromGoalLR, minDistanceFromGoalUD), min(minDistanceFromGoalWithStackLR, minDistanceFromGoalWithStackUD)

    """
  Check whether there is a horizontal winnning path for a given player.
  """

    def myCheck_horizontal_path(self, player, state):
        # initialize left positions that belong to player
        L = []
        R = []
        for r in range(state.size):
            if state.is_controlled_by(r, 0, player):
                L.append((r, 0))
            if state.is_controlled_by(r, state.size - 1, player):
                R.append((r, state.size - 1))
        minDistanceFromGoalLeft, minDistanceFromGoalWithStackLeft = self.myBfs(L, "LEFT", player, state)
        minDistanceFromGoalRight, minDistanceFromGoalWithStackRight = self.myBfs(R, "RIGHT", player, state)
        return min(minDistanceFromGoalLeft, minDistanceFromGoalRight), \
               min(minDistanceFromGoalWithStackLeft, minDistanceFromGoalWithStackRight)

    """
  Check whether there is a vertical winning path for a given player.
  """

    def myCheck_vertical_path(self, player, state):
        # initialize the top positions that belong to player
        U = []
        D = []
        for c in range(state.size):
            if state.is_controlled_by(0, c, player):
                U.append((0, c))
            if state.is_controlled_by(state.size - 1, c, player):
                D.append((state.size - 1, c))
        # perform a BFS from the top to see if we can reach the bottom
        minDistanceFromGoalUp, minDistanceFromGoalWithStackUp = self.myBfs(U, "UP", player, state)
        minDistanceFromGoalDown, minDistanceFromGoalWithStackDown = self.myBfs(D, "DOWN", player, state)
        return min(minDistanceFromGoalUp, minDistanceFromGoalDown), \
               min(minDistanceFromGoalWithStackUp, minDistanceFromGoalWithStackDown)

    """
  Check whether there is a path controlled by the given player connecting the
  cells in S to the cells in T. Used to check winning paths.
  """

    def myBfs(self, S, direction, player, state):
        # initialize BFS
        minDistanceFromGoal = math.inf
        parent = [[None for _ in range(state.size)] for _ in range(state.size)]
        Q = Queue()
        for s in S:
            Q.add(s)
            parent[s[0]][s[1]] = -1
        # BFS loop
        cnt = 0
        while len(Q) > 0:
            cnt += 1
            r, c = Q.remove()
            for d in tak.DIR:
                rr = r + d[0]
                cc = c + d[1]
                if 0 <= rr < state.size and 0 <= cc < state.size and \
                        parent[rr][cc] is None and state.is_controlled_by(rr, cc, player):
                    Q.add((rr, cc))
                    minDistanceFromGoal = min(self.check_possible_path_from_stack(direction, r, c, state, player),
                                              minDistanceFromGoal)
                    parent[rr][cc] = (r, c)
        # check whether the other side was reached
        r, c, step, reverse = self.getDirectionIndexes(direction, state)
        for i in range(0, state.size):
            maxListOfPath = []  # list of paths
            maxList = []  # list of coordinates of the subpaths
            iterationList = range(0, state.size)
            listOfDistancesFromGoal = []
            if reversed:
                reversed(iterationList)
            goalPosition = iterationList[0]
            if r == -1:

                for row in iterationList:
                    if parent[row][c] is not None:
                        # build the path
                        cur = (row, c)
                        # maxListOfPath.append(self.buildPath(parent, cur))
                        maxList.append(cur)
                        listOfDistancesFromGoal.append(abs(goalPosition - row))
            else:  # column
                for col in iterationList:
                    if parent[r][col] is not None:
                        # build the path
                        cur = (r, col)
                        # maxListOfPath.append(self.buildPath(parent, cur))
                        maxList.append(cur)
                        listOfDistancesFromGoal.append(abs(goalPosition - col))

            if len(maxList) == 1:
                return listOfDistancesFromGoal[0], minDistanceFromGoal
            elif len(maxList) > 1:
                return listOfDistancesFromGoal[self.findFarthestFromCapstone(maxList)], minDistanceFromGoal
            r += step[0]
            c += step[1]
        return state.size, minDistanceFromGoal

    def findFarthestFromCapstone(self, maxList):
        farthestElement = None
        maxDistance = - math.inf
        for i in range(0, len(maxList)):
            distance = math.inf
            for capstone in self.adversaryPlacedCapstones:
                distance = min(distance,
                               self.computeEuclidianDistance(capstone[0], capstone[1], maxList[i][0], maxList[i][1]))
            if distance > maxDistance:
                maxDistance = distance
                farthestElement = i
        return farthestElement

    def computeEuclidianDistance(self, x, y, x1, y1):
        return abs(((x - x1) ** 2) + ((y - y1) ** 2))

    def buildPath(self, parent, cur):
        path = []
        while cur != -1:
            path.append(cur)
            cur = parent[cur[0]][cur[1]]
        return path

    def getDirectionIndexes(self, direction, state):
        if direction == "UP":
            startRow = state.size - 1
            startColumn = -1
            step = (-1, 0)
            reverse = False
        elif direction == "DOWN":
            startRow = 0
            startColumn = -1
            step = (1, 0)
            reverse = True
        elif direction == "LEFT":
            startRow = -1
            startColumn = state.size - 1
            step = (0, -1)
            reverse = False
        else:  # RIGHT
            startRow = -1
            startColumn = 0
            step = (0, 1)
            reverse = True
        return startRow, startColumn, step, reverse

    def check_possible_path_from_stack(self, direction, row, col, state, player):
        r = row
        c = col
        myId = player
        otherId = 1 - myId
        countStonesMyId = 0
        flagCapstoneOnTop = False
        onTop, _ = (state.board[r][c].top())
        if onTop == tak.CAP_STONE:
            flagCapstoneOnTop = True

        stack = state.board[r][c]
        for element in stack.s:
            if element[1] == myId:
                countStonesMyId += 1
        _, _, step, _ = self.getDirectionIndexes(direction, state)
        r += step[0]
        c += step[1]
        lenPossiblePath = 1
        countStonesMyId -= 1
        while (0 <= r < state.size) and (0 <= c < state.size) and (countStonesMyId > 0):
            if len(state.board[r][c]) != 0:
                piece_type, owner = state.board[r][c].top()
                if piece_type == tak.STANDING_STONE:
                    if flagCapstoneOnTop is True:
                        lenPossiblePath += 1
                        countStonesMyId -= 1
                    break

                elif piece_type == tak.CAP_STONE:
                    break
            r += step[0]
            c += step[1]
            lenPossiblePath += 1
            countStonesMyId -= 1

        if direction == "UP":
            return row - lenPossiblePath
        elif direction == "DOWN":
            return state.size - row - lenPossiblePath
        elif direction == "LEFT":
            return col - lenPossiblePath
        else:  # RIGHT
            return state.size - col - lenPossiblePath
