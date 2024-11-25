import sys
import igraph
import igraph_testing as ig
import img_to_txt as translate
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np


def visualize(g):
    layout = g.layout('kk')  # Kamada-Kawai layout for better spacing
    fig, ax = plt.subplots(figsize=(10, 10))
    plot = igraph.plot(g,
                       target=ax,
                       layout=layout,
                       vertex_colors = g.vs["color"],
                       vertex_size=10,
                       margin=20)
    axcolor = 'lightgoldenrodyellow'

    ax_zoom_in = plt.axes([0.7, 0.05, 0.1, 0.075], facecolor=axcolor)
    ax_zoom_out = plt.axes([0.81, 0.05, 0.1, 0.075], facecolor=axcolor)
    ax_rotate = plt.axes([0.92, 0.05, 0.1, 0.075], facecolor=axcolor)

    button_zoom_in = Button(ax_zoom_in, label='Zoom In')
    button_zoom_out = Button(ax_zoom_out, label='Zoom Out')
    button_rotate = Button(ax_rotate, label='Rotate')

    current_angle = [0]

    button_zoom_in.on_clicked(lambda event: zoom_in(event, ax))
    button_zoom_out.on_clicked(lambda event: zoom_out(event, ax))
    button_rotate.on_clicked(lambda event: rotate(event, ax, g, layout,current_angle, 30))

    plt.show()


def filter_black_vertices(graph):
    """
        Filters the graph by keeping only edges between vertices of the same color {black}.

        Args:
            graph (ig.Graph): The input graph.

        Returns:
            ig.Graph: The filtered graph.
        """
    edgeList = graph.get_edgelist()
    keptEdges = []

    # Checks edges and keeps only edges that connect to the same colored vertices
    for edge in edgeList:
        currentNode = edge[0]
        toNode = edge[1]
        if (graph.vs[currentNode]['color'] == 'black') and (graph.vs[toNode]['color'] == 'black'):
            keptEdges.append(edge)
        if ((graph.vs[currentNode]['color'] == 'blue') or (graph.vs[toNode]['color'] == 'blue')):
            keptEdges.append(edge)
        elif ((graph.vs[currentNode]['color'] == 'red') or (graph.vs[toNode]['color'] == 'red')) :
            keptEdges.append(edge)
    filteredGraph = graph.subgraph_edges(keptEdges, delete_vertices=True)

    return filteredGraph


def filter_white_vertices(graph):
    """
        Filters the graph by keeping only edges between vertices of the same color {white}.

        Args:
            graph (ig.Graph): The input graph.

        Returns:
            ig.Graph: The filtered graph.
        """
    edgeList = graph.get_edgelist()
    keptEdges = []

    # Checks edges and keeps only edges that connect to the same colored vertices
    for edge in edgeList:
        currentNode = edge[0]
        toNode = edge[1]
        if (graph.vs[currentNode]['color'] == 'white') and (graph.vs[toNode]['color'] == 'white'):
            keptEdges.append(edge)
        if ((graph.vs[currentNode]['color'] == 'blue') or (graph.vs[toNode]['color'] == 'blue')):
            keptEdges.append(edge)
        elif ((graph.vs[currentNode]['color'] == 'red') or (graph.vs[toNode]['color'] == 'red')) :
            keptEdges.append(edge)


    filteredGraph = graph.subgraph_edges(keptEdges, delete_vertices=True)

    return filteredGraph


def zoom_in(event, ax):
    xlims = ax.get_xlim()
    ylims = ax.get_ylim()

    # Calculate the center of the plot
    x_center = (xlims[0] + xlims[1]) / 2
    y_center = (ylims[0] + ylims[1]) / 2

    # Define a more aggressive zoom factor
    factor = 0.5  # Change this value to zoom in more

    # Calculate new limits
    x_range = (xlims[1] - xlims[0]) * factor
    y_range = (ylims[1] - ylims[0]) * factor
    new_xlims = [x_center - x_range / 2, x_center + x_range / 2]
    new_ylims = [y_center - y_range / 2, y_center + y_range / 2]

    # Set new limits
    ax.set_xlim(new_xlims)
    ax.set_ylim(new_ylims)
    plt.draw()


def zoom_out(event, ax):
    xlims = ax.get_xlim()
    ylims = ax.get_ylim()

    # Calculate the center of the plot
    x_center = (xlims[0] + xlims[1]) / 2
    y_center = (ylims[0] + ylims[1]) / 2

    # Define a more aggressive zoom factor
    factor = 2  # Change this value to zoom in less

    # Calculate new limits
    x_range = (xlims[1] - xlims[0]) * factor
    y_range = (ylims[1] - ylims[0]) * factor
    new_xlims = [x_center - x_range / 2, x_center + x_range / 2]
    new_ylims = [y_center - y_range / 2, y_center + y_range / 2]

    # Set new limits
    ax.set_xlim(new_xlims)
    ax.set_ylim(new_ylims)
    plt.draw()


def rotate(event, ax, g, layout,current_angle, angle):
    # Preserve current zoom limits
    xlims = ax.get_xlim()
    ylims = ax.get_ylim()

    # Convert the angle to radians
    current_angle[0] += angle
    angle_rad = np.deg2rad(current_angle[0])

    # Get the original layout coordinates
    coords = np.array(layout.coords)

    # Rotate the coordinates
    cos_angle = np.cos(angle_rad)
    sin_angle = np.sin(angle_rad)
    rotation_matrix = np.array([[cos_angle, -sin_angle], [sin_angle, cos_angle]])
    rotated_coords = coords.dot(rotation_matrix)

    # Update the layout with the rotated coordinates
    new_layout = igraph.Layout(rotated_coords.tolist())

    # Clear the current plot and redraw the graph with the new layout
    ax.clear()
    plot = igraph.plot(g,
                       target=ax,
                       layout=new_layout,
                       vertex_colors=g.vs["color"],
                       vertex_size=5,
                       margin=20)

    # Reapply the previous zoom limits
    ax.set_xlim(xlims)
    ax.set_ylim(ylims)
    plt.draw()


def main():
    input_file = sys.argv[1]
    resize_factor = sys.argv[2]
    resize_factor = float(resize_factor)
    translate.img_to_txt(input_file,resize_factor)
    txt_filename = "resized/resized_" +input_file[7:-4]+".txt"
    (g, is_2D, black_vertices, white_vertices, black_green, black_interface_red, white_interface_blue,
     dim, interface_edge_comp_paths, shortest_path_to_red, shortest_path_to_blue,
     CT_n_D_adj_An, CT_n_A_adj_Ca) = ig.generateGraphAdj(txt_filename)
    print("graph created")
    whiteFilteredGraph = filter_white_vertices(g)
    print("graph filtered")
    visualize(whiteFilteredGraph)
    blackFilteredGraph = filter_black_vertices(g)
    visualize(blackFilteredGraph)

if __name__ == "__main__":
    main()