from game import BoardState


def main():
    bs = BoardState()
    assert bs.decode_single_pos(55) == (6,7)
    assert bs.decode_single_pos(0) == (0,0)

    assert bs.encode_single_pos((6,7)) == 55
    assert bs.encode_single_pos((0,0)) == 0
    assert bs.encode_single_pos((1,3)) == 22


if __name__ == "__main__":
    main()
