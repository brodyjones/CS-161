##############
# Homework 2 #
##############

##############
# Question 1 #
##############

# comment code

def BFS(FRINGE):
    fringe_list = list(FRINGE)
    leaf_nodes = [] #list to leaf nodes, in order of visitation by BFS

    if len(FRINGE) == 0:
        return leaf_nodes # if tree is empty, return empty list

    if len(FRINGE) == 1: # single node base case
        if type(FRINGE[0]) == tuple:
            return BFS(FRINGE[0]) # if single node is a tree, expand it
        else:
            leaf_nodes.append(FRINGE[0])
            return leaf_nodes # otherwise return list containing single leaf node

    i = 0
    next_search = [] # list of nodes in our frontier, will be expanded by recursion call
    while i < len(FRINGE):
        if type(FRINGE[i]) != tuple:
            leaf_nodes.append(FRINGE[i]) # if node is a leaf, add it to the list 
        else:
            j = 0
            while j < len(FRINGE[i]):
                next_search.append(FRINGE[i][j]) # if node contains a subtree, add it to frontier
                j += 1
        i += 1
    n_search = tuple(next_search)
    return leaf_nodes + BFS(n_search) # recursion call to search nodes in frontier




##############
# Question 2 #
##############


# These functions implement a depth-first solver for the homer-baby-dog-poison
# problem. In this implementation, a state is represented by a single tuple
# (homer, baby, dog, poison), where each variable is True if the respective entity is
# on the west side of the river, and False if it is on the east side.
# Thus, the initial state for this problem is (False False False False) (everybody
# is on the east side) and the goal state is (True True True True).

# The main entry point for this solver is the function DFS, which is called
# with (a) the state to search from and (b) the path to this state. It returns
# the complete path from the initial state to the goal state: this path is a
# list of intermediate problem states. The first element of the path is the
# initial state and the last element is the goal state. Each intermediate state
# is the state that results from applying the appropriate operator to the
# preceding state. If there is no solution, DFS returns [].
# To call DFS to solve the original problem, one would call
# DFS((False, False, False, False), [])
# However, it should be possible to call DFS with a different initial
# state or with an initial path.

# First, we define the helper functions of DFS.

# FINAL-STATE takes a single argument S, the current state, and returns True if it
# is the goal state (True, True, True, True) and False otherwise.
def FINAL_STATE(S):
    i = 0
    while i < len(S):
        if S[i] == False:
            return False
        else:
            i += 1
    return True # return true if all elements of S are true


# NEXT-STATE returns the state that results from applying an operator to the
# current state. It takes three arguments: the current state (S), and which entity
# to move (A, equal to "h" for homer only, "b" for homer with baby, "d" for homer
# with dog, and "p" for homer with poison).
# It returns a list containing the state that results from that move.
# If applying this operator results in an invalid state (because the dog and baby,
# or poisoin and baby are left unsupervised on one side of the river), or when the
# action is impossible (homer is not on the same side as the entity) it returns None.
# NOTE that next-state returns a list containing the successor state (which is
# itself a tuple)# the return should look something like [(False, False, True, True)].
def NEXT_STATE(S, A):
    
    if A == "h": # mover homer
        new_tup = (not S[0], S[1], S[2], S[3]) 

    if A == "b":# mover homer and baby
        if S[0] != S[1]: 
            return None
        new_tup = (not S[0], not S[1], S[2], S[3])

    if A == "d": # mover homer and dog
        if S[0] != S[2]:
            return None
        new_tup = (not S[0], S[1], not S[2], S[3])

    if A == "p": # mover homer and poison
        if S[0] != S[3]:
            return None
        new_tup = (not S[0], S[1], S[2], not S[3])

    if new_tup[0] != new_tup[1]: # if homer isn't on the same side as the baby
        if new_tup[1] == new_tup[2] or new_tup[1] == new_tup[3]: # and the baby is alone with either the dog or the poison
            return None

    n_state = []
    n_state.append(new_tup)
    return n_state

    


# SUCC-FN returns all of the possible legal successor states to the current
# state. It takes a single argument (s), which encodes the current state, and
# returns a list of each state that can be reached by applying legal operators
# to the current state.
def SUCC_FN(S):
    succ_states = [] # for each potential move, add it to the list if it is valid
    if NEXT_STATE(S, "h") != None:
        succ_states += NEXT_STATE(S, "h")
    if NEXT_STATE(S, "b") != None:
        succ_states += NEXT_STATE(S, "b")
    if NEXT_STATE(S, "d") != None:
        succ_states += NEXT_STATE(S, "d")
    if NEXT_STATE(S, "p") != None:
        succ_states += NEXT_STATE(S, "p")
    
    return succ_states


# ON-PATH checks whether the current state is on the stack of states visited by
# this depth-first search. It takes two arguments: the current state (S) and the
# stack of states visited by DFS (STATES). It returns True if s is a member of
# states and False otherwise.

def ON_PATH(S, STATES):
    if STATES.count(S) != 0: # if S appears in STATES a nonzero amount of times
        return True
    else: 
        return False


# MULT-DFS is a helper function for DFS. It takes two arguments: a list of
# states from the initial state to the current state (PATH), and the legal
# successor states to the last, current state in the PATH (STATES). PATH is a
# first-in first-out list of states# that is, the first element is the initial
# state for the current search and the last element is the most recent state
# explored. MULT-DFS does a depth-first search on each element of STATES in
# turn. If any of those searches reaches the final state, MULT-DFS returns the
# complete path from the initial state to the goal state. Otherwise, it returns
# [].

def MULT_DFS(STATES, PATH):
    i = 0
    while i < len(STATES): # for each potential move
        temp = DFS(STATES[i], PATH) # search for the goal state
        if temp != False:
            return temp # return full path if goal is found by any state
        i += 1
    return []

    



# DFS does a depth first search from a given state to the goal state. It
# takes two arguments: a state (S) and the path from the initial state to S
# (PATH). If S is the initial state in our search, PATH is set to False. DFS
# performs a depth-first search starting at the given state. It returns the path
# from the initial state to the goal state, if any, or False otherwise. DFS is
# responsible for checking if S is already the goal state, as well as for
# ensuring that the depth-first search does not revisit a node already on the
# search path.
def DFS(S, PATH):
    if PATH == False:
        PATH = [] # create empty path if none exists

    if ON_PATH(S, PATH) == False:
        PATH.append(S) # add S to the PATH if is is not already there
    else: 
        return False # if it is return false

    if FINAL_STATE(S) == True:
        return PATH # if S is the goal state then return the path

    temp = MULT_DFS(SUCC_FN(S), PATH) # search each succesive path
    if temp == []: 
        return False # if no goal is found return false
    else:
        return temp  # otherwise return the first found path
    
    

