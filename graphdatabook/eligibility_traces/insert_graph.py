from __future__ import absolute_import

from dse.util import Point
from create_data import create_tree_data
from dse_connect import DSEGraphConnection

def insert_sensor_vertices(tree, g):
    """

    :param tree:
    :param g:
    :return:
    """
    for i, (key, value) in enumerate(tree.sensors.items()):
        g.addV('Sensor').\
          property('sensorName', key). \
          property("longitude", value[0]). \
          property("latitude", value[1]). \
          property("coordinates", Point(value[0], value[1])). \
          next()

def insert_tower_vertices(tree, g):
    """

    :param tree:
    :param g:
    :return:
    """
    for i, (key, value) in enumerate(tree.towers.items()):
        g.addV('Tower').\
          property('towerName', key). \
          property("longitude", value[0]). \
          property("latitude", value[1]). \
          property("coordinates", Point(value[0], value[1])). \
          next()


def insert_edges(edge_list, g, tower_names):
    """
    Insert all edges in edge_list as Sensor -- time t --> (Sensor, Tower) edges
    :param edge_list: [from_vertex, time, to_vertex]
    :param g: connection to dse graph
    :param tower_names: list of tower names
    """
    for [from_vertex, time, to_vertex] in edge_list:
        # fastest data insertion in C*: upserts
        # that is why we addV new vertices everytime
        if to_vertex in tower_names:
            g.addE("Send"). \
                from_(g.addV("Sensor").property("sensorName", from_vertex)). \
                to(g.addV("Tower").property("towerName", to_vertex)). \
                property("timeStep", time). \
                iterate()
        else:
            g.addE("Send"). \
              from_(g.addV("Sensor").property("sensorName", from_vertex)). \
              to(g.addV("Sensor").property("sensorName", to_vertex)). \
              property("timeStep", time). \
              iterate()


def insert_tower_edges(edge_list, g):
    """
    Insert all edges in edge_list as sensor -- time t --> sensor edges
    :param edge_list: [from_vertex, time, to_vertex]
    :param g: connection to dse graph
    """
    from_vertex = edge_list[0]
    time = edge_list[1]
    to_vertex = edge_list[2]
    # fastest data insertion in C*: upserts
    # that is why we addV new vertices everytime
    g.addE("Send"). \
      from_(g.addV("Sensor").property("sensorName", from_vertex)). \
      to(g.addV("Tower").property("towerName", to_vertex)). \
      property("timeStep", time). \
      iterate()


def make_edge_list(starting_sensor, path):
    """
    create an edge list that represents the tree from starting_sensor to a tower
    :param starting_sensor: the starting sensor
    :param path: JSON object of the form {0:next0, 1:next1, 2:next2}}
    :return: edge_list
    """
    edge_list = [] # start, time, next edges
    current_sensor = starting_sensor
    for time, next_sensor in path.items():
        edge = [current_sensor, time, next_sensor]
        edge_list.append(edge)
        current_sensor = next_sensor
    return edge_list


def insert_tree(tree, graph_connection):
    """
    Iterate through the tree and insert vertices and edges
    """
    insert_sensor_vertices(tree, graph_connection.g)
    insert_tower_vertices(tree, graph_connection.g)
    for i, (starting_sensor, path) in enumerate(tree.sensor_tree.items()):
        graph_connection.logger.info("Inserting Sensor path {} for {}".format(str(i), str(starting_sensor)))
        edge_list = make_edge_list(starting_sensor, path)
        insert_edges(edge_list, graph_connection.g, tree.tower_names)

def insert_tree_data():
    """

    :return:
    """
    Tree = create_tree_data()
    GraphConnection = DSEGraphConnection()
    GraphConnection.logger.info("Inserting Tree Data")
    insert_tree(Tree, GraphConnection)
    GraphConnection.logger.info("Completed Inserting Tree Data")
    GraphConnection.close_session()


if __name__ == "__main__":
    """
    call the driving method
    """
    insert_tree_data()


