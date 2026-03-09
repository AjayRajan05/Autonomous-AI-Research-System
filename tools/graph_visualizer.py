import matplotlib.pyplot as plt
import networkx as nx


def visualize(graph):

    pos = nx.spring_layout(graph)

    nx.draw(
        graph,
        pos,
        node_size=50,
        with_labels=False
    )

    plt.show()