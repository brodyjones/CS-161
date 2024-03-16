##############
# Homework 3 #
##############

# Exercise: Fill this function.
# Returns the index of the variable that corresponds to the fact that
# "Node n gets Color c" when there are k possible colors
from calendar import c


def node2var(n, c, k):
    index = (n-1)*k + c
    return index

# Exercise: Fill this function
# Returns *a clause* for the constraint:
# "Node n gets at least one color from the set {1, 2, ..., k}"
def at_least_one_color(n, k):
    clauses = []
    i = 1
    while i <= k:
        clauses.append(node2var(n, i, k))
        i += 1
    return clauses
    

# Exercise: Fill this function
# Returns *a list of clauses* for the constraint:
# "Node n gets at most one color from the set {1, 2, ..., k}"
def at_most_one_color(n, k):
    init_list = at_least_one_color(n, k)
    c_list = []
    i = 0 
    while i < len(init_list): 
        j = i + 1
        while j < len(init_list):
            clauses = []
            clauses.append(-init_list[i])
            clauses.append(-init_list[j])
            c_list.append(clauses)
            j += 1
        i += 1
    return c_list


# Exercise: Fill this function
# Returns *a list of clauses* for the constraint:
# "Node n gets exactly one color from the set {1, 2, ..., k}"
def generate_node_clauses(n, k):
    c_list = []
    for c in at_most_one_color(n, k):
        c_list.append(c)
    c_list.append(at_least_one_color(n, k))
    return c_list

# Exercise: Fill this function
# Returns *a list of clauses* for the constraint:
# "Nodes connected by an edge e (represented by a list)
# cannot have the same color"
def generate_edge_clauses(e, k):
    e1 = e[0] 
    e2 = e[1]
    c_list = [] 
    for c in range(1, k+1):
        c_list.append([-node2var(e1, c, k), -node2var(e2, c, k)])
    return c_list



# The function below converts a graph coloring problem to SAT
# DO NOT MODIFY
def graph_coloring_to_sat(graph_fl, sat_fl, k):
    clauses = []
    with open(graph_fl) as graph_fp:
        node_count, edge_count = tuple(map(int, graph_fp.readline().split()))
        for n in range(1, node_count + 1):
            clauses += generate_node_clauses(n, k)
        for _ in range(edge_count):
            e = tuple(map(int, graph_fp.readline().split()))
            clauses += generate_edge_clauses(e, k)
    var_count = node_count * k
    clause_count = len(clauses)
    with open(sat_fl, 'w') as sat_fp:
        sat_fp.write("p cnf %d %d\n" % (var_count, clause_count))
        for clause in clauses:
            sat_fp.write(" ".join(map(str, clause)) + " 0\n")


# Example function call
if __name__ == "__main__":
    graph_coloring_to_sat("graph2.txt", "graph2_3colors.txt", 3)
