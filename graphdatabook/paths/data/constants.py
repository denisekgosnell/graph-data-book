import os
dir_path = os.path.dirname(os.path.realpath(__file__))

class InputFile:
  @property
  def INPUT_FILE(self):
    return dir_path + "/soc-sign-bitcoinotc.csv"


class VertexFile:
    @property
    def VERTEX_FILE(self):
        return dir_path + "/vertices.csv"

class EdgeFile:
    @property
    def EDGE_FILE(self):
        return dir_path + "/edges.csv"