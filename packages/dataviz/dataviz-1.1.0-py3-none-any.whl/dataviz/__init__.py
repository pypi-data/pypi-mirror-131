

def figure(spec, backend='matplotlib'):

    if backend == 'matplotlib':
        from .backend_matplotlib import MatplotlibFigure
        return MatplotlibFigure(spec)
    elif backend == 'bokeh':
        from .backend_bokeh import BokehFigure
        return BokehFigure(spec)
    elif backend == 'datashader':
        from .backend_datashader import DatashaderFigure
        return DatashaderFigure(spec)
    else:
        raise NotImplementedError


class Figure:

    DEFAULT_WIDTH = 800
    DEFAULT_HEIGHT = 400

    def __init__(self, spec):
        self.spec = spec
