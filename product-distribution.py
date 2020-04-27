# Product Distribution
# Hack the Interview II - April 2020
# ----------------------------------- Prompt ------------------------------------
# Given an array of integers and a threshold m, find the maximum score such 
# that:
# 1. There are an infinite amount of "buckets" labeled 1 ... inf
# 2. You can only fill a bucket if the previous bucket is filled to 
#    threshold m
# 3. No bucket can contain less than m integers, but the last bucket can
#    contain more than m integers
# 4. The score is calculated by multiplying each integer by its bucket label
#    and adding them all together
# ----------------------------------- Solution ----------------------------------
# Sort the array from smallest to largest so that we minimize numbers being 
# multiplied by the smallest bucket numbers. Then iterate through number of 
# buckets, calculate indices of items belonging to that bucket, and add to score.
# Then add all leftover / overflow integers to the last bucket and add to score.
# Sort takes O(nlgn) time, score calculation takes O(n) time.
# Time: O(nlgn) | Space: O(1)

from typing import List

def maxScore(a: List[int], m: int) -> int:
    a = sorted(a)
    # Calculate number of buckets needed and number of overflow integers
    segs, overflow = len(a) // m, len(a) % m
    # Sum integers multiplied by their buckets
    max_score = 0
    # Iterate over each bucket
    for i in range(segs):
        # Iterate over each number in the bucket (0 -> m)
        for j in range(m):
            # Calculate corresponding index and
            # Adjust from 0-indexing to 1-indexing
            max_score += a[(i * m) + j] * (i + 1)
    # Place overflow into last bucket (index == number of buckets)
    for i in range(overflow):
        max_score += a[(segs * m) + i] * segs
    # Modulo 10^9 + 7 as per question prompt
    return max_score % (10 ** 9 + 7)

# Driver Code
cases = [   ([4, 1, 9, 7],                          4, 21),
            ([1, 5, 4, 2, 3],                       2, 27),
            ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],   3, 171),
            ([],                                    5, 0),
            ([1, 2, 3, 4],                          1, 30)
]
for case in cases:
    a, m, expected = case
    res = maxScore(a, m)
    print("Passed" if res == expected else \
          "{0} failed with {1} expected {2}".format((a, m), res, expected))
