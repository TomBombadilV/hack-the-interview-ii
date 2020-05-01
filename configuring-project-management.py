# Configuring Project Management
# Hack the Interview II - April 2020
# ----------------------------------- Prompt ------------------------------------
# Given an array of relationships between 1 -> n students, determine which 
# integers are friends with student 1 and are not friends with student 2 or any
# of student 2's friends.
# ---------------------------------- Solution ----------------------------------
# Method 1: 
# * This solution times out for large cases due to the n x n matrix *
# Create an adjacency matrix to represent the graph. Then, get an array of all
# of two's friends. For each of two's friends x, if they have an edge with
# student 1, remove that edge. Then for all of x's friends, check if they have
# an edge with student 1. If so, remove it. Then, return the array of all of 1's
# friends.
# Time: O(vertices + edges) | Space: O(vertices * vertices)
#
# Method 2:
# Create a set of all of two's friends by iterating through the array of 
# friendships and checking for a 2. Then create a set of all of two's friends'
# friends by iterating through the friendship array again and checking for 
# any friend in the two's friends set. Finally, iterate once more through the
# array, checking for all friendships between 1 and anyone not in the two sets.
# Time: O(edges) | Space: O(vertices)

from random import randint
from typing import List

def configureProjectPresentation(n: int, friendships: List[List[int]]) -> List[int]:
    """
    Method 1
    """
    # If there are only 2 students, return empty
    if n < 3: 
        return [-1]
    
    # Create adjacency matrix
    m = [[0 for _ in range(n)] for _ in range(n)]
    # Add each friendship to the adjacency matrix
    for f in friendships:
        # Make sure vertices are valid
        if f[0] - 1 < n and f[1] - 1 < n and f[0] >= 0 and f[1] >= 0:
            # Undirected graph, so edges going both ways (and adjust from 
            # 1-index to 0-index)
            m[f[0] - 1][f[1] - 1] = 1
            m[f[1] - 1][f[0] - 1] = 1
    
    # Get list of two's friends
    two_friends = [i for i in range(1, n) if m[1][i] == 1]
    # Go through all of two's friends
    for tf in two_friends:
        # If friends with student 1 (index 0), remove edge from 1 to friend
        if m[0][tf] == 1:
            m[0][tf] = 0
        # Go through all of tf's friends
        for i in range(1, n):
            # If friends with tf
            if m[tf][i] == 1:
                # If friends with student 1 (index 0), remove edge
                if m[0][i] == 1:
                    m[0][i] = 0
    
    # Get list of all of 1's remaining friends (excluding 2 (index 1))
    invites = [i + 1 for i in range(1, n) if m[0][i] == 1 and not(i == 1)]
    return invites if invites else [-1]

def configureProjectPresentation(n: int, friendships: List[List[int]]) -> List[int]:
    """
    Method 2
    """
    twos_friends, twos_friends_friends = set(), set()
    invitees = set()
    i = 0
    
    # Remove all edges that are invalid (negative or > n)
    while i < len(friendships):
        if friendships[i][0] < 0 or friendships[i][1] < 0 or\
           friendships[i][0] > n or friendships[i][1] > n:
            friendships = friendships[:i] + friendships[i + 1:]
        else:
            i += 1
    
    # Add all of twos friends to a set
    for f in friendships:
        if f[0] == 2 and not(f[1] == 1) and not(f[1] == 2):
            twos_friends.add(f[1])
        if f[1] == 2 and not(f[0] == 1) and not(f[0] == 2):
            twos_friends.add(f[0])
    
    # Add all of twos twos friends to a set
    for f in friendships:
        if f[0] in twos_friends and not(f[1] == 1) and not(f[1]) == 2 and \
            not(f[1] in twos_friends):
            twos_friends_friends.add(f[1])
        if f[1] in twos_friends and not(f[0] == 1) and not(f[1]) == 2 and \
            not(f[0] in twos_friends):
            twos_friends_friends.add(f[0])
    
    # Add all of ones friends that arent twos friends or twos twos friends to set
    for f in friendships:
        if f[0] == 1 and not(f[1] == 1) and not(f[1] == 2) and \
            not(f[1] in twos_friends) and not(f[1] in twos_friends_friends):
            invitees.add(f[1])
        if f[1] == 1 and not(f[0] == 1) and not(f[0] == 2) and \
            not(f[0] in twos_friends) and not(f[0] in twos_friends_friends):
            invitees.add(f[0])
    
    # Return sorted invitees
    return sorted(list(invitees)) if invitees else [-1]

# Driver Code
cases = [   (10 ** 6, []),
            (2, [[1, 2]]),
            (3, [[3, 2], [1, 2]]),
            (2, [[1, 3],[4, 6], [1, 5]]),
            (4, [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]),
            (6, [[1, 5], [1, 2], [1, 3], [1, 4], [2, 4], [2, 6], [3, 6]]),
            (9, [[1, 3],[1, 4], [3, 2], [5, 6], [7, 1], [2, 8], [8, 9], [9, 1]])
]

# Generate a random case with 10 students and 15 friendships
n = 10
friendships = []
for i in range(15):
    a, b = randint(1, n), randint(1, n)
    friendships.append([a, b])
cases.append((n, friendships))

for case in cases:
    n, friendships = case
    print(configureProjectPresentation(n, friendships))
