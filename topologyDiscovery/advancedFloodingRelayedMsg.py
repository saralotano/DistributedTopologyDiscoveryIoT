import csv
import operator
import statistics
from random import randint

import networkx as nx
import re

from networkx import convert_node_labels_to_integers

from Message import Message
from Network import Network


def create_global_topology(network_topology, number_of_nodes):
    net = Network()
    net.add_nodes(number_of_nodes)

    # GLOBAL TOPOLOGY GRAPH CREATION
    if network_topology == 'POWER_LAW':
        m = 1
        p = 0.1
        s = 0
        net.graph = nx.powerlaw_cluster_graph(number_of_nodes, m, p, seed=s)
    elif network_topology == 'GRID':
        g = nx.grid_2d_graph(10, 10)
        print(convert_node_labels_to_integers(g))
        g = convert_node_labels_to_integers(g)
        net.graph = g

    network_nodes = list(net.nodes.keys())

    z = 0
    while z < len(network_nodes):
        node = net.nodes[z]

        for i in range(number_of_nodes):
            node.networkNodes[i] = 0
        node.add_node(z)
        neighbors = list(net.graph.adj[z])
        node.neighbors = neighbors
        node.localNetwork[z] = neighbors

        j = 0
        # for each neighbor, add the neighbor node to the local topology and the corresponding edges
        while j < len(neighbors):
            node.add_node(neighbors[j])
            node.discoveredEdges += 1

            j = j + 1
        z = z + 1

    return net


def parse_received_messages():
    f = open("../data/deliveredMessages.txt", "r")
    # row format:
    # time      ID      size    hopcount    deliveryTime  fromHost  toHost  remainingTtl  isResponse  path
    rows = f.readlines()
    length = len(rows)
    received_messages = []

    for x in range(1, length):
        message_info = rows[x].split()

        sim_time_str = re.findall(r'\d+', message_info[0])[0]
        sim_time = int(sim_time_str)

        msg_id = message_info[1]

        size = message_info[2]

        hop_count = int(message_info[3])

        d_time_str = re.findall(r'\d+', message_info[4])[0]
        d_time = int(d_time_str)

        source = int(re.findall(r'\d+', message_info[5])[0])

        destination = int(re.findall(r'\d+', message_info[6])[0])

        if message_info[8] == 'N':
            is_resp = False
        else:
            is_resp = True

        path = re.findall(r'\d+', message_info[9])
        path_int = [int(i) for i in path]

        message = Message(sim_time, msg_id, size, hop_count, d_time, source, destination, is_resp, path_int)
        received_messages.append(message)

    return received_messages


def add_node_neighbor(receiver, node, neighbor, msg, edges):
    receiver.add_neighbor_localTopology(node, neighbor, msg, edges)
    if receiver.discoveredEdges == edges:
        receiver.discoveredTopology = True


def update_node_local_topology(advanced_mode, requested_info):
    i = 0
    while i < len(network_messages):
        msg = network_messages[i]
        receiver_node = network.nodes[msg.destination]

        receiver_node.receivedMsg += 1
        receiver_node.receivedMsgIDs.append(msg)

        z = 0
        path_len = len(msg.path)
        msg.dimension = path_len
        msg.receivedFrom = int(msg.path[path_len - 2])
        msg.source = int(msg.path[0])

        while z < path_len:
            node = msg.path[z]

            if receiver_node.check_node_existence(node):
                updated = 0

                if z - 1 >= 0 and receiver_node.check_neighbor_presence(node, msg.path[z - 1]):
                    add_node_neighbor(receiver_node, msg.path[z], msg.path[z - 1], msg, network.graph.number_of_edges())
                    updated = 1

                if z + 1 < path_len and \
                        receiver_node.check_neighbor_presence(node, msg.path[z + 1]):
                    add_node_neighbor(receiver_node, msg.path[z], msg.path[z + 1], msg, network.graph.number_of_edges())
                    updated = 1

                if updated == 1:
                    msg.isUpdate = 1

            else:
                receiver_node.add_node(node)
                msg.isUpdate = 1

                if z - 1 >= 0:
                    add_node_neighbor(receiver_node, msg.path[z], msg.path[z - 1], msg, network.graph.number_of_edges())

                if z + 1 < path_len:
                    add_node_neighbor(receiver_node, msg.path[z], msg.path[z + 1], msg, network.graph.number_of_edges())

            if z == 0:
                msg.sourceNeighbor = len(receiver_node.localNetwork[msg.path[z]])

            if 1 < z < (path_len - 1):
                t = 0
                while t < z - 1:
                    if not network.nodes[node].check_node_existence(msg.path[t]):
                        network.nodes[node].add_node(msg.path[t])
                    if t - 1 >= 0:
                        network.nodes[node].add_neighbor_localTopology(
                            msg.path[t], msg.path[t + 1], msg, network.graph.number_of_edges())
                    if t + 1 < path_len:
                        network.nodes[node].add_neighbor_localTopology(
                            msg.path[t], msg.path[t + 1], msg, network.graph.number_of_edges())

                    t += 1

            if (z != 0) and (z != path_len - 1):
                network.nodes[node].relayedMsg += 1
            z = z + 1

        if advanced_mode and msg.isResponse:

            if requested_info == 'LOCAL_TOPOLOGY':
                source_localNetwork = network.nodes[msg.source].localNetwork

                for key in source_localNetwork:
                    msg.dimension += 1

                    if not receiver_node.check_node_existence(key):
                        receiver_node.add_node(key)

                    value = source_localNetwork[key]
                    msg.dimension += len(value)

                    for v in value:
                        receiver_node.add_neighbor_localTopology(key, v, msg, network.graph.number_of_edges())

            elif requested_info == 'NEIGHBORS':
                source_neighbors = network.nodes[msg.source].neighbors
                msg.dimension += len(source_neighbors)

                for n in source_neighbors:
                    receiver_node.add_neighbor_localTopology(msg.source, n, msg, network.graph.number_of_edges())

        if msg.isUpdate == 1:
            if not receiver_node.discoveredTopology:
                receiver_node.updateMsg += 1

        i = i + 1


