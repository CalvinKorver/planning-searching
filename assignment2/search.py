import heapq
from collections import deque
import numpy as np
import queue
from game import BoardState, GameSimulator, Rules

class Problem:

    def __init__(self, initial_state, goal_state_set: set):
        self.initial_state = initial_state
        self.goal_state_set = goal_state_set

    def get_actions(self, state):
        """
        Returns a set of valid actions that can be taken from this state
        """
        pass

    def execute(self, state, action):
        """
        Transitions from the state to the next state that results from taking the action
        """
        pass

    def is_goal(self, state):
        """
        Checks if the state is a goal state in the set of goal states
        """
        return state in self.goal_state_set

class GameStateProblem(Problem):

    def __init__(self, initial_board_state, goal_board_state, player_idx):
        """
        player_idx is 0 or 1, depending on which player will be first to move from this initial state.

        The form of initial state is:
        ((game board state tuple), player_idx ) <--- indicates state of board and who's turn it is to move
        """
        super().__init__(tuple((tuple(initial_board_state.state), player_idx)), set([tuple((tuple(goal_board_state.state), 0)), tuple((tuple(goal_board_state.state), 1))]))
        self.sim = GameSimulator(None)
        self.search_alg_fnc = None
        self.set_search_alg()

    def set_search_alg(self, alg=""):
        """
        If you decide to implement several search algorithms, and you wish to switch between them,
        pass a string as a parameter to alg, and then set:
            self.search_alg_fnc = self.your_method
        to indicate which algorithm you'd like to run.

        TODO: You need to set self.search_alg_fnc here
        """
        self.search_alg_fnc = self.adversarial_search_method

    def get_actions(self, state: tuple):
        """
        From the given state, provide the set possible actions that can be taken from the state

        Inputs: 
            state: (encoded_state, player_idx), where encoded_state is a tuple of 12 integers,
                and player_idx is the player that is moving this turn

        Outputs:
            returns a set of actions
        """
        s, p = state
        np_state = np.array(s)
        self.sim.game_state.state = np_state
        self.sim.game_state.decode_state = self.sim.game_state.make_state()

        return self.sim.generate_valid_actions(p)

    def execute(self, state: tuple, action: tuple):
        """
        From the given state, executes the given action

        The action is given with respect to the current player

        Inputs: 
            state: is a tuple (encoded_state, player_idx), where encoded_state is a tuple of 12 integers,
                and player_idx is the player that is moving this turn
            action: (relative_idx, position), where relative_idx is an index into the encoded_state
                with respect to the player_idx, and position is the encoded position where the indexed piece should move to.
        Outputs:
            the next state tuple that results from taking action in state
        """
        s, p = state
        k, v = action
        offset_idx = p * 6
        return tuple((tuple(s[i] if i != offset_idx + k else v for i in range(len(s))), (p + 1) % 2))

    #       Implement your search algorithm(s) here as methods of the GameStateProblem.
    #       You are free to specify parameters that your method may require.
    #       However, you must ensure that your method returns a list of (state, action) pairs, where
    #       the first state and action in the list correspond to the initial state and action taken from
    #       the initial state, and the last (s,a) pair has s as a goal state, and a=None, and the intermediate
    #       (s,a) pairs correspond to the sequence of states and actions taken from the initial to goal state.
    # NOTE: The format of state is a tuple: (encoded_state, player_idx), where encoded_state is a tuple of 12 integers
    #       (mirroring the contents of BoardState.state), and player_idx is 0 or 1, indicating the player that is
    #       moving in this state.
    #       The format of action is a tuple: (relative_idx, position), where relative_idx the relative index into encoded_state
    #       with respect to player_idx, and position is the encoded position where the piece should move to with this action.
    # NOTE: self.get_actions will obtain the current actions available in current game state.
    # NOTE: self.execute acts like the transition function.
    # NOTE: Remember to set self.search_alg_fnc in set_search_alg above.
    #

    # From assignment 3:
    # You can add multiple adversarial search algorithms to the GameStateProblem class, and then
    # create various Player classes which use those specific algorithms.

    def adversarial_search_method(self, state_tup, board_state, player_idx, val_c):

        heap = []
        possible_actions = self.get_actions(state_tup)
        for action in possible_actions:
            new_state = self.execute(state_tup, action)
            h = self.calc_h(new_state, state_tup)
            # h = 0
            # Short circuit if we have an action that immediately wins the game
            if board_state.is_termination_state_for_player(new_state[0], player_idx):
                print()
                print()
                print("Short circuited on the 1st action of the game.")
                print('Action:', action)
                print()
                return action, None
            heap.append((h, ActionNode(action, state_tup)))

        heapq.heapify(heap)
        # heap = heapq.nsmallest(5,heap)

        # Let player 2 "go" now
        player_idx = 1 if state_tup[1] == 0 else 0
        player_2_heap = []
        for _, node in heap:
            state = self.execute(node.state, node.action)
            player_2_poss_actions = self.get_actions(state)
            for action in player_2_poss_actions:
                state_after_player_2_action = self.execute(state, action)
                h = self.calc_h(state_after_player_2_action, state)

                # if board_state.is_termination_state_for_player(state_after_player_2_action[0], player_idx):
                #     print()
                #     print()
                #     print("Found terminating move for other player")
                #     # print('Action:', action)
                #     print()

                player_2_node = ActionNode(action, state)
                player_2_node.setParent(node)
                player_2_heap.append((h, player_2_node))

        heapq.heapify(player_2_heap)

        player_1_heap = []
        for _, node in player_2_heap:
            state = self.execute(node.state, node.action)
            player_1_actions = self.get_actions(state)
            for action in player_1_actions:
                new_state = self.execute(state,action)
                h = self.calc_h(new_state,state)
                player_1_node = ActionNode(action,new_state)
                player_1_node.setParent(node)
                player_1_heap.append((h, player_1_node))

        heapq.heapify(player_1_heap)
        smallest = [x[1] for x in heapq.nsmallest(5,player_1_heap)]
        smallest_node = smallest[0]

        while smallest_node.getParent():
            smallest_node = smallest_node.getParent()

        return smallest_node.action, None

    def calc_h(self, new_state, last_state):
        player_idx = last_state[1]
        last_ball_loc = last_state[0][(player_idx * 5) + 5]
        next_ball_loc = new_state[0][(player_idx * 5) + 5]
        last_ball_loc //= 8
        next_ball_loc //= 8
        h = 7
        if player_idx == 0:
            # We want to get closer to the "top" of the board, in other words current - last == 0
            h = 7 - next_ball_loc
        else:
            h = next_ball_loc
        return h


class ActionNode():
    def __init__(self, action, state):
        self.state = state
        self.action = action # action is a tuple (x,y)
        self.parent = None
    def getParent(self):
        return self.parent

    def setParent(self, parent):
        self.parent = parent

    def __eq__(self, other):
        return True

    def __lt__(self, other):
        return True

    def __gt__(self, other):
        return True
