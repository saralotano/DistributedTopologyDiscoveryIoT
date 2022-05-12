from math import sqrt
import networkx as nx
from matplotlib import pyplot as plt
from networkx import convert_node_labels_to_integers


def powerLawTopology(nodes):
    n = nodes
    m = 1
    p = 0.1  # if m = 1 the value of p does not matter
    s = 0

    return nx.powerlaw_cluster_graph(n, m, p, seed=s)


def gridTopology(nodes):
    m = int(sqrt(nodes))
    n = int(sqrt(nodes))

    g = nx.grid_2d_graph(m, n)
    print(convert_node_labels_to_integers(g))
    return convert_node_labels_to_integers(g)  # needed to number the nodes from 0 to nodes-1


def main(TOPOLOGY, NUMBER_OF_NODES):
    GRAPH = None
    n = []  # DEBUG

    print("TOPOLOGY CREATION")
    if TOPOLOGY == 'POWER_LAW':
        GRAPH = powerLawTopology(NUMBER_OF_NODES)
    elif TOPOLOGY == 'GRID':
        GRAPH = gridTopology(NUMBER_OF_NODES)

    if GRAPH is not None:
        print(nx.is_connected(GRAPH))
        print(len(nx.edges(GRAPH)))

        z = 0
        while z < len(GRAPH.nodes):
            print("nodeID =", z, ", neighbors =", len(GRAPH.adj[z]), ", list:", GRAPH.adj[z])
            n.append(len(GRAPH.adj[z]))  # DEBUG
            z = z + 1

        nx.draw_networkx(GRAPH)
        plt.show()

        print(n)  # DEBUG

        START_TIME = 0.0
        edges = nx.edges(GRAPH)
        with open('../data/connections.txt', 'w') as f:
            for e in edges:
                row = str(START_TIME) + ' CONN ' + str(e[0]) + ' ' + str(e[1]) + ' up'
                f.write("%s\n" % row)

        neighbors = []
        i = 0
        while i < len(GRAPH.nodes):
            neighbors.append(len(GRAPH.adj[i]))
            # print(len(g.adj[i]))
            i = i + 1

        neighbors.sort(reverse=True)
        x = [x for x in range(len(neighbors))]
        y = neighbors
        plt.stem(x, y, use_line_collection=True, label="Number of neighbors")
        plt.ylabel("Number of neighbors")
        plt.xlabel("Nodes")
        plt.legend()
        plt.show()


if __name__ == "__main__":
    TOPOLOGY = 'POWER_LAW'  # possible values: 'POWER_LAW', 'GRID'
    NUMBER_OF_NODES = 100
    main(TOPOLOGY, NUMBER_OF_NODES)
