import csv
import operator
import statistics
from random import randint

import networkx as nx
import re

import pandas as pd
import bnlearn as bn
from networkx import convert_node_labels_to_integers

from Message import Message
from Network import Network


def create_global_topology(network_topology, number_of_nodes):
    # create global network instance
    net = Network()
    # add nodes
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
        while j < len(neighbors):
            node.add_node(neighbors[j])
            node.discoveredEdges += 1
            j = j + 1
        z = z + 1

    return net


def parse_received_messages():
    f = open("../data/deliveredMessages.txt", "r")
    rows = f.readlines()
    length = len(rows)
    received_messages = []

    for x in range(1, length):
        message_info = rows[x].split()
        # print(message_info)

        sim_time_str = re.findall(r'\d+', message_info[0])[0]
        sim_time = int(sim_time_str)
        # print(sim_time)

        msg_id = message_info[1]
        # print(msg_id)

        size = message_info[2]
        # print(size)

        hop_count = int(message_info[3])
        # print(hop_count)

        d_time_str = re.findall(r'\d+', message_info[4])[0]
        d_time = int(d_time_str)
        # print(d_time)

        source = int(re.findall(r'\d+', message_info[5])[0])
        # print(source)

        destination = int(re.findall(r'\d+', message_info[6])[0])
        # print(destination)

        if message_info[8] == 'N':
            is_resp = False
        else:
            is_resp = True
        # print(is_resp)

        path = re.findall(r'\d+', message_info[9])
        path_int = [int(i) for i in path]
        # print(path_int)

        message = Message(sim_time, msg_id, size, hop_count, d_time, source, destination, is_resp, path_int)
        received_messages.append(message)

    return received_messages


def add_node_neighbor(receiver, node, neighbor, msg, edges):
    receiver.add_neighbor_localTopology(node, neighbor, msg, edges)
    if receiver.discoveredEdges == edges:
        receiver.discoveredTopology = True


def update_node_local_topology(advanced_mode, requested_info):

    time = 0
    counter = 0
    time_edge = {}

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

        # VARIAZIONE DEL CODICE
        if time + (60 * counter) <= msg.simTime <= time + (60 * (counter + 1)):
            NODE_ID = 0
            discEdges = []
            while NODE_ID < network.graph.number_of_nodes():
                discEdges.append(network.nodes[NODE_ID].discoveredEdges)
                NODE_ID += 1

            val = time + (60 * counter)
            if val not in time_edge:
                time_edge[val] = statistics.mean(discEdges)

            counter += 1

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

    print(edges)
    print("Average number of edges discovered by each node: ", statistics.mean(edges))
    print("Average number of received messages by each node: ", statistics.mean(received_messages))
    print("Average number of update messages for each node: ", statistics.mean(update_messages))

    print("Max discovered time: ", max(discovered_times))


def sorting_criteria(e):
    return e['probability']


def select_high_probability_nodes(query, number_of_sources):
    source_IDs = list(query.state_names.get('src'))
    source_values = list(query.values)
    source_probabilities = []

    for x in range(len(source_values)):
        dict_sp = {'src': source_IDs[x], 'probability': source_values[x]}
        source_probabilities.append(dict_sp)
    source_probabilities.sort(reverse=True, key=sorting_criteria)

    values = []
    for i in range(number_of_sources):
        values.append(source_probabilities[i].get('src'))
    return values


def choose_random_nodes(node_id, number_of_sources):
    values = []
    while len(values) < number_of_sources:
        val = randint(0, network.graph.number_of_nodes() - 1)
        if val != node_id and (val not in values):
            values.append(val)
    return values


