from hopcroftkarp import HopcroftKarp
from tarjan import tarjan
import time
import string
import random

import tester2

now = time.time()
total = 0


def perfect_matching_algorithm(x_to_y_graph):
    # No maximum matching edges a.k.a 0-persistent edges
    e_0 = set()
    # Some maximum matching edges a.k.a weakly persistent edges
    e_w = set()
    # All maximum matching edges a.k.a 1-persistent edges
    e_1 = set()

    # Find the maximum matching of the graph
    matching = HopcroftKarp(x_to_y_graph).maximum_matching()

    # Create a directed graph to find strongly connected components later
    directed_graph = {}
    # Create a directed graph from an undirected graph For each left node in the graph
    for i in x_to_y_graph:
        result = []
        if i in matching:
            result.append(matching[i])
            directed_graph[i] = result
        # For each right node in the graph
        for j in x_to_y_graph[i]:
            result = []
            if j not in directed_graph[i]:
                if j not in directed_graph:
                    result.append(i)
                    directed_graph[j] = result
                else:
                    directed_graph[j].append(i)

    global tarjan
    # Use tarjan algorithm to find the strongly connected components
    tarjan_result = tarjan(directed_graph)
    sccs = []
    for i in tarjan_result:
        # Strongly connected components must be more than two
        if len(i) > 1:
            sccs.append(i)

    # If the edges from strongly connected components
    # Adding edges into weakly matching set - EW
    if sccs != 0:
        for scc in sccs:
            for i in scc:
                if i in x_to_y_graph:
                    for j in scc:
                        if j in x_to_y_graph[i]:
                            e_w.add(tuple((i, j)))

    # Adding edges into maximum matching set - E1
    for i in matching:
        if i in x_to_y_graph:
            edge = tuple((i, matching[i]))
            if edge not in e_w:
                e_1.add(edge)

    # Create a set of all edges
    edges = set()
    for i in x_to_y_graph:
        for j in x_to_y_graph[i]:
            edges.add(tuple((i,j)))

    # Adding edges into no maximum matching
    # set - E0
    e_0 = edges - e_w - e_1

    return e_0, e_w, e_1

