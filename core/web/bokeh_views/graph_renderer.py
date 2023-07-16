import random
from bokeh.models import (
    GraphRenderer,
    StaticLayoutProvider,
    Circle,
    MultiLine,
    NodesAndLinkedEdges,
    HoverTool
)
from core.graph_work.grapher import Graph


class GraphRendererFactory:
    renderer: GraphRenderer
    graph: Graph

    def __init__(self, graph: Graph):
        self.renderer = GraphRenderer()
        self.graph = graph

        self.renderer.node_renderer.glyph = Circle(size=20, fill_color="#272832", fill_alpha=4)
        self.renderer.edge_renderer.glyph = MultiLine(line_color='#272832', line_alpha=0.5)
        self.renderer.node_renderer.selection_glyph = Circle(size=20, fill_color='#ed1557')
        self.renderer.edge_renderer.hover_glyph = MultiLine(line_color='#c392c3', line_alpha=0.9)
        self.renderer.node_renderer.hover_glyph = Circle(size=20, fill_color="#ffff00", fill_alpha=1)
        self.renderer.inspection_policy = NodesAndLinkedEdges()

    def select_node(self, selected):
        self.renderer.node_renderer.data_source.selected.indices = selected

    @staticmethod
    def make_random_pos() -> float:
        return random.randint(0, 6) / random.randint(1, 10)

    def nodes_from_graph(self):
        data_static = {
            node_index: [self.make_random_pos(), self.make_random_pos()]
            for node_index in range(len(self.graph.nodes))
        }
        self.renderer.layout_provider = StaticLayoutProvider(graph_layout=data_static)
        self.renderer.node_renderer.data_source.add(list(range(len(self.graph.nodes))), 'index')
        self.renderer.node_renderer.data_source.add(self.graph.nodes, 'name')

    def set_cumulatives(self, cum_sums):
        self.renderer.node_renderer.data_source.add(cum_sums, 'cumulative')

    def edges_from_graph(self):
        starts = []
        ends = []
        ways = []
        for start, end, way in self.graph.make_edges():
            starts.append(start)
            ends.append(end)
            ways.append(way)
        self.renderer.edge_renderer.data_source.data = dict(start=starts, end=ends, way=ways)

    @property
    def edges_hover_tool(self):
        hover_tool_edges = HoverTool(
            renderers=[self.renderer.edge_renderer],
            name='Hover edges'
        )
        hover_tool_edges.mode = 'mouse'
        hover_tool_edges.line_policy = 'interp'
        hover_tool_edges.tooltips = [
            ('way', '@way')
        ]
        return hover_tool_edges

    @property
    def nodes_hover_tool(self):
        hover_tool_nodes = HoverTool(
            renderers=[self.renderer.node_renderer],
            name='Hover nodes'
        )
        hover_tool_nodes.mode = 'mouse'
        hover_tool_nodes.line_policy = 'nearest'
        hover_tool_nodes.tooltips = [
            ('cumulative', '@cumulative')
        ]
        return hover_tool_nodes

    def build(self):
        self.nodes_from_graph()
        self.edges_from_graph()
        return self.renderer
