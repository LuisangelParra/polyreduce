def pretty_print_graph(nodes, edges):
    print("Nodes:", nodes)
    print("Edges:")
    for u, v in edges:
        print(f"  {u} -- {v}")