def imperfect_matching_algorithm(x_to_y_graph):
    # A set to store + labelled vertices
    label_plus = set()
    # A set to store * labelled vertices
    label_star = set()
    # A set to store u labelled vertices
    label_u = set()

    # Create two sets to store X and Y vertices
    x_set = set()
    y_set = set()
    # Create two sets to store X and
    # Y labelled vertices
    x_labelled_set = set()
    y_labelled_set = set()
    # Create a turn around graph y to x graph
    y_to_x_graph = {}
    # Add X vertices and Y vertices into two sets
    for x in x_to_y_graph:
        x_set.add(x)
        for y in x_to_y_graph[x]:
            y_set.add(y)
            if y in y_to_x_graph:
                y_to_x_graph[y].add(x)
            else:
                values = set()
                values.add(x)
                y_to_x_graph[y] = values

    # To find exposed vertices in X and Y
    # Label the exposed vertices
    def label_exposed_vertices(
            vertices_set, labelled_set, label_set):
        labelled_set.clear()
        for i in vertices_set:
            if i not in matching:
                label_set.add(i)
                labelled_set.add(i)

    # To find the vertices that are connected to
    # the labelled vertices by an edge
    # And the edge are not in the matching
    # which created from Hopcroft algorithm
    # Label the vertices
    def label_unmatched_vertices(
            graph, labelled_set, labelled_set2, label_set):
        temp = set()
        for i in labelled_set:
            for j in graph[i]:
                if j not in labelled_set2:
                    if matching[j] != i:
                        label_set.add(j)
                        temp.add(j)
        if len(temp) != 0:
            labelled_set2.update(temp)
            return True
        else:
            return False

    # To find the vertices that are connected
    # to the labelled vertices by an edge
    # And the edge are in the matching
    # which created from Hopcroft algorithm
    # Label the vertices
    def label_matched_vertices(
            graph, labelled_set, labelled_set2, label_set):
        temp = set()
        for i in labelled_set:
            for j in graph[i]:
                if j not in labelled_set2:
                    if matching[j] == i:
                        label_set.add(j)
                        temp.add(j)
        if len(temp) != 0:
            labelled_set2.update(temp)
            return True
        else:
            return False

    # Label the exposed X vertices
    label_exposed_vertices(
        x_set, x_labelled_set, label_plus)
    # Create the while loop to start the labelling process
    while len(x_labelled_set) != 0:
        unmatched_y_is_added = label_unmatched_vertices(
            x_to_y_graph, x_labelled_set,
            y_labelled_set, label_plus)
        # If no more vertices to be labelled
        # then break the while loop
        if (unmatched_y_is_added == False):
            break
        matched_x_is_added = label_matched_vertices(
            y_to_x_graph, y_labelled_set,
            x_labelled_set, label_plus)
        # If no more vertices to be labelled
        # then break the while loop
        if (matched_x_is_added == False):
            break

    # Label the exposed Y vertices
    label_exposed_vertices(
        y_set, y_labelled_set, label_star)
    # Create the while loop to start the labelling process
    while len(y_labelled_set) != 0:
        unmatched_x_is_added = label_unmatched_vertices(
            y_to_x_graph, y_labelled_set,
            x_labelled_set, label_star)
        # If no more vertices to be labelled
        # then break the while loop
        if (unmatched_x_is_added == False):
            break
        matched_y_is_added = label_matched_vertices(
            x_to_y_graph, x_labelled_set,
            y_labelled_set, label_star)
        # If no more vertices to be labelled
        # then break the while loop
        if (matched_y_is_added == False):
            break
    # Store all the vertices from the graph
    all_vertices = x_set.union(y_set)
    labelled_vertices = label_plus.union(label_star)
    # Find the unlabelled vertices and store into label_u
    label_u = all_vertices.difference(labelled_vertices)


    # No maximum matching edges a.k.a 0-persistent edges
    # If one of these edges is in the matching
    # then it can't be maximum matching
    e_0 = set()
    # Some maximum matching edges
    # a.k.a weakly persistent edges
    e_w = set()
    # All maximum matching edges
    # a.k.a 1-persistent edges
    e_1 = set()

    # X vertices that exposed in >1 max matching
    a_x = set()
    # Y vertices that exposed in >1 max matching
    a_y = set()
    # X vertices that not in a_x
    # but adjacent to >1 vertices in a_y
    b_x = set()
    # Y vertices that not in a_y
    # but adjacent to >1 vertices in a_x
    b_y = set()
    # X vertices that not in a_x and b_x
    c_x = set()
    # Y vertices that not in a_y and b_y
    c_y = set()

    a_x = label_plus.intersection(x_set)
    a_y = label_star.intersection(y_set)
    b_x = label_star.intersection(x_set)
    b_y = label_plus.intersection(y_set)
    c_x = label_u.intersection(x_set)
    c_y = label_u.intersection(y_set)
    # Create a set of all edges
    edges = set()
    for i in x_to_y_graph:
        for j in x_to_y_graph[i]:
            edges.add(tuple((i,j)))

    def cartesian_product(x_set, y_set):
        result = set()
        for i in x_set:
            for j in y_set:
                result.add(tuple((i,j)))
        return result

    for i in edges:
        # If edge in (b_x * b_y)
        # or (b_x * c_y) or (c_x * b_y)
        # Add the edge into no maximum matching, e_0
        if (i in cartesian_product(b_x, b_y)) \
            or (i in cartesian_product(b_x, c_y)) \
            or (i in cartesian_product(c_x,b_y)):
            e_0.add(i)
        # If edge in (a_x * b_y) or (b_x * a_y)
        # Add the edge into some maximum matching, e_w
        elif (i in cartesian_product(a_x, b_y)) \
            or (i in cartesian_product(b_x, a_y)):
            e_w.add(i)
    # Let the remaining edges to be a set of new edges
    # The edges can form a perfect matching
    new_edges = edges - e_w - e_0

    # Create a new x_to_y_graph from the new edges
    x_to_y_graph_perfect = {}
    for x, y in new_edges:
        if x not in x_to_y_graph_perfect:
            list_y = set()
            list_y.add(y)
            x_to_y_graph_perfect[x] = list_y
        else:
            x_to_y_graph_perfect[x].add(y)
    # Compute the perfect matching algorithm for
    # the new edges since they can be perfect matching
    # To speed up the execution time
    e0_new, ew_new, e1_new = \
        perfect_matching_algorithm(x_to_y_graph_perfect)
    # Adding back the partitioned edges into the results
    e_0.update(e0_new)
    e_w.update(ew_new)
    e_1.update(e1_new)

    return e_0, e_w, e_1


