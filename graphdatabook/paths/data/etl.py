from datetime import datetime
import csv
from constants import InputFile, VertexFile, EdgeFile


def write_edges():
    """
    1. Open soc-sign-bitcoinotc
    2. Transform the timestamp to ISO
    3. write header and edges to edges.csv
    :return:
    """
    # open soc-sign-bitcoinotc
    with open(InputFile().INPUT_FILE, "r") as read_file:
        with open(EdgeFile().EDGE_FILE, "w") as write_file:
            # write edge table header; this MUST match the table definition in DS Graph
            write_file.write("out_publicKey,in_publicKey,trust,datetime\n")
            wr = csv.writer(write_file, quoting=csv.QUOTE_ALL)
            for line in read_file:
                data = line.replace('\n',"").split(",")
                epoch_time = float(data[3])
                # transform the time to ISO 8601 Standard
                str_time = datetime.fromtimestamp(epoch_time).isoformat()
                data[3] = str_time
                wr.writerow(data)

def write_vertices():
    """
    1. Open soc-sign-bitcoinotc
    2. Extract all addresses
    2. write header and unique vertices to edges.csv
    :return:
    """
    addresses = []
    with open(InputFile().INPUT_FILE, "r") as read_file:
        for line in read_file:
            data = line.replace('\n', "").split(",")
            addresses.append(int(data[0]))
            addresses.append(int(data[1]))
    # sort all addresses and get unique addresses
    vertices = list(set(sorted(addresses)))
    with open(VertexFile().VERTEX_FILE, "w") as write_file:
        # write vertex table header; this MUST match the table definition in DS Graph
        write_file.write("publicKey\n")
        for vertex in vertices:
            write_file.write(str(vertex))
            write_file.write("\n")


def driver():
    write_vertices()
    write_edges()


if __name__ == '__main__':
    driver()