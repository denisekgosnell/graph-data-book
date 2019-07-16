from __future__ import absolute_import

from dse.util import Point
from dse_graph import DseGraph

from connection import session
from external_data import TOWERS, SENSORS


def insert_vertices(g):
    """
    For the collected geo-locations for Towers and Sensors,
    use the connection to datastax graph and insert the vertices
    :param g: a traversal source to datastax graph
    :return: nothing
    """
    try:
        for i, (key, value) in enumerate(TOWERS.items()):
            g.addV('Tower').\
              property('towerId', i).\
              property('towerName', key). \
              property("longitude", value[0]). \
              property("latitude", value[1]). \
              property("coordinates", Point(value[0], value[1])). \
              next()

        for i, (key, value) in enumerate(SENSORS.items()):
            g.addV('Sensor').\
              property('sensorId', i).\
              property('sensorName', key). \
              property("longitude", value[0]). \
              property("latitude", value[1]). \
              property("coordinates", Point(value[0], value[1])). \
              next()
    except Exception as e:
        raise e
    finally:
        session.shutdown()


def insert_edges(g):
    """

    :param g:
    :return:
    """

    print("nothing here yet")


def create_data():
    """
    1. create a traversal source,
    2. insert vertices, and
    3. insert edges
    """
    # 1. create a traversal source,
    g = DseGraph.traversal_source(session=session)
    # 2. insert vertices
    insert_vertices(g)
    # 3. insert edges
    insert_edges(g)


if __name__ == "__main__":
    """
    call the driving method
    """
    create_data()


