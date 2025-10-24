from visky.utils import split_sequences_on_gap_in_one


def test_split_single_sequence():
    result = split_sequences_on_gap_in_one([1, 2, 4, 5], 1)
    assert result == [[[1, 2]], [[4, 5]]]


def test_split_two_sequences():
    result = split_sequences_on_gap_in_one([1, 2, 4, 5], 1, [7, 7, 8, 9])
    assert result == [[[1, 2], [7, 7]], [[4, 5], [8, 9]]]
