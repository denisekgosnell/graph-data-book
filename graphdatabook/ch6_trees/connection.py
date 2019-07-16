from dse.cluster import Cluster, GraphExecutionProfile, EXEC_PROFILE_GRAPH_DEFAULT
from dse.graph import GraphOptions, GraphProtocol

graph_name = 'trees'
ep = GraphExecutionProfile(graph_options=GraphOptions(graph_name=graph_name,
                                                  graph_protocol=GraphProtocol.GRAPHSON_3_0))

cluster = Cluster(execution_profiles={EXEC_PROFILE_GRAPH_DEFAULT: ep})
session = cluster.connect()
