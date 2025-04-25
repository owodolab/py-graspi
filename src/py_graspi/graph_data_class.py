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
        - **STAT_n_D** (*int*): Number of black vertices.
        - **STAT_n_A** (*int*): Number of white vertices.
        - **STAT_CC_D** (*int*): Components with at least one black vertex.
        - **STAT_CC_A** (*int*): Components with at least one white vertex.
        - **STAT_CC_D_An** (*int*): Black components connected to red vertex.
        - **STAT_CC_A_Ca** (*int*): White components connected to blue vertex.
        - **CT_f_conn_D_An** (*float*): Fraction of black vertices connected to red.
        - **CT_f_conn_A_Ca** (*float*): Fraction of white vertices connected to blue.
        - **CT_n_D_adj_An** (*int*): Some computed descriptor.
        - **CT_n_A_adj_Ca** (*int*): Another computed descriptor.

        - **countBlack_Red_conn** (*int*): Black vertices in red-connected components.
        - **countWhite_Blue_conn** (*int*): White vertices in blue-connected components.

        - **DISS_f10_D** (*float*): Fraction of black vertices <10px from green.
        - **DISS_wf10_D** (*float*): Weighted fraction of black vertices <10px from green.
        - **CT_f_D_tort1** (*float*): Fraction of black vertices with tortuosity to red < tol.
        - **CT_f_A_tort1** (*float*): Fraction of white vertices with tortuosity to blue < tol.
        - **ABS_wf_D** (*float*): Weighted distance of black vertices from red.

        - **redVertex** (*Optional[Any]*): Reference to the red vertex.
        - **blueVertex** (*Optional[Any]*): Reference to the blue vertex.
        - **first_order_neighbors** (*list*): This is a list of all the first-order pairs.
        - **second_order_neighbors** (*list*): This is a list of all the second-order pairs.
        - **third_order_neighbors** (*list*): This is a list of all the third-order pairs.

    Args:
        graph (ig.Graph): The igraph graph object representing the structure.
        is_2D (bool): Boolean indicating whether the graph is 2D
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
        self.STAT_n_D = len(self.black_vertices)
        self.STAT_n_A = len(self.white_vertices)
        self.STAT_CC_D = 0
        self.STAT_CC_A = 0
        self.STAT_CC_D_An = 0
        self.STAT_CC_A_Ca = 0
        self.CT_f_conn_D_An = 0.0
        self.CT_f_conn_A_Ca = 0.0
        self.CT_n_D_adj_An = 0
        self.CT_n_A_adj_Ca = 0

        # intermediates
        self.countBlack_Red_conn = 0
        self.countWhite_Blue_conn = 0

        # shortest path descriptors
        self.DISS_f10_D = 0
        self.DISS_wf10_D = 0
        self.CT_f_D_tort1 = 0
        self.CT_f_A_tort1 = 0
        self.ABS_wf_D = 0

        self.redVertex = None
        self.blueVertex = None
        self.first_order_neighbors = []
        self.second_order_neighbors = []
        self.third_order_neighbors = []

    def compute_shortest_paths(self, red_vertex, blue_vertex):
        """ Compute and store shortest paths from red and blue vertices. """
        self.shortest_path_to_red = self.graph.shortest_paths(source=red_vertex, weights=self.graph.es["weight"])[0]
        self.shortest_path_to_blue = self.graph.shortest_paths(source=blue_vertex, weights=self.graph.es["weight"])[0]


######################################