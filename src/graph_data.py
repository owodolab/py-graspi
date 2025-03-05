import igraph as ig

class GraphData:
    """
    Class to store all graph parameters in a single object, reducing redundant function returns.
    """

    def __init__(self, graph: ig.Graph, is_2D: bool):
        """ Initialize the GraphData object with a graph and its properties. """
        self.graph = graph  # Store the igraph graph object
        self.is_2D = is_2D  # Boolean indicating whether the graph is 2D

        # Store vertex-based attributes
        self.black_vertices = []
        self.white_vertices = []
        self.shortest_path_to_red = None
        self.shortest_path_to_blue = None

        # Store computed descriptors
        self.black_green = 0
        self.black_interface_red = 0
        self.white_interface_blue = 0
        self.dim = 0
        self.interface_edge_comp_paths = 0
        self.CT_n_D_adj_An = 0
        self.CT_n_A_adj_Ca = 0

    def compute_shortest_paths(self, red_vertex, blue_vertex):
        """ Compute and store shortest paths from red and blue vertices. """
        self.shortest_path_to_red = self.graph.shortest_paths(source=red_vertex, weights=self.graph.es["weight"])[0]
        self.shortest_path_to_blue = self.graph.shortest_paths(source=blue_vertex, weights=self.graph.es["weight"])[0]


######################################
