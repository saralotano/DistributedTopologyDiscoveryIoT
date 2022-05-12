import statistics
import networkx as nx
import re
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

    # network_nodes contains all nodes of the network
    network_nodes = list(net.nodes.keys())

    z = 0
    while z < len(network_nodes):
        node = net.nodes[z]  # node is an instance of Node class

        for i in range(number_of_nodes):
            node.networkNodes[i] = 0  # in questa struttura segnerò i msg passati attraverso l'iesimo nodo

        # CREATE THE GRAPH FOR THE LOCAL TOPOLOGY OF EACH NODE
        # graph = nx.Graph()
        # add the node itself to the local topology
        # graph.add_node(node.nodeID)

        # local topology dictionary
        node.add_node(z)  # aggiungo il nodo stesso alla topologia locale
        # from the global topology, we obtain the neighbors of that node
        neighbors = list(net.graph.adj[z])
        node.neighbors = neighbors  # aggiungo i vicini al nodo
        node.localNetwork[z] = neighbors  # aggiungo i vicini alla topologia locale

        j = 0
        # for each neighbor, add the neighbor node to the local topology and the corresponding edges
        while j < len(neighbors):
            node.add_node(neighbors[j])
            node.discoveredEdges += 1
            # node.new_add_neighbor(neighbors[j], node.nodeID)
            # node.new_add_neighbor(node.nodeID, neighbors[j])
            # edge = (node.nodeID, neighbors[j])
            '''
            if edge not in graph.edges:
                graph.add_edge(node.nodeID, neighbors[j])
                node.discoveredEdges += 1
                if node.discoveredEdges == NUMBER_OF_EDGES:
                    node.discoveredTopology = True
            if neighbors[j] not in node.localNetwork.keys():
                graph.add_node(neighbors[j])
            '''

            # NEW: aggiungo l'istanza del neighbor alla lista di vicini del nodo
            # n = Neighbor(neighbors[j])  # SARA: controllare
            # node.neighbors.append(n)  # SARA: controllare

            j = j + 1

        # node.graph = graph
        # nx.draw_networkx(node.graph)
        # plt.show()
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


def update_node_local_topology(requested_info, sim_time):
    i = 0
    while i < len(network_messages):  # per ogni messaggio ricevuto
        msg = network_messages[i]
        if int(msg.simTime) <= sim_time:
            receiver_node = network.nodes[msg.destination]  # considero il destinatario

            receiver_node.receivedMsg += 1
            receiver_node.receivedMsgIDs.append(msg)  # aggiungo il nuovo messaggio ai msgRicevuti

            z = 0
            path_len = len(msg.path)
            msg.dimension = path_len
            msg.receivedFrom = int(msg.path[path_len - 2])
            msg.source = int(msg.path[0])

            while z < path_len:  # considero tutti i nodi all'interno del path
                node = msg.path[z]

                if receiver_node.check_node_existence(node):
                    updated = 0

                    if z - 1 >= 0 and receiver_node.check_neighbor_presence(node, msg.path[z - 1]):
                        add_node_neighbor(receiver_node, msg.path[z], msg.path[z - 1], msg, network.graph.number_of_edges())
                        updated = 1  # il nodo ha aggiunto una nuova informazione alla topologia

                    if z + 1 < path_len and \
                            receiver_node.check_neighbor_presence(node, msg.path[z + 1]):

                        add_node_neighbor(receiver_node, msg.path[z], msg.path[z + 1], msg, network.graph.number_of_edges())
                        updated = 1

                    if updated == 1:
                        msg.isUpdate = 1

                else:  # il nodo non è presente nella topologia locale del receiver_node
                    receiver_node.add_node(node)
                    msg.isUpdate = 1

                    if z - 1 >= 0:
                        add_node_neighbor(receiver_node, msg.path[z], msg.path[z - 1], msg, network.graph.number_of_edges())

                    if z + 1 < path_len:
                        add_node_neighbor(receiver_node, msg.path[z], msg.path[z + 1], msg, network.graph.number_of_edges())

                if z == 0:  # vuol dire che stiamo considerando la sorgente del msg
                    msg.sourceNeighbor = len(receiver_node.localNetwork[msg.path[z]])

                if 1 < z < (path_len - 1):
                    # non ha senso mettere z=1 perchè è già un vicino
                    t = 0
                    while t < z - 1:  # metto il -1 perchè è inutile considerare il mio vicino
                        if not network.nodes[node].check_node_existence(msg.path[t]):
                            network.nodes[node].add_node(msg.path[t])
                        if t - 1 >= 0:
                            network.nodes[node].add_neighbor_localTopology(msg.path[t], msg.path[t + 1], msg, network.graph.number_of_edges())
                        if t + 1 < path_len:
                            network.nodes[node].add_neighbor_localTopology(msg.path[t], msg.path[t + 1], msg, network.graph.number_of_edges())
                        t += 1

                if (z != 0) and (z != path_len - 1):  # non considero la source e il destinatario del msg
                    network.nodes[node].relayedMsg += 1
                z = z + 1

            if msg.isResponse:

                if requested_info == 'LOCAL_TOPOLOGY':
                    source_localNetwork = network.nodes[msg.source].localNetwork

                    # aggiungo i vicini alla topologia locale
                    for key in source_localNetwork:
                        msg.dimension += 1  # 1byte per la key

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


def compute_transmitted_bytes():
    dim = 0
    for m in network_messages:
        dim += m.dimension
        # if dim >= 46680:
        #     print(m.msgID)
        #     return
    print("Total size of received messages", dim, "(bytes)")


NUMBER_OF_NODES = 100
NETWORK_TOPOLOGY = 'GRID'  # possible values: 'POWER_LAW', 'GRID'
network = create_global_topology(NETWORK_TOPOLOGY, NUMBER_OF_NODES)
network_messages = parse_received_messages()


def main():
    REQUESTED_INFO = 'NEIGHBORS'  # possible values: 'LOCAL_TOPOLOGY', 'NEIGHBORS', 'NONE'
    SIM_TIME = 172798  # serve solo per il bayesian

    update_node_local_topology(REQUESTED_INFO, SIM_TIME)
    get_nodes_statistics()
    compute_transmitted_bytes()


if __name__ == "__main__":
    main()
