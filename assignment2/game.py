import numpy as np


class Player:
    def __init__(self, policy_fnc):
        self.policy_fnc = policy_fnc

    def policy(self, decode_state):
        pass


class AdversarialSearchPlayer(Player):
    def __init__(self, gsp, player_idx):
        # You can customize the signature of the constructor above to suit your needs.
        # In this example, in the above parameters, gsp is a GameStateProblem, and
        # gsp.adversarial_search_method is a method of that class.

        super().__init__(gsp.adversarial_search_method)
        self.gsp = gsp
        self.b = BoardState()
        self.player_idx = player_idx

    def policy(self, decode_state):
        # Here, the policy of the player is to consider the current decoded game state
        # and then correctly encode it and provide any additional required parameters to the
        # assigned policy_fnc (which in this case is gsp.adversarial_search_method), and then
        # return the result of self.policy_fnc

        encoded_state_tup = tuple(self.b.encode_single_pos(s) for s in decode_state)
        state_tup = tuple((encoded_state_tup, self.player_idx))
        val_a, val_b, val_c = (1, 2, 3)
        return self.policy_fnc(state_tup, None, self.player_idx, val_c)


class BoardState:
    """
    Represents a state in the game

    """

    def __init__(self):
        """
        Initializes a fresh game state
        """
        self.N_ROWS = 8
        self.N_COLS = 7

        self.MAX = 55
        self.MIN = 0

        self.white_ball_index = 5
        self.black_ball_index = 11

        self.state = np.array([1, 2, 3, 4, 5, 3, 50, 51, 52, 53, 54, 52])
        self.decode_state = [self.decode_single_pos(d) for d in self.state]

    def update(self, idx, val):
        """
        Updates both the encoded and decoded states
        """
        self.state[idx] = val
        self.decode_state[idx] = self.decode_single_pos(self.state[idx])

    def make_state(self):
        """
        Creates a new decoded state list from the existing state array
        """
        return [self.decode_single_pos(d) for d in self.state]

    def encode_single_pos(self, cr: tuple):
        """
        Encodes a single coordinate (col, row) -> Z

        Input: a tuple (col, row)
        Output: an integer in the interval [0, 55] inclusive

        """
        return cr[1] * self.N_COLS + cr[0]

    def decode_single_pos(self, n: int):
        """
        Decodes a single integer into a coordinate on the board: Z -> (col, row)

        Input: an integer in the interval [0, 55] inclusive
        Output: a tuple (col, row)

        """
        return n % self.N_COLS, n // self.N_COLS

    def is_termination_state(self):
        """
        Checks if the current state is a termination state. Termination occurs when
        one of the player's move their ball to the opposite side of the board.

        You can assume that `self.state` contains the current state of the board, so
        check whether self.state represents a termainal board state, and return True or False.

        """
        if not self.is_valid():
            return False
        else:
            return 49 <= self.state[self.white_ball_index] <= self.MAX or self.MIN <= self.state[
                self.black_ball_index] <= 6

    def is_termination_state_for_player(self, state, player_idx):
        if not self.is_valid():
            return False
        else:
            if player_idx == 0:
                return 49 <= state[self.white_ball_index] <= self.MAX
            else:
                return self.MIN <= state[self.black_ball_index] <= 6



    def is_valid(self):
        """
        Checks if a board configuration is valid. This function checks whether the current
        value self.state represents a valid board configuration or not. This encodes and checks
        the various constrainsts that must always be satisfied in any valid board state during a game.

        If we give you a self.state array of 12 arbitrary integers, this function should indicate whether
        it represents a valid board configuration.

        Output: return True (if valid) or False (if not valid)

        """
        all_states = set()
        for index, state in enumerate(self.state):
            # Checks for overlap and within bounds
            if not (self.MIN <= state <= self.MAX):
                return False

            if index not in [self.white_ball_index, self.black_ball_index]:
                if state in all_states:
                    return False
                else:
                    all_states.add(state)

        # Check that the player is holding the ball
        if self.state[self.white_ball_index] not in self.state[:self.white_ball_index] or self.state[
            self.black_ball_index] not in self.state[self.white_ball_index + 1:self.black_ball_index]:
            return False

        return True


