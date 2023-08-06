from datetime import datetime, timedelta
from calendar import timegm

import requests
import numpy as np
import pandas as pd


def load_data_into_df(parent, spec, x_range, y_range, *args, **kwargs):
    data = spec['data'] if spec.get('data') else parent.spec['data']
    encoding = spec['encoding']

    if 'values' in data:  # inline data
        df = pd.DataFrame(data['values'])
    elif 'url' in data:
        url = data['url']
        query = "?" if "?" not in url else "&"
        if x_range:
            x_start = x_range[0]
            x_end = x_range[1]
            if encoding.get('x') and not encoding.get('x2'):
                query += "{}=ge:{}&".format(
                    encoding['x']['field'], isoformat(x_start))
                query += "{}=le:{}&".format(
                    encoding['x']['field'], isoformat(x_end))
            elif encoding.get('x') and encoding.get('x2'):
                query += "{}=ge:{}&".format(
                    encoding['x2']['field'], isoformat(x_start))
                query += "{}=le:{}&".format(
                    encoding['x']['field'], isoformat(x_end))
            else:
                raise NotImplementedError
        if y_range:
            raise NotImplementedError
        result = requests.get(url + query)
        if result.status_code != 200:
            return pd.DataFrame()
        result = result.json()
        if data.get('format'):
            if data['format'].get('property'):
                result = result[data['format']['property']]
        if not isinstance(result, list):
            result = [result]
        df = pd.DataFrame(result)
    elif 'dataframe' in data:
        df = kwargs.get(data['dataframe'])
    elif 'eval' in data:
        expr = data['eval']
        data = [{"result": eval(expr)}]
        df = pd.DataFrame(data)
    else:
        raise ValueError()
    return df


def get_encoding_channels(spec):
    encoding = spec['encoding']
    channel = {}
    channel['x'] = encoding.get('x')
    channel['x2'] = encoding.get('x2')
    channel['y'] = encoding.get('y')
    return channel


def apply_time_conversion(df, channel):
    def convert_field(df, field):
        if df[field].dtype == np.dtype('timedelta64[ns]'):
            df[field] = pd.to_timedelta(df[field])
        elif df[field].dtype == np.dtype('int64'):
            df[field] = pd.to_datetime(df[field] * 1e6)
        else:
            df[field] = pd.to_datetime(df[field])

    if channel['x'] and channel['x']['type'] == 'temporal':
        convert_field(df, channel['x']['field'])

    if channel['x2'] and channel['x2']['type'] == 'temporal':
        convert_field(df, channel['x2']['field'])

    if channel['y'] and channel['y']['type'] == 'temporal':
        convert_field(df, channel['y']['field'])


def default_color_palette():
    from bokeh.palettes import Category10_10 as palette
    import itertools
    return itertools.cycle(palette)


def isoformat(object):
    """ All datetime objects are stored as strings in the stretchy database.
    In order to handle comparisions properly, these strings must have a
    common format. The chosen format has microseconds resolution.
    """
    if isinstance(object, datetime):
        return object.strftime("%Y-%m-%dT%H:%M:%S.%f")
    else:
        raise NotImplementedError


def to_bokeh_timestamp(utc_datetime):
    # bokehjs plot uses nanoseconds
    return 1000 * to_timestamp(utc_datetime)


def to_timestamp(utc_datetime):
    return timegm(utc_datetime.utctimetuple())


def to_bokeh_datetime(utc_timestamp):
    # bokehjs plot uses nanoseconds
    utc_timestamp = utc_timestamp / 1000
    if utc_timestamp >= 0:
        return datetime.utcfromtimestamp(utc_timestamp)
    else:
        utc_timestamp = -1 * utc_timestamp
        seconds = utc_timestamp // 1
        microseconds = utc_timestamp % 1
        delta = timedelta(seconds=seconds, microseconds=microseconds)
        return datetime(1970, 1, 1) - delta
