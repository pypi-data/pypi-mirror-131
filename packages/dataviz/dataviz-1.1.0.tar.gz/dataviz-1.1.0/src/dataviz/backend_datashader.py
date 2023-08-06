
import holoviews as hv
from holoviews.operation.datashader import datashade, dynspread

from . import Figure
from .utils import get_encoding_channels, load_data_into_df,\
    apply_time_conversion


hv.extension('bokeh')


class DatashaderFigure(Figure):

    def show(self, x_range=None, y_range=None):
        return self.generate_fig(x_range, y_range)

    def save(self, filename, x_range=None, y_range=None, **kwargs):
        raise NotImplementedError

    def _format_axes(self, spec):
        pass

    def generate_fig(self, x_range=None, y_range=None):
        width = self.spec['width']\
            if self.spec.get('width') else self.DEFAULT_WIDTH
        height = self.spec['height']\
            if self.spec.get('height') else self.DEFAULT_HEIGHT
        responsive = self.spec['responsive']\
            if self.spec.get('responsive') else False

        if self.spec.get('mark'):  # single view
            element = self._generate_single_view(self.spec, x_range, y_range)
            fig = element

        elif self.spec.get('layer'):
            elements = []
            for spec in self.spec['layer']:
                element = self._generate_single_view(spec, x_range, y_range)
                elements.append(element)
            fig = hv.Overlay(elements).collate()

        if responsive:
            return fig.opts(responsive=True)
        else:
            return fig.opts(width=width, height=height)

    def _generate_single_view(self, spec, x_range=None, y_range=None):
        mark = spec['mark']
        encoding = spec['encoding']

        opt = {}

        if encoding.get('color'):
            if encoding['color'].get('value'):  # fixed color
                opt['color'] = encoding['color']['value']
            else:  # color mapping
                raise NotImplementedError
        else:
            opt['color'] = 'blue'

        if encoding.get('text'):
            opt['text'] = encoding['text']

        # determine encoding channels, fields and types
        channel = get_encoding_channels(spec)

        # load data
        df = load_data_into_df(self, spec, x_range, y_range)
        if df.empty:
            return

        # bug: datashade cannot handle all values as zero
        if not any(df.value):
            df.loc[0, 'value'] = 1e-6  # workaround: set to small value

        # apply time conversion where needed
        apply_time_conversion(df, channel)

        # generate plot
        if mark == 'circle':
            element = hv.Scatter(
                df, channel['x']['field'], channel['y']['field'])

        elif mark == 'line':
            element = hv.Curve(
                df, channel['x']['field'], channel['y']['field'])

        else:
            raise NotImplementedError

        return dynspread(datashade(element, cmap=[opt['color']]))
