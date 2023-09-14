from game import BoardState, Rules, find_ball_coords
import numpy as np


def main():
    bs = BoardState()
    assert bs.decode_single_pos(55) == (6,7)
    assert bs.decode_single_pos(0) == (0,0)

    assert bs.encode_single_pos((6,7)) == 55
    assert bs.encode_single_pos((0,0)) == 0
    assert bs.encode_single_pos((1,3)) == 22


    bs.state = np.array([1,2,2,4,5,3,50,51,56,53,54,52])
    assert not bs.is_valid()
    bs.state = np.array([1,2,3,4,5,3,50,51,52,53,54,52])
    assert bs.is_valid()

    bs.state = np.array([1,2,3,4,5,3,50,51,52,53,54,52])
    assert not bs.is_termination_state()
    bs.state = np.array([1,2,3,4,5,52,50,51,52,53,54,52])
    assert bs.is_termination_state()
    bs.state = np.array([1,2,3,4,5,3,50,51,52,53,54,3])
    assert bs.is_termination_state()

    bs.state = np.array([1,2,3,4,5,3,50,51,52,53,54,52])
    rules = Rules()

    print("Testing single piece actions")
    assert 0 not in rules.single_piece_actions(bs, 0)

    for n in rules.single_piece_actions(bs, 0):
        col,row = bs.decode_single_pos(n)
        assert 0 <= col <= bs.N_COLS - 1 and 0 <= row <= bs.N_ROWS - 1

    bs.state = np.array([1,2,3,4,5,3,50,51,52,53,54,52])

    assert len(rules.single_piece_actions(bs, 3)) == 0
    assert len(rules.single_piece_actions(bs, 2)) != 0
    assert len(rules.single_piece_actions(bs, 52)) == 0

    print("Passed!")
    print()
    print("Testing ball state helper")

    bs.state = np.array([1,2,3,4,5,3,50,51,52,53,54,52])

    assert find_ball_coords(bs, 0) == bs.decode_single_pos(3)
    assert find_ball_coords(bs, 1) == bs.decode_single_pos(52)
    print("Passed")

    bs.state = np.array([1,2,3,4,5,3,50,51,52,53,54,52])

    print("Testing ball move")
    bs.state = np.array([1,2,3,4,24,3,50,51,52,53,54,52])
    bs.decode_state = [bs.decode_single_pos(d) for d in bs.state]
    ball_actions = Rules.single_ball_actions(bs, 0)

    assert 24 in ball_actions
    assert 4 in ball_actions
    assert 1 in ball_actions

    # Test 2
    bs.state = np.array([1,2,3,4,24,3,50,51,17,53,54,52])
    bs.decode_state = [bs.decode_single_pos(d) for d in bs.state]
    ball_actions = Rules.single_ball_actions(bs, 0)
    print(ball_actions)
    assert 24 not in ball_actions # It's blocked!






if __name__ == "__main__":
    main()
