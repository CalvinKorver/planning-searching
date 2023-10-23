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
        super().__init__(tuple((tuple(initial_board_state.state), player_idx)),
                         set([tuple((tuple(goal_board_state.state), 0)), tuple((tuple(goal_board_state.state), 1))]))
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


    def adversarial_search_method(self, state_tup, board_state, player_idx, plies):
        plies = 3
        possible_actions = self.get_actions(state_tup)
        maximum = float('-inf')
        maximumAction = None
        prev_actions_h = []
        for action in possible_actions:
            piece_to_move = state_tup[0][action[0] + (player_idx * 6)]
            state_tuple = self.execute(state_tup, action)
            board_state, next_player_idx = create_next_board(state_tuple)
            val = self.determine_max(board_state, next_player_idx, 1, plies)
            if val > maximum:
                maximum = val
                maximumAction = action

            prev_actions_h.append((val, piece_to_move,action[1]))
        # reversed = True if player_idx == 0 else False
        reversed = True
        prev_actions = sorted(prev_actions_h, key=lambda x: x[0], reverse=reversed)
        print()
        print(prev_actions[:7])
        print()
        return maximumAction, maximum


    def determine_max(self, board_state, player_idx, current_plie, total_plies):
        if self.minimax_term_conditions(board_state, current_plie, total_plies):
            return calc_h(board_state, player_idx, True)

        current_plie += 1
        actions = self.get_actions((board_state.state, player_idx))
        maximum = float('-inf')
        for action in actions:
            new_state = self.execute((board_state.state, player_idx), action)
            next_board_state, next_player_idx = create_next_board(new_state)
            val = self.determine_min(next_board_state, next_player_idx, current_plie, total_plies)
            if val > maximum:
                maximum = val
        return maximum

    def determine_min(self, board_state, player_idx, current_plie, total_plies):
        if self.minimax_term_conditions(board_state, current_plie, total_plies):
            return calc_h(board_state, player_idx, False)

        current_plie += 1
        actions = self.get_actions((board_state.state, player_idx))
        minimum = float('inf')
        for action in actions:
            new_state = self.execute((board_state.state, player_idx), action)
            next_board_state, next_player_idx = create_next_board(new_state)
            val = self.determine_max(next_board_state, next_player_idx, current_plie, total_plies)
            if val < minimum:
                minimum = val
        return minimum

    def minimax_term_conditions(self, board_state, current_plie, total_plies):
        return current_plie == total_plies or board_state.is_termination_state()


    # This should return a value in the range of [-7 to 7] depending on
    # how close the player is to winning. If the move is perfect for white, it should
    # return 1. If the move is the worst for white it should return -1
    # For example, if player==0 and was 0 rows from winning and player1 was 1 rows,
    # we could do (next_ball_loc / 7) - ((7 - enemy_ball_loc) / 7) / 2
def calc_h(board_state, player_idx, is_max):
    new_state = board_state.state

    white_ball_row = new_state[5] // 7
    black_ball_row = new_state[11] // 7

    white_score = 0
    black_score = 0

    # Calculate heuristic for the white and black players, how close the pieces are getting to the other side
    white_score = np.mean([val // 7 for val in new_state[:5]])
    black_score = 7 - np.mean([(val // 7) for val in new_state[6:11]])

    for val in new_state[:5]:
        if val // 7 == 7:
            white_score += 7

    for val in new_state[6:11]:
        if val // 7 == 0:
            black_score += 7

    if white_ball_row == 7:
        white_score += 20

    if black_ball_row == 0:
        black_score += 20

    score = round(white_score, 3) if player_idx == 1 else round(black_score, 3)

    return score if is_max else -score # For calls from minimum, we'd like to return the negative since we are
    # trying to minimize the value
    # return round(white_score - black_score, 3)

    # white_win = white_ball_row == 7
    # black_win = black_ball_row == 0
    #
    # if white_win and black_win:
    #     return 0
    # elif white_win:
    #     return 7
    # elif black_win:
    #     return -7
    # else:
    #     return round(white_ball_row - (7 - black_ball_row))

def create_next_board(state_and_plx):
    state, plx = state_and_plx
    b = BoardState()
    b.state = np.array(state)
    b.decode_state = b.make_state()
    # next_plx = 0 if plx == 1 else 0
    next_plx = plx
    return b, next_plx
