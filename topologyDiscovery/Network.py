from Node import Node


class Network:
    def __init__(self):
        self.graph = None
        self.nodes = {}  # key:nodeID, value:Node
        
    def add_nodes(self, number_of_nodes):
        node_list = list(range(0, number_of_nodes))
        i = 0
        while i < len(node_list):
            self.nodes[i] = Node(i)
            i = i + 1
