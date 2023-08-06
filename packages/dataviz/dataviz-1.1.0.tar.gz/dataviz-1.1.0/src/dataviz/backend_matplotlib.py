import math

from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt

from . import Figure
from .utils import load_data_into_df, get_encoding_channels,\
    apply_time_conversion

# suppress warnings ("No handles with labels found to put in legend.")
import logging
logging.getLogger().setLevel(logging.CRITICAL)


register_matplotlib_converters()


class MatplotlibFigure(Figure):

    INCH_PIXEL = 1/58

    def show(self, x_range=None, y_range=None, *args, **kwargs):
        self.generate_fig(x_range, y_range, *args, **kwargs)
        plt.show()

    def save(self, filename, x_range=None, y_range=None, *args, **kwargs):
        self.generate_fig(x_range, y_range, *args, **kwargs)
        plt.savefig(filename, **kwargs)
        plt.close(self.fig)

    def _format_axes(self, spec, axes):
        """Define the grid, ticks, labels and legend of the axes"""

        axes.grid(True)
        if 'color' in spec['encoding'] and\
                'field' in spec['encoding']['color']:
            axes.legend(loc='upper right')
        self.fig.autofmt_xdate()  # format x axis for dates

        if spec.get('encoding'):
            encoding = spec['encoding']

            # format y axis
            if encoding.get('y'):
                encoding_y = encoding['y']
                if encoding_y.get('scale'):
                    encoding_y_scale = encoding_y['scale']
                    if encoding_y_scale.get('range'):
                        y_scale_range = encoding_y_scale['range']
                        axes.set_yticks([
                            i for i in range(len(y_scale_range))])
                        axes.set_yticklabels(y_scale_range)
                        axes.set_ylim([-0.5, len(y_scale_range) - 0.5])
                    elif encoding_y_scale.get('domain'):
                        y_scale_range = encoding_y_scale['domain']
                        axes.set_ylim(y_scale_range)

    def _layer_view(self, layer_spec, x_range, y_range, *args, **kwargs):
        axes = {}  # keep track of additional axes, not to create duplicates
        for spec in layer_spec:
            if spec['encoding'].get('y') and\
                    spec['encoding']['y'].get('axis') and\
                    spec['encoding']['y']['axis'].get('name'):
                encoding_y_axis_name = spec['encoding']['y']['axis']['name']
                if encoding_y_axis_name != 'default' and\
                        encoding_y_axis_name not in axes:
                    # create an additional axis
                    axis = self.current_ax.twinx()
                    axes[encoding_y_axis_name] = axis
                    self.current_ax = axis
                    self.current_ax.get_yaxis().set_visible(True)
                    # show or hide the axis
                    self.current_ax.get_yaxis().set_visible(
                        spec['encoding']['y']['axis'].get('visible', True))
            self._format_axes(spec, self.current_ax)
            self._generate_single_view(spec, x_range, y_range, *args, **kwargs)

    def generate_fig(self, x_range=None, y_range=None, *args, **kwargs):
        width = self.spec['width']\
            if self.spec.get('width') else self.DEFAULT_WIDTH
        height = self.spec['height']\
            if self.spec.get('height') else self.DEFAULT_HEIGHT
        self.figsize = (width*self.INCH_PIXEL, height*self.INCH_PIXEL)

        if self.spec.get('mark'):  # single view
            self.fig, self.current_ax = plt.subplots(figsize=self.figsize)
            self._format_axes(self.spec, self.current_ax)
            self._generate_single_view(self.spec, x_range, y_range)

        elif self.spec.get('layer'):
            self.fig, self.current_ax = plt.subplots(figsize=self.figsize)
            self._layer_view(
                self.spec['layer'], x_range, y_range, *args, **kwargs)

        elif self.spec.get('concat'):
            views = len(self.spec['concat'])
            if self.spec.get('columns'):
                columns = self.spec['columns']
                rows = math.ceil(views / columns)
                subplots = (rows, columns)
            else:
                subplots = (1, views)
            self.fig, self.ax = plt.subplots(
                *subplots, sharex=True, figsize=self.figsize)
            axes = [self.ax] if subplots == (1, 1) else self.ax.reshape(-1)

            for spec, ax in zip(self.spec['concat'], axes):
                self.current_ax = ax
                if spec.get('title'):  # subplot title
                    ax.set_title(spec['title'])
                if spec.get('layer'):
                    self._layer_view(spec['layer'], x_range, y_range)
                else:
                    self._format_axes(spec, self.current_ax)
                    self._generate_single_view(spec, x_range, y_range)

        else:  # view not supported
            raise NotImplementedError

        self.fig.tight_layout()
        self.fig.subplots_adjust(top=0.92)

        if self.spec.get('title'):
            self.fig.suptitle(self.spec['title'])

        if x_range:
            plt.xlim(x_range)

    def _generate_single_view(
            self, spec, x_range=None, y_range=None, *args, **kwargs):
        mark = spec['mark']
        encoding = spec['encoding']
        opacity = 1 if not spec.get('opacity') else spec['opacity']['value']
        size = 1 if not spec.get('size') else spec['size']['value']

        opt = {}

        if encoding.get('color'):
            if encoding['color'].get('value'):  # fixed color
                opt['color'] = encoding['color']['value']
            elif encoding['color'].get('field'):  # color mapping
                opt['color_field'] = encoding['color']['field']
                opt['color_type'] = encoding['color']['type']
                if opt['color_type'] == 'nominal':  # categorical mapping
                    if encoding['color'].get('scale'):
                        color_range = encoding['color']['scale']['range']
                        color_domain = encoding['color']['scale']['domain']
                        z = zip(color_domain, color_range)
                        opt['color_map'] = {k: c for k, c in z}

        if encoding.get('text'):
            opt['text'] = encoding['text']

        if encoding.get('y'):
            if encoding['y'].get('scale'):
                if encoding['y']['scale'].get('range'):
                    opt['y_scale_range'] =\
                        spec['encoding']['y']['scale']['range']

        # determine encoding channels, fields and types
        channel = get_encoding_channels(spec)

        # load data
        df = load_data_into_df(self, spec, x_range, y_range, *args, **kwargs)
        if df.empty:
            return

        # apply time conversion where needed
        apply_time_conversion(df, channel)

        # generate plot
        if mark == 'hbar':
            if 'y_scale_range' not in opt:
                opt['y_scale_range'] = sorted(set(df[channel['y']['field']]))

            for i, category in enumerate(opt['y_scale_range']):
                df_cat = df[df[channel['y']['field']] == category]

                if 'color' in opt:
                    start = df_cat[channel['x']['field']]
                    end = df_cat[channel['x2']['field']]
                    xranges = [(l, r-l) for l, r in zip(start, end)]
                    yrange = (i - size/2, size)
                    self.current_ax.broken_barh(
                        xranges, yrange, color=opt['color'], alpha=opacity)
                    if 'text' in opt:
                        for i, row in df_cat.iterrows():
                            x = row[channel['x']['field']]
                            y = yrange[0]
                            label = row[opt['text']['field']]
                            self.current_ax.text(x, y, label)

                elif 'color_map' in opt:
                    for key, color in opt['color_map'].items():
                        df_col = df_cat[
                            df_cat[opt['color_field']] == key]
                        if df_col.empty:
                            continue
                        start = df_col[channel['x']['field']]
                        end = df_col[channel['x2']['field']]
                        xranges = [(l, r-l) for l, r in zip(start, end)]
                        yrange = (i - size/2, size)
                        self.current_ax.broken_barh(
                            xranges, yrange, color=color, alpha=opacity)
                        if 'text' in opt:
                            for i, row in df_col.iterrows():
                                x = row[channel['x']['field']]
                                y = yrange[0]
                                label = row[opt['text']['field']]
                                self.current_ax.text(x, y, label)

                else:
                    raise NotImplementedError

        elif mark == 'circle':
            if 'y_scale_range' in opt:
                map = {
                    k: v for k, v in zip(
                        opt['y_scale_range'], range(len(opt['y_scale_range'])))
                }
                df[channel['y']['field']] = df[channel['y']['field']].map(map)

            if 'color_map' in opt:
                for key, color in opt['color_map'].items():
                    df_col = df[df[opt['color_field']] == key]
                    self.current_ax.plot(
                        df_col[channel['x']['field']],
                        df_col[channel['y']['field']],
                        'o', markersize=size, color=color, alpha=opacity)
            elif 'color_field' in opt:
                categories = sorted(set(df[opt['color_field']]))
                for i, category in enumerate(categories):
                    df_cat = df[df[opt['color_field']] == category]
                    self.current_ax.plot(
                        df_cat[channel['x']['field']],
                        df_cat[channel['y']['field']],
                        'o', markersize=size, label=category, alpha=opacity)
            elif 'color' in opt:
                self.current_ax.plot(
                    df[channel['x']['field']],
                    df[channel['y']['field']], 'o',
                    markersize=size, color=opt['color'], alpha=opacity)
            else:
                self.current_ax.plot(
                    df[channel['x']['field']],
                    df[channel['y']['field']], 'o',
                    markersize=size, alpha=opacity)

        elif mark == 'line':
            if 'y_scale_range' in opt:
                map = {
                    k: v for k, v in zip(
                        opt['y_scale_range'], range(len(opt['y_scale_range'])))
                }
                df[channel['y']['field']] = df[channel['y']['field']].map(map)

            if 'color_map' in opt:
                for key, color in opt['color_map'].items():
                    df_col = df[df[opt['color_field']] == key]
                    self.current_ax.plot(
                        df_col[channel['x']['field']],
                        df_col[channel['y']['field']],
                        linewidth=size, color=color, alpha=opacity)
            elif 'color_field' in opt:
                categories = sorted(set(df[opt['color_field']]))
                for i, category in enumerate(categories):
                    df_cat = df[df[opt['color_field']] == category]
                    self.current_ax.plot(
                        df_cat[channel['x']['field']],
                        df_cat[channel['y']['field']],
                        linewidth=size, label=category, alpha=opacity)
            elif 'color' in opt:
                self.current_ax.plot(
                    df[channel['x']['field']],
                    df[channel['y']['field']],
                    linewidth=size, color=opt['color'], alpha=opacity)
            else:
                element, = self.current_ax.plot(
                    df[channel['x']['field']],
                    df[channel['y']['field']],
                    linewidth=size, alpha=opacity)

        elif mark == 'rule':
            for x in df[channel['x']['field']]:
                self.current_ax.axvline(x, color=opt['color'], alpha=opacity)

        else:
            raise NotImplementedError