class Rules:

    @staticmethod
    def single_piece_actions(board_state, piece_idx):
        """
        Returns the set of possible actions for the given piece, assumed to be a valid piece located
        at piece_idx in the board_state.state.

        Inputs:
            - board_state, assumed to be a BoardState
            - piece_idx, assumed to be an index into board_state, identfying which piece we wish to
              enumerate the actions for.

        Output: an iterable (set or list or tuple) of integers which indicate the encoded positions
            that piece_idx can move to during this turn.
        """

        # Rule 1: A block can only be moved if it is not holding a ball
        if piece_idx == board_state.white_ball_index or piece_idx == board_state.black_ball_index:
            raise ValueError("A block can only be moved if it is not holding a ball!")

        col_0, row_0 = board_state.decode_state[piece_idx]  # Gets the col,row of the piece we care about

        # Occupied spaces are all the other pieces (except for the piece we are looking at)
        occupied_spaces = [(col, row) for i, (col, row) in enumerate(board_state.decode_state) if i != piece_idx]

        # Moves are similar to a knight, so we create all 8 here
        possible_move_values = [(1, 2), (-1, 2), (-2, 1), (2, 1), (2, -1), (-2, -1), (-1, -2), (1, -2)]

        legal_moves = set()

        # Rules 2: A block can only move to unoccupied spaces on the board
        for col_move, row_move in possible_move_values:
            col = col_0 + col_move
            row = row_0 + row_move
            if 0 <= col < board_state.N_COLS and 0 <= row < board_state.N_ROWS \
                    and (col, row) not in occupied_spaces:
                legal_moves.add((col, row))

        # We need to encode the legal moves back to integers and return
        return [board_state.encode_single_pos((col, row)) for col, row in legal_moves]

    @staticmethod
    def find_ball_coords(board_state, player_idx):
        if player_idx == 0:
            return board_state.decode_state[board_state.white_ball_index]
        else:
            return board_state.decode_state[board_state.black_ball_index]

    @staticmethod
    def find_team_pieces(board_state, player_idx):
        if player_idx == 0:
            l = set(board_state.decode_state[:board_state.white_ball_index])
            if board_state.decode_state[board_state.white_ball_index] in l:
                l.remove(board_state.decode_state[board_state.white_ball_index])
        else:
            l = set(board_state.decode_state[board_state.white_ball_index + 1:board_state.black_ball_index])
            if board_state.decode_state[board_state.black_ball_index] in l:
                l.remove(board_state.decode_state[board_state.black_ball_index])

        return list(l)

    @staticmethod
    def find_opposing_team_pieces(board_state, player_idx):
        if player_idx == 1:
            l = set(board_state.decode_state[:board_state.white_ball_index])
            # l.remove(board_state.decode_state[board_state.white_ball_index])
        else:
            l = set(board_state.decode_state[board_state.white_ball_index + 1:board_state.black_ball_index])
            # l.remove(board_state.decode_state[board_state.black_ball_index])

        return list(l)

    @staticmethod
    def diagonal_move_available(ball_col, ball_row, catch_col, catch_row, opposing_pieces):

        if abs(catch_col - ball_col) == abs(catch_row - ball_row):  # If the difference its equal, its diag

            distance = abs(catch_col - ball_col)
            # Iterate ovefr all possible diagonals to check if opposing pieces exist there
            for i in range(1, distance):
                if catch_col < ball_col and catch_row < ball_row:  # Lower left
                    target = ball_col - i, ball_row - i
                elif catch_col > ball_col and catch_row > ball_row:  # Upper right
                    target = ball_col + i, ball_row + i
                elif catch_col < ball_col and catch_row > ball_row:  # Upper left
                    target = ball_col - i, ball_row + i
                else:
                    target = ball_col + i, ball_row - i

                if target in opposing_pieces:
                    return False
            return True
        else:
            return False

    @staticmethod
    def single_ball_actions(board_state, player_idx):
        """
        Returns the set of possible actions for moving the specified ball, assumed to be the
        valid ball for player_idx  in the board_state

        Inputs:
            - board_state, assumed to be a BoardState
            - player_idx, either 0 or 1, to indicate which player's ball we are enumerating over
        
        Output: an iterable (set or list or tuple) of integers which indicate the encoded positions
            that player_idx's ball can move to during this turn.

        FROM SPEC:
        A player’s ball can only be passed from the block piece holding it to a block piece of the same color along
        vertical, horizontal, or diagonal channels (same as a queen in chess). If an opposing player’s block piece
        would intercept the ball along the desired passing path between pieces b1 and b2, then the pass is not
        valid, and the ball cannot be moved from b1 to b2 directly. However, if there exists an unobstructed passing
        path from b1 to b3, and from b3 to b2, then the player could pass from b1 to b3 to b2 as a valid move.
        Therefore, in a single turn, a player may pass their ball between pieces of the same color an unlimited
        number of times as long as the passing channels for the ball are unobstructed on each pass.

        ball_col + n, ball_row + n == catch_col, catch_row
        """

        ball_col, ball_row = Rules.find_ball_coords(board_state, player_idx)
        team_pieces = Rules.find_team_pieces(board_state, player_idx)
        opposing_pieces = Rules.find_opposing_team_pieces(board_state, player_idx)

        finding_new_moves = True

        # First, lets find all the possible moves from the current ball location
        legal_moves = Rules.enumerate_options(ball_col, ball_row, opposing_pieces, team_pieces)

        # Next, while we continue to find new places for the ball, continue iterating until we
        # end up with the same set as last time
        while True:
            new_moves = set()
            for col, row in legal_moves:
                new_moves = new_moves.union(Rules.enumerate_options(col, row, opposing_pieces, team_pieces))

            # Combine the new moves with the old
            new_legal_moves = new_moves.union(legal_moves)

            if len(new_legal_moves) == len(legal_moves):
                break
            else:
                legal_moves = new_legal_moves

        return set(board_state.encode_single_pos((col, row)) for col, row in legal_moves)

    @staticmethod
    def enumerate_options(ball_col, ball_row, opposing_pieces, team_pieces):
        legal_moves = set()
        for catch_col, catch_row in team_pieces:
            if catch_col == ball_col and catch_row == ball_row:
                continue
            # First, lets see if it is horizontal or vertical and not blocked
            if (catch_col == ball_col and ball_col not in [col for col, row in opposing_pieces if
                                                           ball_row < row < catch_row or ball_row > row > catch_row]) or \
                    (catch_row == ball_row and ball_row not in [row for col, row in opposing_pieces if
                                                                ball_col < col < catch_col or ball_col > col > catch_col]):
                legal_moves.add((catch_col, catch_row))
            elif Rules.diagonal_move_available(ball_col, ball_row, catch_col, catch_row, opposing_pieces):
                legal_moves.add((catch_col, catch_row))
            else:
                pass
        return legal_moves


