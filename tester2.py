def test(original_dicts, y_number, e0, ew, e1):
    graphs = []
    graph = original_dicts
# Create two sets to store X and Y vertices
    x_set = set()
    y_set = set()

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

    copied_graph = {}
    ycopied_graph = {}

    for y, count in y_number.items():
        for i in range(count):
            copied_y = f"{y}-{i+1}"
            ycopied_graph[copied_y] = y_to_x_graphn[y].copy()

    # Create two sets to store X and Y vertices
    x_set = set()
    y_set = set()

    expend_graph = {}

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
    original_dict = expend_graph

    edges = []
    for x_node, y_nodes in original_dict.items():
        for y_node in y_nodes:
            edges.append((x_node, y_node))

    # print("Edges:")
    # print(edges)


    def is_valid_combination(combination):
        all_nodes = set()
        for edge in combination:
            all_nodes.update(edge)
        return len(all_nodes) == len(combination) * 2

    def find_combinations(edges, current_combination, all_combinations):
        if not edges:
            if is_valid_combination(current_combination):
                all_combinations.append(current_combination)
            return

        edge = edges.pop()
        # Include the edge and explore the next possibilities
        find_combinations(edges.copy(), current_combination + [edge], all_combinations)
        # Skip the edge and explore the next possibilities
        find_combinations(edges.copy(), current_combination, all_combinations)


    all_combinations = []
    find_combinations(list(edges), [], all_combinations)

    # Find the length of the longest combination
    max_length = max(len(comb) for comb in all_combinations)

    # Find all combinations with the longest length
    longest_combinations = [comb for comb in all_combinations if len(comb) == max_length]

    # Display all longest combinations
    # print("Longest Combinations:")
    # for combination in longest_combinations:
    #     print(combination)

    graphs = longest_combinations

    updated_graphs = [[(x, y[:-2]) for x, y in subgraph] for subgraph in graphs]
    # print(updated_graphs)
    # for combination in updated_graphs:
    #     print(combination)


    #print('ffff')
    updated_graphs = [list(item) for item in set(tuple(combination) for combination in updated_graphs)]
    # print(updated_graphs)
    # 打印更新后的图形
    # for combination in updated_graphs:
    #     print(combination)

    t = 0
    f = 0

    correct1 = True
    for item in e1:
        is_present = all(item in combination for combination in updated_graphs)
        if not is_present:
            correct1 = False
            break

    if correct1:
        print("True")
        t = t+1
    else:
        print("error")


    correct2 = True
    for item in ew:
        is_present = any(item in combination for combination in updated_graphs)
        if not is_present:
            correct2 = False
            break

    if correct2:
        print("True")
        t = t+1
    else:
        print("error")

    not_present = True

    for item in e0:
        is_present = any(item in combination for combination in updated_graphs)
        if is_present:
            not_present = False
            break

    if not_present:
        print("True")
        t = t+1
    else:
        print("error")

    edgess = []
    for x_nodes, y_nodess in original_dicts.items():
        for y_nodes in y_nodess:
            edgess.append((x_nodes, y_nodes))

    # print("Edges:")
    # print(edgess)
    edgess = set(edgess)
    set1 = set(e1 | ew | e0)
    set2 = set(e1 & ew & e0)
    # print(set1)
    # print(len(set2))
    if edgess == set1 and len(set2) == 0:
        print("True")
        t = t+1
    else:
        print("error")

    if t == 4:
        return True
    else:
        return False




# original_dicts = {'x_1': {'y_1'}, 'x_2': {'y_1', 'y_2'}, 'x_3': {'y_2', 'y_3'}, 'x_4': {'y_3'}, 'x_5': {'y_3'}, 'x_6': {'y_3'}}
# y_number = {'y_2': 2, 'y_1': 1, 'y_3': 2}
# E_0 ={('x_2', 'y_1'), ('x_3', 'y_3')}
# E_w ={('x_4', 'y_3'), ('x_5', 'y_3') , ('x_6', 'y_3')}
# E_1 ={('x_1', 'y_1'), ('x_2', 'y_2'), ('x_3', 'y_2')}
#
# print(test(original_dicts,y_number,E_0,E_w,E_1))
