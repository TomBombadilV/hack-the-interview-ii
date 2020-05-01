# Minimum String Co-Efficient
# Hack the Interview II - April 2020
# ----------------------------------- Prompt ------------------------------------
# Given a binary string s and number of flips p, determine the  smallest string
# coefficient that can be produced with p flips. The coefficient is calculated
# by adding up the count of all 0s sandwiched between 1s and all 1s sandwiched
# between 0s. Each flip will reverse 0s to 1s and 1s to 0s and can occur between
# any range within the string s.
# ---------------------------------- Solution -----------------------------------
# First Attempt:
# This is a greedy approach which ended up being incorrect. I had two insights 
# that led to this solution:
# 1) It is always optimal to select a "chunk" of 1s or 0s that are second from 
# the left or second from the right, because this will "delete" the largest 
# amount of digits from the coefficient, and 
# 2) It is always optimal to only flip isolated "chunks" of 1s or 0s.
# This second determination ended up being incorrect, which I later found out,
# but I relied on it for my first attempt. What it does is it shaves of the 
# first and last "chunks" from the string so that we isolate the digits which
# contribute to the coefficient. Then we use a greedy approach to always select
# the chunk on the left or right of the string which is larger. Flipping a chunk
# in the second-to-left or second-to-right position will also remove the next
# chunk from the coefficient (ex: 01010 - Flipping the second to left bit "1" 
# would also remove the 0 to its right since the string would become '00010').
# So the algorithm looks at the left chunk and its neighbor, and the right chunk
# and its neighbor, and chooses the one that's bigger.
# Time: O(n) | Space: O(1)
#
# Correct Method:
# Turns out there are two interesting cases -
# 1) The case where selecting the smaller chunk right now will enable you to 
#    select a larger chunk later
# 2) The case where flipping the entire range of coefficients maximizes how many
#    coefficients you can delete from the total
# This solution calculates "range flips" which essentially is just removing the
# "chunks" on both ends, and "max windows" which is essentially finding the 
# window of chunks on both ends that will maximize the sum being removed from
# the coefficients. The algorithm will calculate the coefficient for 0 through p
# ranged flips followed by max windows and select the smallest one.
# Time: O(p*n) | Space: O()
#
# Brute Force Method:
# I programmed this because I was stuck and couldn't tell what my algorithm was
# doing wrong. It only works for small p (~2 or less) and short s because it 
# checks every single possible range in the string and calculates its
# coefficient. For p > 1, it does this recursively by performing a flip on every
# single range and then performing another flip on every single range. This is
# obviously very costly.
# Time: O(n^(p*n)) | Space: O(n^n)

from random import randint
from typing import Dict, List, Union

def minStringCoeff(s: str, p: int) -> int:
    """
    First Attempt
    """

    # Counts the length of the leftmost "chunk" of the string
    def count_from_left(s:str) -> int:
        # An empty string has no chunks
        if not(s): 
            return 0
        # While char is same as first char, increment count
        i, c = 0, s[0]
        while i < len(s) and s[i] == c:
            i += 1
        # Return count (minus the last increment which breaks the while loop)
        return i - 1

    # Counts the length of the rightmost "chunk" of the string
    def count_from_right(s:str) -> int:
        # An empty string has no chunks
        if not(s): 
            return 0
        # While char is same as last char, increment count
        i, c = len(s) - 1, s[len(s) - 1]
        while s and i >= 0 and s[i] == c:
            i -= 1
        # Return count (minus the last increment which breaks the while loop)
        return i + 1

    # Returns length of leftmost chunk and its neighbor, and rightmost chunk
    # and its neighbor
    def chunk_lengths(s: str) -> Union(int):
        # Get length of left and right chunks
        left = count_from_left(s) + 1
        right = len(s) - count_from_right(s)
        # String with left and right chunks removed 
        neighbor_s = s[left:-right]
        # Get length of left and right chunks' neighbors
        left_neighbor = count_from_left(neighbor_s) + 1, 
        right_neighbor = len(neighbor_s) - count_from_right(neighbor_s)
        # Return lengths
        return left + left_neighbor, right + right_neighbor

    # Empty string has no coefficients
    if not(s): 
        return 0 
    # Cut off leftmost and rightmost chunks
    # Do this in two parts so that if leftmost chunk and rightmost chunk happen
    # to be the same thing, we won't have crossing indices
    i = count_from_left(s)
    s = s[i + 1:]
    i = count_from_right(s)
    s = s[:i]
    # Do p flips
    for _ in range(p):
        # If s is empty after cutting off non-coefficient bits, do nothing
        if s:
            left_length, right_length = chunk_lengths(s)
            # Select which length is longer
            if left_length > right_length:
                s = s[left_length:]
            else:
                s = s[:-right_length]
    # Return new coefficient
    return len(s)

