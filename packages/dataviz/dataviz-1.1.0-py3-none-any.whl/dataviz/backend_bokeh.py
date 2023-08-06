import math

from pandas.api.types import CategoricalDtype
from bokeh.io import show, output_notebook
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, CategoricalColorMapper, Range1d,\
    DatetimeTickFormatter, Span, LabelSet, FixedTicker, LinearAxis,\
    DataRange1d, CategoricalAxis, FactorRange
from bokeh.layouts import gridplot
from bokeh.palettes import d3

from . import Figure
from .utils import load_data_into_df, get_encoding_channels,\
    apply_time_conversion, default_color_palette


_DATETIME_FORMAT = dict(
    microseconds=["%H:%M:%S.%f"],
    milliseconds=["%H:%M:%S.%f"],
    seconds=["%T"],
    minsec=["%T"],
    minutes=["%H:%M"],
    hourmin=["%H:%M"],
    hours=["%H:%M"],
    days=["%a %d/%m"],
    months=["%b'%g"],
    years=["%Y"],
)

_color_index = 0


class BokehFigure(Figure):

    def show(self, x_range=None, y_range=None):
        fig = self.generate_fig(x_range, y_range)
        output_notebook()
        self.handle = show(fig, notebook_handle=True)

    def save(self, filename, x_range=None, y_range=None, **kwargs):
        raise NotImplementedError

    def _get_color(self):
        global _color_index
        color = d3['Category10'][10][_color_index]
        _color_index = _color_index + 1 if _color_index < 9 else 0
        return color

    def _format_axes(self, spec):
        kw = {}
        kw['tools'] = 'wheel_zoom,box_zoom,pan,reset,save'
        kw['active_scroll'] = 'wheel_zoom'
        kw['active_drag'] = 'pan'
        if spec['encoding'].get('y'):
            if spec['encoding']['y'].get('scale'):
                if spec['encoding']['y']['scale'].get('range'):  # categorical
                    kw['tools'] = 'xwheel_zoom,xpan,reset,save'
                    kw['active_scroll'] = 'xwheel_zoom'
                    kw['active_drag'] = 'xpan'
            if spec['encoding']['y']['type'] == 'temporal':
                kw['y_axis_type'] = 'datetime'
        if spec['encoding']['x']['type'] == 'temporal':
            kw['x_axis_type'] = 'datetime'
        return kw

    def generate_fig(self, x_range=None, y_range=None):
        width = self.spec['width']\
            if self.spec.get('width') else self.DEFAULT_WIDTH
        height = self.spec['height']\
            if self.spec.get('height') else self.DEFAULT_HEIGHT

        if self.spec.get('mark'):  # single view
            kw = self._format_axes(self.spec)
            fig = figure(
                plot_width=width, plot_height=height,
                toolbar_location='above', **kw)
            if 'x_axis_type' in kw and kw['x_axis_type'] == 'datetime':
                fig.xaxis.formatter =\
                    DatetimeTickFormatter(**_DATETIME_FORMAT)
            self._generate_single_view(fig, self.spec, x_range, y_range)

        elif self.spec.get('layer'):
            kw = self._format_axes(self.spec['layer'][0])
            fig = figure(
                plot_width=width, plot_height=height,
                toolbar_location='above', **kw)
            if 'x_axis_type' in kw and kw['x_axis_type'] == 'datetime':
                fig.xaxis.formatter =\
                    DatetimeTickFormatter(**_DATETIME_FORMAT)
            for spec in self.spec['layer']:
                self._generate_single_view(fig, spec, x_range, y_range)

        elif self.spec.get('concat'):
            views = len(self.spec['concat'])
            columns = self.spec['columns']\
                if self.spec.get('columns') else views
            rows = math.ceil(views / columns)
            subfigs = []
            for spec in self.spec['concat']:
                if spec.get('layer'):
                    kw = self._format_axes(spec['layer'][0])
                    subfig = figure(
                        plot_width=width, plot_height=height,
                        toolbar_location='above', **kw)
                    if 'x_axis_type' in kw and kw['x_axis_type'] == 'datetime':
                        subfig.xaxis.formatter =\
                            DatetimeTickFormatter(**_DATETIME_FORMAT)
                    for spec in spec['layer']:
                        self._generate_single_view(
                            subfig, spec, x_range, y_range)
                else:
                    kw = self._format_axes(spec)
                    subfig = figure(**kw)
                    if 'x_axis_type' in kw and kw['x_axis_type'] == 'datetime':
                        subfig.xaxis.formatter =\
                            DatetimeTickFormatter(**_DATETIME_FORMAT)
                    if 'title' in spec:
                        subfig.title.text = spec['title']
                    self._generate_single_view(subfig, spec, x_range, y_range)
                subfigs.append(subfig)
            fig = gridplot(
                subfigs, ncols=columns,
                plot_width=self.spec['width']//columns,
                plot_height=self.spec['height']//rows,
                merge_tools=False)

        else:  # view not supported
            raise NotImplementedError

        if self.spec.get('title'):
            if hasattr(fig, 'title'):
                fig.title.text = self.spec['title']

        if x_range and hasattr(fig, 'x_range'):
            fig.x_range = Range1d(*x_range)

        # fig.legend.location = "top_left"
        # fig.legend.click_policy = "hide"

        return fig

    def _generate_single_view(self, fig, spec, x_range=None, y_range=None):
        mark = spec['mark']
        encoding = spec['encoding']
        opacity = 1 if not spec.get('opacity') else spec['opacity']['value']
        size = 1 if not spec.get('size') else spec['size']['value']

        opt = {}

        if encoding.get('color'):
            if encoding['color'].get('value'):  # fixed color
                opt['color'] = encoding['color']['value']
            else:  # color mapping
                opt['color_field'] = encoding['color']['field']
                opt['color_type'] = encoding['color']['type']
                if opt['color_type'] == 'nominal':  # categorical mapping
                    if encoding['color'].get('scale'):
                        color_range = encoding['color']['scale']['range']
                        color_domain = encoding['color']['scale']['domain']
                        z = zip(color_domain, color_range)
                        opt['color_map'] = {k: c for k, c in z}
                        ccm = CategoricalColorMapper(
                            palette=color_range, factors=color_domain)
                        opt['color'] = {
                            'field': opt['color_field'], 'transform': ccm}
        else:
            opt['color'] = self._get_color()

        if encoding.get('text'):
            opt['text'] = encoding['text']

        # determine encoding channels, fields and types
        channel = get_encoding_channels(spec)

        # load data
        df = load_data_into_df(self, spec, x_range, y_range)
        if df.empty:
            return

        # apply time conversion where needed
        apply_time_conversion(df, channel)

        # convert categorical axis to numerical axis
        # this is a workaround, as numerical and categorical axis cannot
        # be used together (e.g. as needed for a layered plot)
        y_range_name = 'default'
        if encoding.get('y'):

            if encoding['y'].get('axis') and encoding['y']['axis'].get('name'):
                y_range_name = encoding['y']['axis']['name']

            if y_range_name != 'default' and\
                    y_range_name not in fig.extra_y_ranges:
                fig.extra_y_ranges[y_range_name] = DataRange1d()
                fig.add_layout(LinearAxis(
                    y_range_name=y_range_name), 'right')
                fig.yaxis[-1].visible =\
                    encoding['y']['axis'].get('visible', True)

            if encoding['y'].get('scale') and\
                    encoding['y']['scale'].get('domain'):
                domain = spec['encoding']['y']['scale']['domain']
                if y_range_name != 'default':
                    fig.extra_y_ranges[y_range_name] =\
                        Range1d(domain[0], domain[1])
                else:  # set the y range
                    fig.y_range = Range1d(domain[0], domain[1])

            if encoding['y'].get('scale') and\
                    encoding['y']['scale'].get('range'):
                y_range = encoding['y']['scale']['range']
                y_labels = zip(range(len(y_range)), y_range)
                if y_range_name == 'default':
                    fig.y_range = Range1d(-0.5, len(y_range)-0.5)
                    fig.yaxis.major_label_overrides = dict(y_labels)
                    fig.yaxis.ticker = FixedTicker(
                        ticks=[i for i, __ in enumerate(y_range)])
                else:
                    fig.extra_y_ranges[y_range_name] =\
                        Range1d(-0.5, len(y_range)-0.5)
                    fig.yaxis[-1].major_label_overrides = dict(y_labels)
                    fig.yaxis[-1].ticker = FixedTicker(
                        ticks=[i for i, __ in enumerate(y_range)])

                cat_type = CategoricalDtype(
                   categories=y_range, ordered=True)
                df[channel['y']['field']] =\
                    df[channel['y']['field']].astype(cat_type).cat.codes

        # generate plot
        if mark == 'hbar':
            fig.hbar(
                y=channel['y']['field'],
                left=channel['x']['field'],
                right=channel['x2']['field'],
                color=opt['color'],
                height=size,
                source=ColumnDataSource(df),
                alpha=opacity,
                y_range_name=y_range_name)
            if 'text' in opt:
                labels = LabelSet(
                    x=channel['x']['field'],
                    y=channel['y']['field'],
                    text=opt['text']['field'],
                    source=ColumnDataSource(df),
                    y_range_name=y_range_name)
                fig.add_layout(labels)

        elif mark == 'circle':
            if 'color' in opt:
                fig.circle(
                    x=channel['x']['field'],
                    y=channel['y']['field'],
                    color=opt['color'],
                    size=size,
                    source=ColumnDataSource(df),
                    alpha=opacity,
                    y_range_name=y_range_name)
            elif 'color_field' in opt:
                categories = sorted(set(df[opt['color_field']]))
                for cat, color in zip(categories, default_color_palette()):
                    df_col = df[df[opt['color_field']] == cat]
                    fig.circle(
                        x=channel['x']['field'],
                        y=channel['y']['field'],
                        legend_label=cat,
                        color=color,
                        size=size,
                        source=ColumnDataSource(df_col),
                        alpha=opacity,
                        y_range_name=y_range_name)

        elif mark == 'line':
            if 'color_map' in opt:
                # workaround because Line does not accept ColorSpec
                for key, color in opt['color_map'].items():
                    df_col = df[df[opt['color_field']] == key]
                    fig.line(
                        x=channel['x']['field'],
                        y=channel['y']['field'],
                        color=color,
                        line_width=size,
                        source=ColumnDataSource(df_col),
                        alpha=opacity,
                        y_range_name=y_range_name)
            elif 'color_field' in opt:
                categories = sorted(set(df[opt['color_field']]))
                for cat, color in zip(categories, default_color_palette()):
                    df_col = df[df[opt['color_field']] == cat]
                    fig.line(
                        x=channel['x']['field'],
                        y=channel['y']['field'],
                        legend_label=cat,
                        color=color,
                        line_width=size,
                        source=ColumnDataSource(df_col),
                        alpha=opacity,
                        y_range_name=y_range_name)
            elif 'color' in opt:
                fig.line(
                    x=channel['x']['field'],
                    y=channel['y']['field'],
                    color=opt['color'],
                    line_width=size,
                    source=ColumnDataSource(df),
                    alpha=opacity,
                    y_range_name=y_range_name)

        elif mark == 'rule':
            for x in df[channel['x']['field']]:
                span = Span(
                    location=x, dimension='height',
                    line_color=opt['color'], line_alpha=opacity)
                fig.add_layout(span)

        else:  # plot type not yet supported
            raise NotImplementedError
