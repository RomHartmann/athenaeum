from collections import namedtuple

import numpy as np


def exp_decay(x0=0, y0=1, x1=200, y1=0.5):
    """Calculate the coefficients of an exponential decay function.

    https://www.elastic.co/guide/en/elasticsearch/guide/current/decay-functions.html
    https://www.elastic.co/guide/en/elasticsearch/reference/master/query-dsl-function-score-query.html#function-field-value-factor
    https://www.elastic.co/guide/en/elasticsearch/guide/master/boosting-by-popularity.html
    https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html

    :param x0:
    :type x0:
    :param y0:
    :type y0:
    :param x1:
    :type x1:
    :param y1:
    :type y1:
    :return:
    :rtype:
    """
    pass  # TODO


def recip_params(x_max, y_max, y_min=1, x_left_shift=1):
    """Calculate the parameters for the Solr recip function.

    Based on min and max boost value and the corresponding maximum boost
      amount.
    The maximum value boost amount, y_max, occurs at x = 0.  Assigned x0, y0
        This boost value causes no change to the assigned value
    The minimum boost value, y_min, orrurs at x_max.  Assigned x0, y1
        This function is assymptotical, so a "close enough" constant is chosen
    All x and y values are larger than zero (in which case negative values,
      like age are considered as "how long ago in positive numbers")

    y = a / (mx + b)

    y0 = y_min = a / b   # x0 == 0
        a = y_min * b

    y1 = assymp_thresh = a / (m * x_max + b)

    a = (m * x_max) + b   # y_max == 1

    :param x_max: x1 at which minimum boost occurs
    :type x_max: float or int
    :param y_max: The max-boost multiplyer at x0
    :type y_max: float or int
    :param y_min: Assymptotical approximation min boost at x1
    :type y_min: float or int
    :param x_left_shift: b-variable that is responsible for y-intercept at x=0
        Shifts the whole graph to the left.  Should not == 0 else inf at x=0
    :type x_left_shift: float or int
    :return: (m, a, b) to parameterize the solr recip function
    :rtype: collections.namedtuple
    """
    y0 = float(y_max)
    y1 = float(y_min)
    x1 = float(x_max)
    b = float(x_left_shift)

    # From x_min == 0 and y_max:
    a = y0 * b

    # From x_max and and y_min
    m = (((y0 * b) / y1) - b)/x1

    params = namedtuple('Params', 'm a b')
    return params(m, a, b)

