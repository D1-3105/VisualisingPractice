from core.web.bokeh_views.graph_renderer import GraphRendererFactory
from core.graph_work import grapher
from bokeh.plotting import figure
from bokeh.embed import components

from core.web.bokeh_views.heli_renderer import CityRendererFactory


def generate_graph_widget(graph: grapher.Graph):
    min_way_len, min_city, cums = grapher.find_city(graph_matrix=graph.graph_matrix, node_pseudos=graph.nodes)
    graph_factory = GraphRendererFactory(graph)
    graph_factory.select_node(min_city)
    graph_renderer = graph_factory.build()
    graph_factory.set_cumulatives(cums)
    fig = figure()
    fig.renderers.append(graph_renderer)
    hover_tool_edges = graph_factory.edges_hover_tool
    hover_tool_nodes = graph_factory.nodes_hover_tool
    fig.add_tools(
        hover_tool_edges,
        hover_tool_nodes
    )
    fig.toolbar.logo = None
    fig.xaxis.visible = False
    fig.yaxis.visible = False
    fig.xgrid.visible = False
    fig.ygrid.visible = False
    return fig


def generate_graph_component(graph: grapher.Graph):
    return components(generate_graph_widget(graph))


def generate_heli_widget(hor_c, vert_c, side):
    widget = figure()
    city_factory = CityRendererFactory(vert_c, hor_c, side)
    city_factory.build()
    renderers = city_factory.renderers
    for glyph in renderers:
        widget.renderers.append(glyph)
    return widget


def generate_heli_component(hor_c, vert_c, side):
    return components(generate_heli_widget(hor_c, vert_c, side))
