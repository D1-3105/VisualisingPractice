from bokeh.models import (
    GlyphRenderer,
    Rect,
    Arrow, OpenHead,
    ColumnDataSource
)

from core.heli.poly import gen_quadro_poly_start_points, make_quadro_corners, is_line_inside


class DistrictFactory:
    renderer: GlyphRenderer

    def __init__(self, side, data_source):
        self.renderer = GlyphRenderer()
        self.renderer.data_source = data_source
        self.renderer.glyph = Rect(
            x='x0', y='y0',
            width=side, height=side,
            fill_color='#FFFFFF', line_color='#000000')
        self.renderer.selection_glyph = Rect(
            x='x0', y='y0',
            width=side, height=side,
            fill_color='#cccccc', line_color='#000000')


class CityRendererFactory:
    renderers: list[GlyphRenderer]

    def __init__(self, hor_dist_n, vert_dist_n, side):
        self.renderers = []
        self.source = ColumnDataSource(
            dict()
        )
        self.hor_n = hor_dist_n
        self.ver_n = vert_dist_n
        self.side = side

    def build_heli_vector(self):
        vector_line = Arrow(
            end=OpenHead(
                line_color='red',
                line_width=3,
            ),
            line_color='red',
            line_width=3,
            x_start=0,
            y_start=0,
            x_end=self.side * self.hor_n,
            y_end=self.side * self.ver_n
        )
        self.renderers.append(vector_line)

    def calculate_line(self):
        quadro_params, d = make_quadro_corners(self.ver_n, self.hor_n, self.side)
        vector_k = (quadro_params[self.hor_n - 1][self.ver_n - 1][0]
                    /
                    quadro_params[self.hor_n - 1][self.ver_n - 1][1])
        vector_b = 0
        crossed = []
        for r_ind, q_r in enumerate(quadro_params):
            for c_ind, q_col in enumerate(q_r):
                if is_line_inside(vector_k, vector_b, *q_col[::-1], d=d):
                    crossed.append(self.hor_n * c_ind + r_ind)
        self.source.selected.indices = crossed

    def build_district_glyphs(self):
        start_coords_gen = gen_quadro_poly_start_points(self.ver_n, self.hor_n, self.side)
        y0s = []
        x0s = []
        indices = []
        for ind, start_c in enumerate(start_coords_gen):
            y0s.append(start_c[0] + self.side / 2)
            x0s.append(start_c[1] + self.side / 2)
            indices.append(ind)
        self.source.add(y0s, 'y0')
        self.source.add(x0s, 'x0')
        self.source.add(indices, 'indices')
        district_g = DistrictFactory(side=self.side, data_source=self.source)
        self.renderers.append(district_g.renderer)

    def build(self):
        self.build_district_glyphs()
        self.calculate_line()
        self.build_heli_vector()
