from numpy import matrix, ndarray, sum, min, argmin
import numpy as np


class Graph:
    graph_matrix: matrix
    nodes: tuple

    def __init__(self, graph_matrix: matrix, node_pseudos: tuple):
        self.cum_sums = set()
        self.graph_matrix = graph_matrix
        self.nodes = node_pseudos

    def is_allowed(self, from_node, to_node):
        return self.graph_matrix[from_node, to_node] > 0

    def view_weight(self, from_node, to_node):
        return self.graph_matrix[from_node, to_node]

    def make_edges(self):
        links = set()
        for row_ind in range(self.graph_matrix.shape[0]):
            for col_ind in range(self.graph_matrix.shape[1]):
                if self.is_allowed(row_ind, col_ind):
                    links.add((row_ind, col_ind, self.graph_matrix[col_ind, row_ind]))
        return list(links)

    def graph_col_sum(self, index):
        return sum(self.graph_matrix[index])


def make_random_matrix(size: int):
    adj_matrix = np.random.random_integers(0, 2, (size, size))
    adj_matrix = np.triu(adj_matrix) + np.triu(adj_matrix, 1).T
    reachability_matrix = np.linalg.matrix_power(adj_matrix, size - 1)
    vect_func = np.vectorize(lambda x: int(np.sqrt(x)))
    reachability_matrix = vect_func(reachability_matrix)
    np.fill_diagonal(reachability_matrix, 0)
    return reachability_matrix


def find_city(graph_matrix: matrix, node_pseudos: tuple):
    graph = Graph(graph_matrix, node_pseudos)
    cum_weights = []
    for row in range(graph.graph_matrix.shape[0]):
        cum_weights.append(graph.graph_col_sum(row))

    min_indices = argmin(cum_weights)

    if isinstance(min_indices, ndarray):
        return min(cum_weights), min_indices
    return min(cum_weights), [min_indices], cum_weights