def judgment_bipartite_graphs(e_0p, e_wp, e_1p):
    e_1 = set()
    for edge in e_1p:
        modified_edge = tuple(
            (node[:-2] if node.startswith('y')
             else node) for node in edge)
        e_1.add(modified_edge)

    e_0 = set()
    for edge in e_0p:
        modified_edge = tuple(
            (node[:-2] if node.startswith('y')
             else node) for node in edge)
        e_0.add(modified_edge)

    e_w = set()
    edge_count = {}
    for edge in e_wp:
        modified_edge = (edge[0], edge[1][:-2])
        if modified_edge in edge_count:
            edge_count[modified_edge] += 1
        else:
            edge_count[modified_edge] = 1

    E1 = set()
    Ew = set()

    for edge, count in edge_count.items():
        if count > 1:
            E1.add(edge)
        else:
            Ew.add(edge)

    En = set()
    common_x = set()
    for edge in E1:
        x = edge[0]
        same_x_edges = set(
            e for e in E1 if e[0] == x)
        if len(same_x_edges) > 1:
            En |= same_x_edges

    E1 -= En

    common_x = set()
    for edge in Ew:
        common_x.add(edge[0])

    for edge in E1:
        if edge[0] in common_x:
            En.add(edge)

    E1 -= En
    Ew -= En

    merged_set = Ew | En

    E_1 = e_1 | E1
    E_w = merged_set
    E_0 = e_0
    return E_0, E_w, E_1

def generate_bipartite_graph(x_no, y_no, edges_no):
    # The number of edges must be bigger than the maximum
    # between number of X nodes and number of Y nodes
    if edges_no < max(x_no, y_no):
        raise ValueError("edges_no is too small, "
                         "it must be bigger or equal to "
                         + str(max(x_no, y_no)))
    # The number of edges must be smallar or equal to the
    # product of number of X nodes and number of Y nodes
    if edges_no > x_no * y_no:
        raise ValueError("edges_no is too big, "
                         "it must be smaller or equal to "
                         + str(x_no * y_no))

    # Create two lists to store X and Y that has no edge
    x_list_no_adj = []
    y_list_no_adj = []
    # Create two lists to store X and Y vertices
    x_list = []
    y_list = []

    graph = {}

    for i in range(x_no):
        x_list.append("x_" + str(i + 1))
        x_list_no_adj.append("x_" + str(i + 1))

    for i in range(y_no):
        y_list.append("y_" + str(i + 1))
        y_list_no_adj.append("y_" + str(i + 1))

    for i in x_list:
        graph[i] = set()

    min_x_y = min(x_no, y_no)

    # Connecting the edges between X nodes and Y nodes
    for i in range(min_x_y):
        # Randomly choose a X node
        x = random.choice(x_list_no_adj)
        x_list_no_adj.remove(x)
        # Randomly choose a Y node
        y = random.choice(y_list_no_adj)
        y_list_no_adj.remove(y)
        # Connect X node to Y node by storing
        # into a set form of bipartite graph
        graph[x].add(y)

    # If still have X vertices are not connected
    # by an edge
    if len(x_list_no_adj) != 0:
        for i in x_list_no_adj:
            # Randomly choose a Y node
            y = random.choice(y_list)
            # Connect X node to Y node by storing
            # into a set form of bipartite graph
            graph[i].add(y)

    # If still have Y vertices are not connected by
    # an edge
    if len(y_list_no_adj) != 0:
        for i in y_list_no_adj:
            # Randomly choose a X node
            x = random.choice(x_list)
            # Connect X node to Y node by storing
            # into a set form of bipartite graph
            graph[x].add(i)

    max_x_y = max(x_no, y_no)
    # If still got unconnected edges
    if edges_no > max_x_y:
        for i in range(edges_no - max_x_y):
            # Randomly choose a X node
            x = random.choice(x_list)
            # Randomly choose a Y node
            y = random.choice(y_list)
            # If the X node already connected
            # with all the Y nodes
            while len(graph[x]) == y_no:
                # Reselect the X node again
                x = random.choice(x_list)
            # If the X node already connected
            # with the Y node
            while y in graph[x]:
                # Reselect the Y node again
                y = random.choice(y_list)
            # Connect X node to Y node by storing
            # into a set form of bipartite graph
            graph[x].add(y)

    return graph


def generate_sample_graph(number, min_nodes, max_nodes):
    graphs = []
    for i in range(number):
        # Randomly select a number to be a number of X nodes
        x = random.randint(min_nodes, max_nodes)
        # Randomly select a number to be a number of Y nodes
        y = random.randint(min_nodes, max_nodes)
        # Randomly select a number of edges
        edges_no = random.randint(max(x, y), x * y)
        graph = generate_bipartite_graph(x, y, edges_no)
        graphs.append(graph)
    return graphs