class GameSimulator:
    """
    Responsible for handling the game simulation
    """

    def __init__(self, players):
        self.game_state = BoardState()
        self.current_round = -1  ## The game starts on round 0; white's move on EVEN rounds; black's move on ODD rounds
        self.players = players

    def run(self):
        """
        Runs a game simulation
        """
        while not self.game_state.is_termination_state():

            ## Determine the round number, and the player who needs to move
            self.current_round += 1
            player_idx = self.current_round % 2

            ## For the player who needs to move, provide them with the current game state
            ## and then ask them to choose an action according to their policy
            action, value = self.players[player_idx].policy(self.game_state.make_state())
            print(
                f"Round: {self.current_round} Player: {player_idx} State: {tuple(self.game_state.state)} Action: {action} Value: {value}")

            if not self.validate_action(action, player_idx):
                ## If an invalid action is provided, then the other player will be declared the winner
                if player_idx == 0:
                    return self.current_round, "BLACK", "White provided an invalid action"
                else:
                    return self.current_round, "WHITE", "Black probided an invalid action"

            ## Updates the game state
            self.update(action, player_idx)

        ## Player who moved last is the winner
        if player_idx == 0:
            return self.current_round, "WHITE", "No issues"
        else:
            return self.current_round, "BLACK", "No issues"

    def generate_valid_actions(self, player_idx: int):
        """
        Given a valid state, and a player's turn, generate the set of possible actions that player can take

        player_idx is either 0 or 1

        Input:
            - player_idx, which indicates the player that is moving this turn. This will help index into the
              current BoardState which is self.game_state
        Outputs:
            - a set of tuples (relative_idx, encoded position), each of which encodes an action. The set should include
              all possible actions that the player can take during this turn. relative_idx must be an
              integer on the interval [0, 5] inclusive. Given relative_idx and player_idx, the index for any
              piece in the boardstate can be obtained, so relative_idx is the index relative to current player's
              pieces. Pieces with relative index 0,1,2,3,4 are block pieces that like knights in chess, and
              relative index 5 is the player's ball piece.
        """
        # Gets the correct indices depending on the player idx
        indices = [i for i in range(5)] if player_idx == 0 else [i for i in range(6, 11)]

        pieces_actions = [Rules.single_piece_actions(self.game_state, i) for i in indices]

        all_actions = set()
        for i, actions in enumerate(pieces_actions):
            for action in actions:
                all_actions.add((i, action))

        for ball_action in Rules.single_ball_actions(self.game_state, player_idx):
            all_actions.add((5, ball_action))

        return all_actions

    def validate_action(self, action: tuple, player_idx: int):
        """
        Checks whether or not the specified action can be taken from this state by the specified player

        Inputs:
            - action is a tuple (relative_idx, encoded position)
            - player_idx is an integer 0 or 1 representing the player that is moving this turn
            - self.game_state represents the current BoardState

        Output:
            - if the action is valid, return True
            - if the action is not valid, raise ValueError

        """
        valid_actions = self.generate_valid_actions(player_idx)
        if action in valid_actions:
            return True
        else:
            raise ValueError(
                "For each case that an action is not valid, specify the reason that the action is not valid in this ValueError.")

    def update(self, action: tuple, player_idx: int):
        """
        Uses a validated action and updates the game board state
        """
        offset_idx = player_idx * 6  ## Either 0 or 6
        idx, pos = action
        self.game_state.update(offset_idx + idx, pos)