def get_nodes_statistics():
    print("\nNODES DATA")
    network_nodes = network.nodes.keys()
    edges = []
    received_messages = []
    update_messages = []
    discovered_times = []

    z = 0
    while z < len(network_nodes):
        node = network.nodes[z]
        edges.append(node.discoveredEdges)
        received_messages.append(node.receivedMsg)
        update_messages.append(node.updateMsg)
        discovered_times.append(node.discoveredTime)
        print('NodeID =', node.nodeID, ', neighbors =', len(network.graph.adj[z]),
              ' discoveredEdges =', node.discoveredEdges,
              ' discoveredTopology =', node.discoveredTopology,
              ' discoveredTime = ', node.discoveredTime,
              ', rcvMsg =', node.receivedMsg, ', updMsg =', node.updateMsg)

        z = z + 1

    print("Average number of edges discovered by each node: ", statistics.mean(edges))
    print("Average number of received messages by each node: ", statistics.mean(received_messages))
    print("Average number of update messages for each node: ", statistics.mean(update_messages))

    print("Max discovered time: ", max(discovered_times))


def choose_random_nodes(node_id, number_of_sources):
    values = []
    while len(values) < number_of_sources:
        val = randint(0, network.graph.number_of_nodes() - 1)
        if val != node_id and (val not in values):
            values.append(val)
    return values


def compute_transmitted_bytes(method):
    dim = 0
    for m in network_messages:
        if method == 'RELAYED_MSG' and m.isResponse:
            m.dimension += 1
        dim += m.dimension
    print("Total size of received messages", dim, "(bytes)")


def select_relayed_msg_nodes(number_of_sources):
    NODE_ID = 0
    results = {}
    incomplete_nodes = []

    while NODE_ID < network.graph.number_of_nodes():

        if not network.nodes[NODE_ID].discoveredTopology:
            incomplete_nodes.append(NODE_ID)

            for n in list(network.nodes[NODE_ID].localNetwork.keys()):
                if n != NODE_ID:
                    network.nodes[NODE_ID].networkNodes[n] = network.nodes[n].relayedMsg

            sorted_d = dict(sorted(network.nodes[NODE_ID].networkNodes.items(),
                                   key=operator.itemgetter(1), reverse=True))
            sorted_list = list(sorted_d.keys())

            nodes = []
            i = 0
            j = 0
            while i < len(sorted_list) and j < number_of_sources:
                if sorted_list[i] != NODE_ID:
                    if sorted_list[i] not in network.nodes[NODE_ID].neighbors:
                        nodes.append(sorted_list[i])
                        j += 1
                i += 1
            results[NODE_ID] = nodes

        NODE_ID += 1

    a_file = open("../data/relayedMsgSources.csv", "w", newline="")
    writer = csv.writer(a_file)
    for i in range(number_of_sources):
        for j in range(len(incomplete_nodes)):
            writer.writerow([incomplete_nodes[j], results.get(incomplete_nodes[j])[i]])
    a_file.close()


NUMBER_OF_NODES = 100
NETWORK_TOPOLOGY = 'POWER_LAW'  # possible values: 'POWER_LAW', 'GRID'
network = create_global_topology(NETWORK_TOPOLOGY, NUMBER_OF_NODES)
network_messages = parse_received_messages()


def main():
    ADVANCED_FLOODING = True
    NODE_SELECTION_METHOD = 'RELAYED_MSG'  # possible values: 'HOP_COUNT', 'RELAYED_MSG', 'BAYESIAN'
    REQUESTED_INFO = 'LOCAL_TOPOLOGY'  # possible values: 'LOCAL_TOPOLOGY', 'NEIGHBORS', 'NONE'
    NUMBER_OF_SOURCES = 20

    update_node_local_topology(ADVANCED_FLOODING, REQUESTED_INFO)

    if ADVANCED_FLOODING:
        select_relayed_msg_nodes(NUMBER_OF_SOURCES)

    get_nodes_statistics()
    compute_transmitted_bytes(NODE_SELECTION_METHOD)


if __name__ == "__main__":
    main()
