# DataViz

DataViz helps you to create plots quickly. You declare what information (the
data source) to display and how to display it (the plot type and style).
DataViz tries to be as close as possible to the [Vega-Lite](https://vega.github.io/) visualization grammar. Available backends for plotting are [matplotlib](https://matplotlib.org/) and [bokeh](https://docs.bokeh.org).

## Installation

Install via pip:

```bash
$ pip install dataviz
```

## Example

To display a plot in Jupyter notebook:

```python
import dataviz as dv

spec = {
    "width": 600,
    "height": 300,

    "data": {
        "values": [
            {"time": "2021-01-01", "value": 28},
            {"time": "2021-01-02", "value": 55},
            {"time": "2021-01-03", "value": 43},
            {"time": "2021-01-04", "value": 91},
            {"time": "2021-01-05", "value": 81},
            {"time": "2021-01-06", "value": 53},
        ]
    },
    "mark": "line",
    "encoding": {
        "x": {"field": "time", "type": "temporal"},
        "y": {"field": "value", "type": "quantitative"},
        "color": {"value": "red"},
    }
}

fig = dv.figure(spec, 'matplotlib')
fig.show()
```

This will produce the following plot:

![](docs/plot1.png)

## Contribute

- Issue Tracker: https://gitlab.com/librecube/lib/python-dataviz/-/issues
- Source Code: https://gitlab.com/librecube/lib/python-dataviz

To learn more on how to successfully contribute please read the contributing
information in the [LibreCube guidelines](https://gitlab.com/librecube/guidelines).

## Support

If you are having issues, please let us know. Reach us at
[Matrix](https://app.element.io/#/room/#librecube.org:matrix.org)
or via [Email](mailto:info@librecube.org).

## License

The project is licensed under the MIT license. See the [LICENSE](./LICENSE.txt) file for details.
