import igraph as ig

class graph_data_class:
    """
    Class to store all graph parameters in a single object, reducing redundant function returns.

    **Attributes:**
        - **graph** (*ig.Graph*): Stores the igraph graph object.
        - **is_2D** (*bool*): Indicates whether the graph is 2D.
        - **black_vertices** (*list*): A list to store black vertices in the graph.
        - **white_vertices** (*list*): A list to store white vertices in the graph.
        - **shortest_path_to_red** (*Optional[list]*): Stores the shortest path to the red vertex.
        - **shortest_path_to_blue** (*Optional[list]*): Stores the shortest path to the blue vertex.
        - **black_green** (*int*): Computed descriptor for black-green interaction.
        - **black_interface_red** (*int*): Computed descriptor for the black-red interface.
        - **white_interface_blue** (*int*): Computed descriptor for the white-blue interface.
        - **dim** (*int*): Dimension descriptor for the graph.
        - **interface_edge_comp_paths** (*int*): Number of interface edges in computed paths.
        - **CT_n_D_adj_An** (*int*): Some computed descriptor.
        - **CT_n_A_adj_Ca** (*int*): Another computed descriptor.
        - **redVertex** (*Optional[Any]*): Reference to the red vertex.
        - **blueVertex** (*Optional[Any]*): Reference to the blue vertex.

    Args:
        graph (ig.Graph): The igraph graph object representing the structure.
        is_2D (str): Boolean indicating whether the graph is 2D
    """

    def __init__(self, graph: ig.Graph, is_2D: bool):
        """ Initialize the graph_data_class object with a graph and its properties. """

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
        self.redVertex = None
        self.blueVertex = None

    def compute_shortest_paths(self, red_vertex, blue_vertex):
        """ Compute and store shortest paths from red and blue vertices. """
        self.shortest_path_to_red = self.graph.shortest_paths(source=red_vertex, weights=self.graph.es["weight"])[0]
        self.shortest_path_to_blue = self.graph.shortest_paths(source=blue_vertex, weights=self.graph.es["weight"])[0]


######################################