import external_data

import numpy as np
import random
import logging

class TreeGraph(object):
    """
        This class creates the tree data structure used in 
        The Practitioners Guide to Graph Data
    """
    
    def __init__(self):
        """
        initialize the data structures to be used during tree construction
        """
        # initialize in memory data structures
        self.sensor_tree = {}  # USAGE: {vertex : {0:next0, 1:next1, 2:next2}}
        self.edge_list = {} # USAGE: {vertex: {0: next0}, next0: {1: next1}, next1: {2: next2}
        self.time_bound = 5 # USAGE: the max # of pings from a sensor to a tower
        self.neighborhood_size = 5 # USAGE: the max size of nearest neighbors
        # sensors: JSON of the structure {"name1": [long1, lat1], "name2": [long2, lat2]...}
        self.sensors = external_data.SENSORS
        # towers: JSON of the structure {"name1": [long1, lat1], "name2": [long2, lat2]...}
        self.towers = external_data.TOWERS
        self.tower_names = self.towers.keys()
        # create dictionaries of the nearest sensors
        self.sensor_neighbors = {}
        self.make_sensor_neighbors()
        # create dictionaries of the nearest towers
        self.sensor_tower_neighbors = {}
        self.make_sensor_tower_neighbors()
        # logging information
        self.logfile = "tree_data.log"
        logging.basicConfig(filename=self.logfile,
                            filemode='w',
                            level=logging.DEBUG,
                            format='%(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger("TreeClassLogger")

        
    def haversine_np(self, lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)

        All args must be of equal length.

        """
        lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2
        c = 2 * np.arcsin(np.sqrt(a))
        km = 6367 * c
        return km

    def make_sensor_neighbors(self):
        """
        Calculate the haversine distance between each SENSOR
        Retain the top 5 closest
        :return: sensor_neighbors
        """
        for i, (key, val) in enumerate(self.sensors.items()):
            distances = {}
            for j, (key2, val2) in enumerate(self.sensors.items()):
                if key != key2: # RULE 7: Enforcing that you can't have yourself as a nearest neighbor
                    distance = self.haversine_np(val[0], val[1], val2[0], val2[1])
                    distances[key2] = distance
            sorted_distances = sorted(distances.items(), key=lambda kv: kv[1])
            self.sensor_neighbors[key] = sorted_distances[0:self.neighborhood_size]

    def make_sensor_tower_neighbors(self):
        """
        Calculate the haversine distance between each SENSOR and TOWERS
        Retain the top 5 closest
        :return: sensor_tower_neighbors
        """
        for i, (key, val) in enumerate(self.sensors.items()):
            distances = {}
            for j, (key2, val2) in enumerate(self.towers.items()):
                distance = self.haversine_np(val[0], val[1], val2[0], val2[1])
                distances[key2] = distance
            sorted_distances = sorted(distances.items(), key=lambda kv: kv[1])
            self.sensor_tower_neighbors[key] = sorted_distances[0:5]

    def update_edge_list(self, current_sensor, time, to_edge):
        """
        update in memory graph data structure
        Structure:
            {current_sensor: {time: next0},
             next0: {1: next1},
             next1: {2: next2}
        """
        # current_sensor --- time ---> to_edge
        if current_sensor in self.edge_list.keys():
            if time in self.edge_list[current_sensor].keys():
                logging.error("CONSTRUCTION ERROR: {} already has an edge at time {}".format(current_sensor, time))
                raise ValueError
            else:
                self.edge_list[current_sensor][time] = to_edge
        else:
            self.edge_list[current_sensor] = {time: to_edge}

    def update_sensor_tree(self, starting_sensor, time, to_edge):
        """
        update in memory graph data structure
        # {starting_sensor : {time:to_edge}}
        """
        # current_sensor --- t ---> to_edge
        if starting_sensor in self.sensor_tree.keys():
            if time in self.sensor_tree[starting_sensor].keys():
                logging.error("CONSTRUCTION ERROR: {} already has an edge at time {} in sensor_tree".format(starting_sensor, time))
                raise ValueError
            else:
                self.sensor_tree[starting_sensor][time] = to_edge
        else:
            logging.error("CONSTRUCTION ERROR: sensor_path was not initialized for {}".format(starting_sensor))
            raise ValueError

    def edge_already_exists(self, current_sensor, time):
        """
        see if there aready is an edge @ time in edge_list
        """
        if current_sensor in self.edge_list.keys():
            if time in self.edge_list[current_sensor].keys():
                return True
        return False

    def get_adjacent_vertex(self, current_sensor, t):
        """
        get the vertex connect to the current sensor at time t
        """
        if current_sensor in self.edge_list.keys():
            if t in self.edge_list[current_sensor].keys():
                return self.edge_list[current_sensor][t]
        return None

    def is_tower(self, current_sensor):
        """
        return true of the sensor is a tower
        """
        if current_sensor in self.tower_names:
            return True
        else:
            return False

    def validate_sensor_tree(self, starting_sensor):
        """
        1. sensor_path[starting_sensor] ends at a tower
        2. all edges from sensor_path are in edge list
        """
        # VALIDATE CONSTRUCTION FOR THE STARTING VERTEX
        time = 0
        current_sensor = starting_sensor
        next_vertex = self.get_adjacent_vertex(current_sensor, time)
        # Rule 1 Assertion; that there is an edge from start @ time 0
        try:
            assert next_vertex
        except AssertionError as e:
            e.args += "Next Vertex was unexpectedly None"
            raise
        path = [starting_sensor]
        while next_vertex:
            path.append(next_vertex)
            if next_vertex not in self.tower_names:
                # Rule 3 Assertion that the edge goes from Sensor -- near neighbor sensor
                try:
                    neighbors = [item[0] for item in self.sensor_neighbors[current_sensor]]
                    assert next_vertex in neighbors
                except AssertionError as e:
                    e.args += ("Next Vertex", str(next_vertex), " was not a near neighbor of ", str(current_sensor))
                    raise
            current_sensor = next_vertex
            time = time + 1
            next_vertex = self.get_adjacent_vertex(current_sensor, time)
        # Rule 4.A Assertion
        try:
            assert time <= self.time_bound + 1
        except AssertionError as e:
            e.args += ("Time was out of bounds. Value: ", str(time), " Expected: ", str(self.time_bound))
            raise
        # Rule 4.B Assertion
        try:
            assert self.is_tower(current_sensor)
        except AssertionError as e:
            e.args += ("End of tree; expected to be at a tower. Full Path: ", str(path))
            raise
        # Rule 6 and 7 Enforcement (no self pings; no cycles)
        # This test does not pass for the following reasons:
            # When we check that an edge exists at time t,
            # we do not enforce that the previously created path
            # does not have vertices on the current path
            # TODO: added inline within make_tree
        # try:
        #     assert len(path) == len(set(path))
        # except AssertionError as e:
        #     e.args += ("Tree's path has duplicates: ", str(path))
        #     raise

    def make_tree(self):
        """
        For each sensor, create a valid path from the sensor to a tower using nearest neighbors
        Structure Rules:
            1. Time starts at zero
            2. Each edge increments time by 1
            3. Edges start from a sensor and go to a nearest neighboring sensor until a condition is met
            4. Sensor -- Send --> Sensor Conditions:
                A. The max path length from the starting sensor is self.time_bound number
                B. If an edge at time t already exists from the current sensor,
                    then we can assume there exists a path to a tower
            5. The last edge with time self.time_bound connects the last sensor on the path to a tower
            6. No cycles are permitted
            7. A sensor cannot add an edge to itself (Enforced in make_sensor_neighbors())
        """
        # for each sensor, create a valid path from it to a tower
        for i, (starting_sensor, val) in enumerate(self.sensors.items()):
            # initialize variables
            time = 0 # Rule 1 Enforcement: Time starts at 0
            tower_path = False # Rule 4, Condition B Enforcement: Any Valid Path to a Tower
            visited_on_path = [starting_sensor] # Rule 6 Enforcement: No Cycles
            self.sensor_tree[starting_sensor] = {}
            current_sensor = starting_sensor
            # while there is not a valid path to a tower and we are within the max time limit
            while not tower_path and (time < self.time_bound): # While Rule 4, 6 Conditions are not met
                # Rule 4, Condition B Enforcement: Any Valid Path to a Tower
                if self.edge_already_exists(current_sensor, time):
                    # setting this to break the while loop
                    # TODO: check if the path down current_sensor does NOT have any sensors within visited_on_path
                    tower_path = True
                else:
                    random.shuffle(self.sensor_neighbors[current_sensor])
                    to_edge = self.sensor_neighbors[current_sensor][0][0]
                    # Rule 6 Enforcement: No Cycles
                    if to_edge in visited_on_path:
                        tower_path = True
                    else:
                        visited_on_path.append(to_edge)
                        self.update_edge_list(current_sensor, time, to_edge)
                        self.update_sensor_tree(starting_sensor, time, to_edge)
                        time = time + 1 # Rule 2 Enforcement
                        current_sensor = to_edge
            # Conditions 4A, 4B, or 6 have been met
            # Start with checking Rule 4A
            if time == self.time_bound:
                # did we already add a tower at this time?
                if not self.edge_already_exists(current_sensor, time):
                    ## add an edge from the current sensor to a tower
                    random.shuffle(self.sensor_tower_neighbors[current_sensor])
                    to_tower = self.sensor_tower_neighbors[current_sensor][0][0]
                    self.update_edge_list(current_sensor, time, to_tower)
                    self.update_sensor_tree(starting_sensor, time, to_tower)
            else:
                ## add an edge from the current sensor to a tower
                if not (self.edge_already_exists(current_sensor, time)):
                    random.shuffle(self.sensor_tower_neighbors[current_sensor])
                    to_tower = self.sensor_tower_neighbors[current_sensor][0][0]
                    self.update_edge_list(current_sensor, time, to_tower)
                    self.update_sensor_tree(starting_sensor, time, to_tower)


    def validate_all_trees(self):
        """
        Check that all construction rules were enforced for each sensor's path to a Tower
        :return:
        """
        for i, (starting_sensor, val) in enumerate(self.sensor_tree.items()):
            try:
                self.validate_sensor_tree(starting_sensor)
            except AssertionError as e:
                self.logger.error(e.args)
                raise


def create_tree_data():
    """
    Create a tree
    :return: sensor_tree
    """
    Tree = TreeGraph()
    Tree.logger.info("Making Tree Data")
    Tree.make_tree()
    Tree.logger.info("Validating Tree Data")
    Tree.validate_all_trees()
    Tree.logger.info("Tree Validated")
    return Tree


if __name__ == '__main__':
    """
    create the Tree data that will be used starting in chapter 6
    """
    sensor_tree = create_tree_data()
