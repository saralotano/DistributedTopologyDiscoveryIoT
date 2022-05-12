class Node:
    def __init__(self, node_id):
        self.nodeID = node_id
        self.localNetwork = {}  # key=nodeID, value=node neighbors
        self.receivedMsg = 0
        self.updateMsg = 0
        self.receivedMsgIDs = []  # value of type Message
        self.discoveredEdges = 0
        self.discoveredTime = 0
        self.discoveredTopology = False
        self.neighbors = []  # neighbors nodeID
        self.networkNodes = {}  # key=nodeID, value=number of relayed messages
        self.nodesDistance = {}  # key=nodeID, value=hopCount
        self.relayedMsg = 0

    def check_node_existence(self, node):
        if node in self.localNetwork:
            return True
        else:
            return False

    def check_neighbor_presence(self, node, neighbor):
        return neighbor not in self.localNetwork[node]

    def add_node(self, node_id):
        self.localNetwork[node_id] = []

    def add_neighbor_localTopology(self, node, new_node, msg, edges):
        neighbor_list = self.localNetwork[node]
        if new_node not in neighbor_list:
            self.localNetwork[node].append(new_node)
            if new_node not in self.localNetwork:
                self.discoveredEdges += 1
                self.discoveredTime = msg.simTime
                msg.isUpdate = 1
            else:
                if node not in self.localNetwork[new_node]:
                    self.discoveredEdges += 1
                    self.discoveredTime = msg.simTime
                    msg.isUpdate = 1
        if self.discoveredEdges == edges:
            self.discoveredTopology = True