def select_bayesian_inference_nodes(sim_time, number_of_sources):

    inference_results = {}
    NODE_ID = 0
    incomplete_nodes = []

    while NODE_ID < network.graph.number_of_nodes():
        if not network.nodes[NODE_ID].discoveredTopology:
            incomplete_nodes.append(NODE_ID)
            node_msgs = network.nodes[NODE_ID].receivedMsgIDs
            LEVELS = [0, 1, 2, 3]  # -> ['LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH']
            sim_unit = int(sim_time / len(LEVELS))

            dt_values = []
            for m in node_msgs:
                dt_values.append(int(m.deliveryTime))
            dt_unit = int(max(dt_values) / len(LEVELS))

            # DATAFRAME COLUMN HEADER
            # src | simTime | srcNeighbor | delTime | hopCount | updateMsg | dir
            column_names = []
            data = {}

            s = 'src'
            st = 'simTime'
            sn = 'srcNeighbor'
            dt = 'delTime'
            hc = 'hopCount'
            u = 'update'
            d = 'dir'
            column_names.extend((s, st, sn, dt, hc, u, d))

            i = 0
            while i < len(node_msgs):
                # source
                row_info = [node_msgs[i].source]

                # simTime
                simTime_value = node_msgs[i].simTime
                st_value = 0
                if sim_unit <= simTime_value <= sim_unit * 2:
                    st_value = 1
                elif sim_unit * 2 <= simTime_value <= sim_unit * 3:
                    st_value = 2
                elif simTime_value > sim_unit * 3:
                    st_value = 3
                row_info.append(st_value)

                # sourceNeighbor
                row_info.append(node_msgs[i].sourceNeighbor)

                # deliveryTime
                msg_deliveryTime = node_msgs[i].deliveryTime
                dt_value = 0
                if dt_unit <= msg_deliveryTime <= dt_unit * 2:
                    dt_value = 1
                elif dt_unit * 2 <= msg_deliveryTime <= dt_unit * 3:
                    dt_value = 2
                elif msg_deliveryTime > dt_unit * 3:
                    dt_value = 3
                row_info.append(dt_value)

                # hopCount
                row_info.append(node_msgs[i].hopCount)

                # isUpdate
                row_info.append(node_msgs[i].isUpdate)

                # direction
                row_info.append(node_msgs[i].receivedFrom)

                data['M' + str(i)] = row_info

                i += 1

            # DATAFRAME CREATION
            dataframe = pd.DataFrame.from_dict(data, orient='index', columns=column_names)
            with open('../data/dataframe.txt', 'w') as f:
                dfAsString = dataframe.to_string()
                f.write(dfAsString)

            # STRUCTURED LEARNING
            DAG = bn.structure_learning.fit(dataframe, methodtype='hc', scoretype='k2', verbose=0)

            # PARAMETER LEARNING
            model = bn.parameter_learning.fit(DAG, dataframe, methodtype='ml', verbose=0)

            # INFERENCE
            query = bn.inference.fit(model, variables=['src'], evidence={'update': 0}, verbose=0)
            inference_results[NODE_ID] = select_high_probability_nodes(query, number_of_sources)

        NODE_ID += 1

    a_file = open("../data/inferenceSources.csv", "w", newline="")
    writer = csv.writer(a_file)
    for i in range(number_of_sources):
        for j in range(len(incomplete_nodes)):
            writer.writerow([incomplete_nodes[j], inference_results.get(incomplete_nodes[j])[i]])
    a_file.close()


def select_hop_count_nodes():
    NODE_ID = 0
    results = {}
    max_length = 0
    incomplete_nodes = []

    while NODE_ID < network.graph.number_of_nodes():
        if not network.nodes[NODE_ID].discoveredTopology:
            incomplete_nodes.append(NODE_ID)
            network.nodes[NODE_ID].nodesDistance = nx.single_source_shortest_path_length(network.graph, NODE_ID)
            sorted_d = dict(sorted(network.nodes[NODE_ID].nodesDistance.items(),
                                   key=operator.itemgetter(1), reverse=True))
            sorted_list = list(sorted_d.keys())

            nodes = []
            i = 0
            while i < len(sorted_list):
                if sorted_list[i] != NODE_ID and \
                        sorted_list[i] in list(network.nodes[NODE_ID].localNetwork.keys()) and  \
                        (sorted_list[i] not in network.nodes[NODE_ID].neighbors):
                    nodes.append(sorted_list[i])
                i += 1

            if len(nodes) > max_length:
                max_length = len(nodes)
            results[NODE_ID] = nodes

        NODE_ID += 1

    a_file = open("../data/hopCountSources.csv", "w", newline="")
    writer = csv.writer(a_file)

    for i in range(max_length):
        for j in range(len(incomplete_nodes)):
            if len(results.get(incomplete_nodes[j])) > i:
                writer.writerow([incomplete_nodes[j], results.get(incomplete_nodes[j])[i]])
    a_file.close()


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
    SIM_TIME = 10800
    NUMBER_OF_SOURCES = 20

    update_node_local_topology(ADVANCED_FLOODING, REQUESTED_INFO)

    if ADVANCED_FLOODING:
        if NODE_SELECTION_METHOD == 'HOP_COUNT':
            select_hop_count_nodes()
        elif NODE_SELECTION_METHOD == 'RELAYED_MSG':
            select_relayed_msg_nodes(NUMBER_OF_SOURCES)
        elif NODE_SELECTION_METHOD == 'BAYESIAN':
            select_bayesian_inference_nodes(SIM_TIME, NUMBER_OF_SOURCES)

    get_nodes_statistics()
    compute_transmitted_bytes(NODE_SELECTION_METHOD)


if __name__ == "__main__":
    main()
