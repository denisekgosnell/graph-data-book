# -*- coding: utf-8 -*-
#
# Please see the License.txt file for more information.
# All other rights reserved.
#

from __future__ import absolute_import

from dse.cluster import Cluster, GraphExecutionProfile, EXEC_PROFILE_GRAPH_DEFAULT
from dse.graph import GraphOptions, GraphProtocol
from dse_graph import DseGraph
import logging

class DSEGraphConnection(object):
    """
        DataStax Graph Connection
        This class provides a wrapper around connecting to DSE Graph
        to handle common operations
    """

    def __init__(self, graph_name="trees"):
        """

        :param graph_name: name of the graph
        :param ep: Execution profile
        :param cluster:
        """
        self.graph_name = graph_name
        self.ep = GraphExecutionProfile(graph_options=GraphOptions(graph_name=graph_name,
                                                                   graph_protocol=GraphProtocol.GRAPHSON_3_0))
        self.cluster = Cluster(execution_profiles={EXEC_PROFILE_GRAPH_DEFAULT: self.ep})
        self.session = self.cluster.connect()
        self.g = DseGraph.traversal_source(session=self.session)
        # logging information
        self.logfile = "connection.log"
        logging.basicConfig(filename=self.logfile,
                            filemode='w',
                            level=logging.DEBUG,
                            format='%(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger("GraphConnectionLogger")


    def close_session(self):
        """
        Close connection to DSE
        """
        self.session.shutdown()