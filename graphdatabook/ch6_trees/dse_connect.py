# -*- coding: utf-8 -*-
#
# Please see the License.txt file for more information.
# All other rights reserved.
#

from __future__ import absolute_import

from dse.cluster import Cluster, GraphExecutionProfile, EXEC_PROFILE_GRAPH_DEFAULT
from dse.graph import GraphOptions

class DSEConnect(object):
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
        self.ep = GraphExecutionProfile(graph_options=GraphOptions(graph_name=self.graph_name))


    def dse_session(self):
        """

        :param cluster:
        :param self:
        :return:
        """

        self.cluster = Cluster(execution_profiles={EXEC_PROFILE_GRAPH_DEFAULT: self.ep})
        self.session = self.cluster.connect()