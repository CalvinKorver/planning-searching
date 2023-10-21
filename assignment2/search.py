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
        self.search_alg_fnc = self.bfs

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
        p1_q = deque()
        p1_q.append(self.initial_state)
        seen = set()
        seen.add(self.initial_state)
        parent = {self.initial_state: None}
        heap = []

        while True:
            state = p1_q.popleft()
            possible_actions = self.get_actions(state)
            for action in possible_actions:
                new_state = self.execute(state, action)
                # We should determine heuristic here...
                last_ball_loc = state[0][(player_idx * 5) + 5]
                next_ball_loc = new_state[0][(player_idx * 5) + 5]

                last_ball_loc //= 8
                next_ball_loc //= 8

                h = 7

                if player_idx == 0:
                    # We want to get closer to the "top" of the board, in other words current - last == 0
                    h = 7 - next_ball_loc
                else:
                    h = next_ball_loc

                heap.append((h, action))
            break

        heapq.heapify(heap)
        smallest = [x[1] for x in heapq.nsmallest(5,heap)]
        return smallest[0], None

    def bfs(self):

        # First, we perform BFS search and record the parents of each node
        parent, state = self.perform_bfs_search()

        # Next, we make sure we have the correct goal state from th e passed in parameter
        goal_state = self.find_goal_state(state)

        # Recursively back using the and the state and then reverse it (since we start from the back)
        result = []
        curr = goal_state
        while curr:
            result.append(curr)
            curr = parent[curr]
        pathway = result[::-1]

        # Reconstruct the actions using the states
        result = self.backtrack(pathway)

        # Append the final goal state to the result
        result.append((goal_state, None))
        return result

    def find_goal_state(self, state):
        for _s in self.goal_state_set:
            if _s == state:
                return _s

        raise ValueError("Error, goal state not matching")

    def perform_bfs_search(self):
        p1_q = deque()
        p1_q.append(self.initial_state)
        seen = set()
        seen.add(self.initial_state)
        parent = {self.initial_state: None}

        while True:
            state = p1_q.popleft()
            if self.is_goal(state):
                break

            possible_actions = self.get_actions(state)
            for action in possible_actions:
                new_state = self.execute(state, action)
                if new_state not in seen:
                    p1_q.append(new_state)
                    seen.add(new_state)
                    parent[new_state] = state
        return parent, state

    def backtrack(self, nodes):
        result = []

        for i in range(1, len(nodes)):
            current_state, current_player = nodes[i]
            previous_state, previous_player = nodes[i - 1]

            for index, _ in enumerate(current_state):
                if current_state[index] != previous_state[index]:
                    action = (index, current_state[index])
                    result.append(((previous_state, previous_player), action))

        return result