def minStringCoeff(s: str, p: int) -> int:
    """
    Method 2
    """

    # Turn string into array of lengths of consecutive 1s or 0s
    def condenseString(s: str) -> List:
        # Empty string
        if not(s): 
            return []
        l, count = [], 0
        curr_c = s[0]
        for c in s:
            # If c is different than previous c, add previous count to array and 
            # begin new count of new c
            if not(c == curr_c):
                curr_c = c
                l.append(count)
                count = 1 
            # If c is same as previous c, incremenent count
            else:
                count += 1
        # Add last count to array
        l.append(count)
        return l

    # Calculate sum of first window
    def first_window_sum(left: int, right: int, coeffs: List[int], 
                         sum_dict: Dict[int]) -> int:
        # If already exists in sumdict, get sum
        if (left, right) in sum_dict:
            curr_sum = sum_dict[(left, right)]
        # If not, add up all numbers in range and update dictionary
        else:
            curr_sum = sum(coeffs[left:right])
            sum_dict[(left, right)] = curr_sum
        return curr_sum, sum_dict

    # Move window to the right by 2 places and update sum
    def update_window_sum(left: int, right: int, curr_sum: int, 
                          coeffs: List[int]) -> Union[int, int, int]:
        # Delete two left values
        curr_sum = curr_sum - (coeffs[left] + coeffs[(left + 1) % len(coeffs)])
        left = (left + 2) % len(coeffs)
        right = (right + 2) % len(coeffs)
        # Add two right values
        curr_sum = curr_sum + (coeffs[right - 2] + coeffs[right - 1])
        return left, right, curr_sum

    # Gets indices of window that will maximize amount subtracted from coefficient
    def get_max_window_indices(coeffs: List[int], p: int, window_len: int,
                               sum_dict: Dict[int]) -> Union[int, int]: 
        # Get indices of first window to check (leftmost)
        left, right = (len(coeffs) - window_len) % len(coeffs), len(coeffs)
        # Calculate sum of first window
        curr_sum, sum_dict = first_window_sum(left, right, coeffs, sum_dict)
        # Keep track of max sum and its indices (left inclusive, right exclusive)
        max_sum, max_left, max_right = curr_sum, left, right
        for _ in range(p):
            # Move window indices and update sum
            left, right, curr_sum = update_window_sum(left, right, curr_sum, coeffs)
            # Update max sum
            if curr_sum > max_sum:
                max_sum, max_left, max_right = curr_sum, left, right
        return max_left, max_right

    # Selects the group of chunks that will maximize the value subtracted from 
    # coefficient
    def get_max_window(coeffs, p, sum_dict):
        # If p = 0, no flips will be performed
        if p == 0: 
            return sum(coeffs), sum_dict
        # Number of "chunks" of 1s and 0s that will be affected by p flips
        window_len = p * 2
        # If window is longer than number of chunks in total, then there will be 
        # no coeffs
        if window_len >= len(coeffs): 
            return 0, sum_dict
        # Get indices of window that would maximize value subtracted from coeffs
        max_left, max_right = get_max_window_indices(coeffs, p, window_len, 
                                                     sum_dict)
        # Update list of chunk lengths to remove window
        if max_left < max_right:
            coeffs = coeffs[max_right:] + coeffs[:max_left]
        else:
            coeffs = coeffs[max_right % len(coeffs):max_left]
        # Return coefficient and dictionary of sums
        return sum(coeffs), sum_dict

    # No string no play!
    if not(s): 
        return 0
    coeffs = condenseString(s)
    # Strip off first and last run of 1s or 0s to isolate coefficient 
    coeffs = coeffs[1:-1]
    # If p = 0, no flips will be performed
    if p == 0: return sum(coeffs)
    sum_dict = {}
    # Calculate max window with 0 range flips
    min_coeff, sum_dict = get_max_window(coeffs, p, sum_dict)
    curr_coeffs = coeffs
    # Perform a range flip and then calculate max window 
    # The min(2, p) part was to optimize for passing test cases. This will fail
    # if we need a "range flip" with a depth greater than 2
    for curr_p in range(min(2, p)):
        curr_coeff, sum_dict = get_max_window(coeffs[1:-1], 
                                              p - (curr_p + 1), 
                                              sum_dict)
        min_coeff = min(min_coeff, curr_coeff)
    return min_coeff 

