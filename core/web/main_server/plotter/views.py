from random import randint

from django.core.exceptions import BadRequest
from django.views.generic import TemplateView, FormView
from core.web.bokeh_views.views import generate_graph_component, generate_heli_component
from core.graph_work.grapher import Graph, make_random_matrix
from core.web.main_server.plotter.forms import HelicopterParametersForm


class GraphView(TemplateView):
    template_name = 'plotter/graph_template.html'

    def get_context_data(self, **kwargs):
        rand_mat = make_random_matrix(size:=randint(5, 10))
        graph = Graph(rand_mat, [str(i) for i in range(size)])
        script, div = generate_graph_component(graph)
        return {
            'script': script,
            'div': div,
            'matrix': rand_mat.tolist(),
            'size': size
        }


class HeliView(TemplateView):
    template_name = 'plotter/heli_template.html'

    def get_context_data(self, **kwargs):
        param_form = HelicopterParametersForm(data=self.request.GET)
        if not param_form.is_valid():
            raise BadRequest({'error': param_form.errors})
        params = param_form.cleaned_data
        script, div = generate_heli_component(**params)
        return {
            'script': script,
            'div': div
        }


class IndexView(TemplateView):
    template_name = 'plotter/index.html'

    def get_context_data(self, **kwargs):

        return {'form_33': HelicopterParametersForm()}

# Create your views here.
