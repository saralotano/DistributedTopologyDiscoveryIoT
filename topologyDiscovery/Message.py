class Message:
    
    def __init__(self, sim_time, msg_id, size, hop_count, d_time, source, destination, is_resp, path):
        self.msgID = msg_id
        self.simTime = sim_time
        self.size = size
        self.hopCount = hop_count
        self.deliveryTime = d_time
        self.source = source
        self.destination = destination
        self.isResponse = is_resp  # True or False
        self.path = path  # list of nodeID
        self.isUpdate = 0
        self.receivedFrom = None
        self.sourceNeighbor = 0  # number of neighbors of the message source
        self.dimension = 0