def Generate_one_to_many_bipartite_graphs():

    graphs = generate_sample_graph(1, 4, 4)
    expend_graphs = []
    y_x_counts = []

    for graph in graphs:
        # Create two sets to store X and Y vertices
        x_set = set()
        y_set = set()
        # Create a turn around graph y to x graph
        y_to_x_graphn = {}
        # Add X vertices and Y vertices into two sets
        for x in graph:
            x_set.add(x)
            for y in graph[x]:
                y_set.add(y)
                if y in y_to_x_graphn:
                    y_to_x_graphn[y].add(x)
                else:
                    values = set()
                    values.add(x)
                    y_to_x_graphn[y] = values
        # Randomly generate the number of matches of y nodes
        y_x_count = {}
        for x_vertex, y_vertices in y_to_x_graphn.items():
            count = len(y_vertices) - \
                    random.randint(0, len(y_vertices)-1)
            y_x_count[x_vertex] = count

        ycopied_graph = {}
        # Copy y nodes and adjacent edges
        # according to the number
        for y, count in y_x_count.items():
            for i in range(count):
                copied_y = f"{y}-{i+1}"
                ycopied_graph[copied_y] = \
                    y_to_x_graphn[y].copy()

        # Create two sets to store X and Y vertices
        x_set = set()
        y_set = set()

        expend_graph = {}

        # Transform the graph back to x to y
        # Add X vertices and Y vertices into two sets
        for x in ycopied_graph:

            x_set.add(x)
            for y in ycopied_graph[x]:
                y_set.add(y)
                if y in expend_graph:
                    expend_graph[y].add(x)
                else:
                    values = set()
                    values.add(x)
                    expend_graph[y] = values
        expend_graphs.append(expend_graph)
        y_x_counts.append(y_x_count)

    return graphs, expend_graphs, y_x_counts


graphs, expend_graphs, y_x_counts = Generate_one_to_many_bipartite_graphs()


for index, x_to_y_graph in enumerate(expend_graphs):

    matching = HopcroftKarp(x_to_y_graph).maximum_matching()
    # print("Matching is ", matching)
    is_perfect = True
    for i in x_to_y_graph:
            for j in x_to_y_graph[i]:
                if i not in matching or j not in matching:
                    is_perfect = False
    if (is_perfect):
        e_0p, e_wp, e_1p = perfect_matching_algorithm(x_to_y_graph)
        e0, ew, e1 = judgment_bipartite_graphs(e_0p, e_wp, e_1p)

        # print("graph: ", graphs[index])
        # print("y number: ", y_x_counts[index])
        # print("expend_graph: ", x_to_y_graph)
        # print("e_0p: ",e_0p,"e_wp: ", e_wp,"e_1p: ", e_1p)
        # print("E_0: ",e0,"E_w: ", ew,"E_1: ", e1)


        res = tester2.test(graphs[index], y_x_counts[index], e0, ew, e1)
        if res:
            print(res)
            print("graph: ", graphs[index])
            print("y number: ", y_x_counts[index])
            print("expend_graph: ", x_to_y_graph)
            print("e_0p: ",e_0p,"e_wp: ", e_wp,"e_1p: ", e_1p)
            print("E_0: ",e0,"E_w: ", ew,"E_1: ", e1)
        else:
            print("error")

    else:
        e_0p, e_wp, e_1p = imperfect_matching_algorithm(x_to_y_graph)
        e0, ew, e1 = judgment_bipartite_graphs(e_0p, e_wp, e_1p)

        # print("graph: ", graphs[index])
        # print("y number: ", y_x_counts[index])
        # print("expend_graph: ", x_to_y_graph)
        # print("e_0p: ",e_0p,"e_wp: ", e_wp,"e_1p: ", e_1p)
        # print("E_0: ",e0,"E_w: ", ew,"E_1: ", e1)

        res = tester2.test(graphs[index], y_x_counts[index], e0, ew, e1)
        if res:
            print(res)
            print("graph: ", graphs[index])
            print("y number: ", y_x_counts[index])
            print("expend_graph: ", x_to_y_graph)
            print("e_0p: ",e_0p,"e_wp: ", e_wp,"e_1p: ", e_1p)
            print("E_0: ",e0,"E_w: ", ew,"E_1: ", e1)
        else:
            print("error")
    total += (time.time()-now)


print("Executed time: " + str(total))
