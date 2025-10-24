def split_two_on_gap_in_one(
    seq_to_split_on: list[float],
    threshold_for_split: float,
    *other_seqs: list[float],
) -> list[list[list[float]]]:
    """Given a sequence and a threshold, this will traverse the sequence and split it
    into multiple lists whenever the difference between two elements is greater than the
    threshold. If other_seqs are passed, they will be split at the same indexes as the
    first one, but the other_seqs are not inspected. For example:

    ```python
    split_two_on_gap_in_one([1,2,4,5], 1)  # -> [[[1,2],[4,5]]]
    split_two_on_gap_in_one([1,2,4,5], 1, [3,4,5,9])  # -> [[[1,2],[4,5]],[[3,4],[5,9]]]

    Args:
        seq_to_split_on (list[float]): list of floats to split based on a threshold
        threshold_for_split (float): threshold to split sequence on 

    Raises:
        ValueError: if all sequences are not the same length

    Returns:
        list[list[list[float]]]: list of split results
    """
    n = len(seq_to_split_on)

    if any(len(s) != n for s in other_seqs):
        raise ValueError("All sequences must have the same length")
    if n == 0:
        return []
    groups = []
    start = 0
    for i in range(1, n):
        if seq_to_split_on[i] - seq_to_split_on[i - 1] > threshold_for_split:
            a_slice = seq_to_split_on[start:i]
            b_slices = [s[start:i] for s in other_seqs]
            groups.append([a_slice] + b_slices)
            start = i
    # final chunk
    a_slice = seq_to_split_on[start:]
    b_slices = [s[start:] for s in other_seqs]
    groups.append([a_slice] + b_slices)
    return groups
