# Maximal Char Requests
# Hack the Interview II - April 2020
# ----------------------------------- Prompt ------------------------------------
# Given a string of upper and lower case English letters and a list of intervals,
# determine the count of the greatest case-insensitive letter in each interval.
# ---------------------------------- Solution -----------------------------------
# Method 1:
# * This method times out for larger cases *
# Turn string into all lowercase. Scan each interval of the string, keeping 
# track of the max char and its count.
# Time: O(n * intervals) | Space: O(1)
#
# Method 2:
# * This method times out for larger cases *
# Turn string into all lowercase. Use a hash map to record the max char and 
# count of every interval checked. Check the hash map every time an interval is 
# being queried to avoid repeated iterations through the same interval.
# Time: O(n * intervals) | Space: O(1)
#
# Method 3
# Run through the string and create a hash map of the indices of every letter in 
# the alphabet. Then, for each letter, starting with the last, run through all 
# of the intervals, checking which ones contain any indices of the current 
# letter using modified binary search. If an interval does, then count how many 
# indices are contained within that interval, and store it as the interval's max 
# char and count.
# Creating the hash map takes O(n) time. Checking each letter will take 
# O(26 * intervals * logn) time, since there will be 26 runs through the interval
# array and each interval will require a logn binary search.
# Time: O(n) + O(intervals * logn)

from bisect import bisect_left, bisect_right
from collections import defaultdict
from typing import List

def getMaxCharCount(s: str, queries: List[List[int]]) -> List[int]:
    """
    Method 1
    """
    # Make string all lowercase
    s = s.lower()
    res = []
    for query in queries:
        i, j = query
        # Current max char and its count
        max_char, count = -1, 0
        # Run through entire interval
        for k in range(i, j + 1):
            # If current char is greater than max char
            if ord(s[k]) > max_char:
                # Update max char and reset count
                max_char = ord(s[k])
                count = 1
            # If current char is same as max char, increment count
            elif ord(s[k]) == max_char:
                count += 1
            else:
                pass
        res.append(count)
    return res

def getMaxCharCount_2(s: str, queries: List[List[int]]) -> List[int]:
    """
    Method 2
    """

    # Get stored max char and count of remaining range and update current char
    def remaining_range(k: int, j: int, query_dic: Dict[int], max_char: int, 
                        count: int) -> Union[int, int]:
        # Get stored max char and count
        kj_max_char, kj_count = query_dic[(k, j)]
        # If current char is less than max char of remaining range
        if kj_max_char > max_char:
            # Then max char of remaining range is max char of entire range
            max_char = kj_max_char
            count = kj_count
        # If current char is same as max char of remaining range
        elif kj_max_char == max_char:
            # Add counts together
            count += kj_count
        # If current char is greater than max char of remaining range, then ignore
        # remaining range
        else: 
            pass
        return max_char, count

    # Check if given char is new max char
    def check_char(char: int, max_char: int, count: int) -> Union[int, int]:
        # If current char is greater than max char
        if char > max_char:
            # Set new max char and reset count
            max_char = char
            count = 1 
        # If equal to max char, increment count
        elif char == max_char:
            count += 1
        # If less than max char, ignore it
        else:
            pass
        return max_char, count
   
    def check_range(i: int, k: int, j: int, query_dic: Dict[int], max_char: int,
                    count: int) -> Union[int, int, Dict[int], bool]:
        found = False
        # If remaining range has already been checked before, update max
        # char and count accordingly
        if (k, j) in query_dic:
            # Update char and count of entire range based on remaining range
            max_char, count = remaining_range(k, j, query_dic, max_char, count)
            # Add range to dictionary and break
            query_dic[(i, j)] = (max_char, count)
            found = True
        else:
            # Check if current range has been checked
            if (i, k) in query_dic:
                # If it has, then update max char and count
                max_char, count = query_dic[(i, k)]
            # If not, then calculate new max char and count
            else:
                # Update max char and count with current char
                max_char, count = check_char(ord(s[k]), max_char, count)
                # Add new calculation to dictionary
                query_dic[(i, k)] = (max_char, count)
        return max_char, count, query_dic, found

    # Make all lowercase
    s = s.lower()
    res = []
    query_dic = {}
    for query in queries:
        # Get start and and indices
        i, j = query
        # Make sure they're valid
        i, j = max(0, i), min(len(s) - 1, j)
        # Keep track of max char and count of max char
        max_char, count = -1, 0
        # Inclusive range (i, j would exclude j)
        for k in range(i, j + 1):
            # Update char and count for range
            max_char, count, query_dic, found = check_range(i, k, j, query_dic, 
                                                     max_char, count)
            if found:
                break
    res.append(count)
    return res

def getMaxCharCount(s: str, queries: List[int]) -> List[int]:
    """
    Method 3
    """

    # Takes an interval and the indices of a character and returns the count
    # of that character within the interval
    def check_interval(query: List[int], char_indices: List[int]) -> int:
        lower, upper = query
        # Force interval into valid indices
        lower, upper = max(0, lower), min(len(s) - 1, upper)
        # If lower is greater than upper, the interval is invalid
        if lower > upper:
            return 0
        # Use binary search to find which char indices the interval contains
        lower_i = bisect_left(char_indices, lower)
        upper_i = bisect_right(char_indices, upper)
        # Return count
        return upper_i - lower_i
   
    # Make string all lowercase
    s = s.lower()
    # Create dictionary of each char's indices
    char_dict = defaultdict(list)
    for i, c in enumerate(s):
        char_dict[ord(c)].append(i)
    # Array of each interval's max char count
    res = [0] * len(queries)
    # For each character from z to a
    for c in reversed(range(97, 123)):
        # If character exists in string
        if c in char_dict:
            # Run through list of queries to check if they contain character
            for query_i, query in enumerate(queries):
                c_indices = char_dict[c]
                # If interval hasn't set its highest letter count yet, then 
                # check if it contains current letter
                if not(res[query_i]):
                    res[query_i] = check_interval(query, c_indices)
    # Return array of max char counts
    return res

# Driver Code
cases = [   ('aAabBcba', [[2, 6], [1, 2], [2, 2], [0, 4], [0, 7]]),
            ('ddaaa', [[0, 4]]),
            ('ddddddd', [[1, 2], [0, 6]]),
            ('AbaBacD', [[0, 4]]),
            ('AbaBacD', [[0, 7], [1, 7], [2, 7], [3, 7], [4, 7], [5, 7], [6, 7], [7, 7]]),
            ('AbaBacD', [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7]]),
            ('AbaBacD', [[7, 7], [6, 7], [5, 7], [4, 7], [3, 7], [2, 7], [1, 7], [0, 7]]),
            ('', [[100000, 0], [0, 9]]),
            ('abcdefhijklMnopQrstVvwxYz', [[0, 100], [-100, 5], [5, 6], [0, 10], [10, 20], [20, 50], [50, 75], [1, 1], [100, 100], [-5, -5],  [10, 20]]),
            ('fazcdefz', [[0, 7]]),
            ('abcdefhijklMnopQrstVvwxYz', [[-100, 5]])
]
for case in cases:
    s, queries = case
    print(getMaxCharCount(s, queries))
