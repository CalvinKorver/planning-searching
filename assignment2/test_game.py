import numpy as np
import pytest

from game import BoardState, GameSimulator, AdversarialSearchPlayer
from search import GameStateProblem, calc_h


@pytest.mark.parametrize("p1_class,p2_class,encoded_state_tuple,exp_winner,exp_stat", [
    (AdversarialSearchPlayer, AdversarialSearchPlayer,
     (49, 37, 46, 41, 55, 41, 50, 51, 52, 53, 54, 52),
     "WHITE", "No issues")
])
def test_adversarial_search(p1_class, p2_class, encoded_state_tuple, exp_winner, exp_stat):
    b1 = BoardState()
    b1.state = np.array(encoded_state_tuple)
    b1.decode_state = b1.make_state()
    players = [
        p1_class(GameStateProblem(b1, b1, 0), 0),
        p2_class(GameStateProblem(b1, b1, 0), 1)]
    sim = GameSimulator(players)
    sim.game_state = b1
    rounds, winner, status = sim.run()
    assert winner == exp_winner and status == exp_stat


# (44, 37, 46, 41, 40, 41, 1, 2, 52, 4, 5, 52),  White wins within 3 steps
@pytest.mark.parametrize("p1_class,p2_class,encoded_state_tuple,exp_winner,exp_stat", [
    # (AdversarialSearchPlayer, AdversarialSearchPlayer,
    #  (44, 37, 46, 41, 40, 41, 1, 2, 52, 4, 5, 52),
    #  "WHITE", "No issues"),
    (AdversarialSearchPlayer, AdversarialSearchPlayer,
     (14, 21, 22, 28, 29, 22, 11, 20, 34, 48, 55, 55),
     "BLACK", "No issues"),
])
def test_adversarial_search2(p1_class, p2_class, encoded_state_tuple, exp_winner, exp_stat):
    b1 = BoardState()
    b1.state = np.array(encoded_state_tuple)
    b1.decode_state = b1.make_state()
    players = [
        p1_class(GameStateProblem(b1, b1, 0), 0),
        p2_class(GameStateProblem(b1, b1, 0), 1)]
    sim = GameSimulator(players)
    sim.game_state = b1
    rounds, winner, status = sim.run()
    assert winner == exp_winner and status == exp_stat


@pytest.mark.parametrize("p1_class,p2_class,encoded_state_tuple,exp_winner,h", [
    (AdversarialSearchPlayer, AdversarialSearchPlayer,
     ((1, 2, 3, 4, 5, 3, 50,51,52,53,54,52), 0),
     "WHITE", 0),
    (AdversarialSearchPlayer, AdversarialSearchPlayer,
     ((49, 37, 46, 41, 40, 37, 1, 2, 3, 4, 5, 3), 0),
     "WHITE", -8.4),

    (AdversarialSearchPlayer, AdversarialSearchPlayer,
     ((49, 37, 46, 41, 40, 49, 1, 2, 52, 4, 5, 52), 0),
     "WHITE", 7.0),

    # (AdversarialSearchPlayer, AdversarialSearchPlayer,
    #  ((49, 37, 46, 41, 40, 37, 1, 2, 3, 4, 5, 3), 0),
    #  "WHITE", -1.4),

    # (AdversarialSearchPlayer, AdversarialSearchPlayer,
    #  ((49, 37, 46, 41, 40, 49, 1, 2, 52, 4, 5, 1), 1),
    #  "WHITE", 0),
    #     (AdversarialSearchPlayer, AdversarialSearchPlayer,
    #  ((49, 37, 46, 41, 40, 40, 1, 2, 52, 4, 5, 1), 1),
    #  "WHITE", -7),
])
def test_h(p1_class, p2_class, encoded_state_tuple, exp_winner, h):
    b1 = BoardState()
    b1.state = np.array(encoded_state_tuple[0])
    b1.decode_state = b1.make_state()
    assert (calc_h(b1, 0) == h)


