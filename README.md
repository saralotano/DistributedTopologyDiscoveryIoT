# DistributedTopologyDiscoveryIoT

Folders:

- data folder contains the following files:
	- connections.txt is the file that is used in TheONE simulator to create connections between nodes. This file is generated as output from the file topologyDiscovery/topologyCreation.py

	- dataframe.txt contains the information to create the DAG in the Bayesian inference method. It is created in the select_bayesian_inference_nodes function in the file topologyDiscovery/advancedFlooding.py

	- deliveredMessages.txt contains the data obtained from the Test-100-nodes_DeliveredMessagesReport.txt report of the TheONE simulator

	- floodingMessages.txt contains the message creation events that will be used in the TheONE simulator. This file is generated as output of topologyDiscovery/messageCreation.py

	- hopCountSources.csv contains the source,destination pairs of nodes identified by the HopCount method. This file is generated by the select_hop_count_nodes function contained in topologyDiscovery/advancedFlooding.py and is used as input to the topologyDiscovery/messageCreation.py file

	- inferenceSources.csv contains the source,destination pairs of nodes identified by the Bayesian Inference method. This file is generated by the select_bayesian_inference_nodes function contained in topologyDiscovery/advancedFlooding.py and is used as input to the topologyDiscovery/messageCreation.py file

	- relayedMsgSources.csv contains the source,destination pairs of nodes identified by the Relayed Messages method. This file is generated by the select_relayed_msg_nodes function contained in topologyDiscovery/advancedFlooding.py and is used as input to the topologyDiscovery/messageCreation.py file


- plot folder contains all the scripts used to create the plots


- topologyDiscovery folder contains the files for the three classes:
	- Message.py
	- Network.py
	- Node.py

  Other files:
  - advancedFlooding.py contains the main and instances of all classes
  
  - advancedFloodingPerformanceEval.py contains a small code variation in the update_node_local_topology function used to compute the evolution of the number of discovered edges versus simulation time.
  
  - advancedFloodingRelayedMsg.py contains only the code related to the RelayedMessages method. It was created only for convenience. It contains no changes with respect to the advancedFlooding.py file.
  
  - centralityIndixes.py contains code for creating graphs related to studying the centrality of nodes within the network.
  
  - messageCreation.py contains the code used for message creation. The input can be random or it can be one of the csv files contained in the data folder.
  
  - nodeCentrality.py contains the code to compute the ten nodes traversed by the largest number of messages within the network
  
  - randomFlooding.py contains code for parsing messages when they have been randomly generated
  
  - topologyCreation.py contains the code for creating the network topology. The output is the file contained in data/connections.txt that will be used in the TheONE simulator to create the connections between nodes.