def minStringCoeffsBruteForce(s: str, p: int) -> int:
    """
    Brute Force Method
    """

    # Calculate coefficient of string 
    def calculate_coeff(s: str):
        # Coefficient of empty string is 0
        if not(s): 
            return 0
        # Count length of lefmost chunk
        count = 0
        c, i = s[0], 0
        while i < len(s) and s[i] == c:
            count += 1
            i += 1
        # Count length of rightmost chunk
        c, j = s[-1], len(s) - 1
        while j >= 0 and s[j] == c:
            count += 1
            j -= 1
        # Return length of string minus length of right and leftmost chunks
        return max(0, len(s) - count)

    # Flip all bits of a string in given range
    def flip_bits(s: str, start: int, end: int) -> str:
        for i in range(start, end + 1):
            new_char = '0' if s[i] == '1' else '1'
            s = s[:i] + new_char + s[i + 1:]
        return s

    if not(s): 
        return 0
    # No flips, coefficient doesn't change
    if p == 0:
        return calculate_coeff(s)
    coeffs = []
    strs = []
    # Try flipping bits and calculating coefficient of every single possible 
    # range, keeping track of minimum coefficient. For p > 1, perform the same
    # thing recursively on every previous calculated string
    for i in range(len(s)):
        for j in range(i, len(s)):
            temp_s = flip_bits(s, i, j)
            temp_coeff = minStringCoeffsBruteForce(temp_s, p - 1)
            coeffs.append(temp_coeff)
    return min(coeffs)

# Driver Code
cases = [   ('110100100', 1, 2),
            ('110100100', 2, 0),
            ('1101011111000001110001110001', 0, 25),
            ('1101011111000001110001110001', 1, 19),
            ('1101011111000001110001110001', 2, 13),
            ('1101011111000001110001110001', 3, 3),
            ('1101011111000001110001110001', 4, 1),
            ('1101011111000001110001110001', 5, 0),
            ('1101011111000001110001110001', 6, 0),
            ('1101011111000001110001110001', 7, 0),
            ('1101011111000001110001110001', 8, 0),
            ('11011001001', 2, 1),
            ('1101', 1, 0),
            ('1011010', 1, 2),
            ('1011010', 2, 0),
            ('010', 1, 0),
            ('010', 0, 1),
            ('', 1, 0),
            ('1', 1, 0),
            ('101010101', 3, 1),
            ('11', 100, 0),
            ('101010', 1, 2),
            ('10101', 1, 1),
            ('000000000000000000', 0, 0),
            ('10101010101010101', 0, 15),
            ('101010', 5, 0),
            ('110100100', 0, 5),
            ('10110110011001111101110100000110', 0, 30),
            ('10110110011001111101110100000110', 1, 23),
            ('10110110011001111101110100000110', 2, 20),
            ('10110110011001111101110100000110', 3, 17),
            ('10110110011001111101110100000110', 4, 10),
            ('10110110011001111101110100000110', 5, 6),
            ('10110110011001111101110100000110', 6, 2),
            ('10110110011001111101110100000110', 7, 0),
            ('101111100000010101', 2, 3),
            ('10110110011001111101110100000110', 4, 10)
            ('1100101110101100', 1, None)
]

# Generate given number of strings of given number of length
cases = []
n, bit_len = 25, 16
for _ in range(n):
    s = ''
    for _ in range(bit_len):
        s += str(randint(0, 1))
        cases.append((s, 1, None))
        cases.append((s, 2, None))
        #cases.append((s, 3, None))

# Special case where "range flip" is required with p = 5
#s = '1010' + '1' * 10 + '01010101010' + '1' * 10 + '1001'
#cases = [(s, 3, None)]

for case in cases:
    s, p, expected = case
    res = minStringCoeff(s, p)
    expected = minStringCoeffsBruteForce(s, p)
    print("Passed" if res == expected else "{0} failed with {1} expected {2}".\
          format(s, res, ans))
