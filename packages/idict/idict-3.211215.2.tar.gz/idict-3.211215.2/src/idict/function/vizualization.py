from itertools import repeat

import numpy as np
import pandas

from idict.macro import isnumber


def X2histogram(col=0, input="X", output="histogram", **kwargs):
    """
    >>> import numpy as np
    >>> from idict import let
    >>> X = np.array([["a", 2.1, 1.6], ["a", 3, 2], ["b", 7, 3]])
    >>> X2histogram(X=X, col=0)
    {'histogram': [{'x': 'a', 'count': 2}, {'x': 'b', 'count': 1}], '_history': Ellipsis}
    >>> from idict import idict
    >>> from idict.function.dataset import df2Xy
    >>> d = idict.fromtoy(output_format="df") >> df2Xy >> X2histogram
    >>> d.histogram
    [{'x': '(-0.9, 2.2]', 'count': 8}, {'x': '(2.2, 5.3]', 'count': 6}, {'x': '(5.3, 8.4]', 'count': 3}, {'x': '(8.4, 11.5]', 'count': 2}, {'x': '(11.5, 14.6]', 'count': 0}, {'x': '(14.6, 17.7]', 'count': 0}, {'x': '(17.7, 20.8]', 'count': 0}, {'x': '(20.8, 23.9]', 'count': 0}, {'x': '(23.9, 27.0]', 'count': 0}, {'x': '(27.0, 30.1]', 'count': 0}]
    """
    X = kwargs[input]
    vals = X.iloc[:, col] if hasattr(X, "iloc") else X[:, col]
    if isnumber(vals[0]):
        cut = list(map(float, vals))
        maximum = max(cut)
        minimum = min(cut)
        step = (maximum - minimum) / 10
        ranges = np.arange(minimum - 1, maximum + 1, step)

        df = pandas.DataFrame(cut)
        df2 = df.groupby(pandas.cut(cut, ranges)).count()
        dic = df2.to_dict()[0]
    else:
        from pandas import Series

        dic = Series(vals).value_counts()
    result = [{"x": str(k), "count": v} for k, v in dic.items()]
    return {output: result, "_history": ...}


def tofloat(X, k, col):
    if hasattr(X, "iloc"):
        X = X.iloc
    val = X[k, col]
    try:
        return float(val)
    except ValueError:
        return float(list(X[:, col]).index(val))


def Xy2scatterplot(colx=0, coly=1, Xin="X", yin="y", output="scatterplot", **kwargs):
    """
    >>> import numpy as np
    >>> X = np.array([["c1", 2.1, 1.6], ["c2", 3.2, 2.3], ["c3", 7, 3]])
    >>> y = np.array(["a", "b", "c"])
    >>> Xy2scatterplot(X=X, y=y, colx=1, coly=2)
    {'scatterplot': [{'id': 'a', 'data': [{'x': 2.1, 'y': 1.6}]}, {'id': 'b', 'data': [{'x': 3.2, 'y': 2.3}]}, {'id': 'c', 'data': [{'x': 7.0, 'y': 3.0}]}], '_history': Ellipsis}
    >>> Xy2scatterplot(X=X, y=y, colx=1, coly=0)
    {'scatterplot': [{'id': 'a', 'data': [{'x': 2.1, 'y': 0.0}]}, {'id': 'b', 'data': [{'x': 3.2, 'y': 1.0}]}, {'id': 'c', 'data': [{'x': 7.0, 'y': 2.0}]}], '_history': Ellipsis}
    >>> from idict import idict
    >>> from idict.function.dataset import df2Xy
    >>> d = idict.fromtoy(output_format="df") >> df2Xy >> Xy2scatterplot
    >>> d.scatterplot
    [{'id': '0', 'data': [{'x': 5.1, 'y': 6.4}, {'x': 6.1, 'y': 3.6}, {'x': 3.1, 'y': 2.5}, {'x': 9.1, 'y': 3.5}, {'x': 9.1, 'y': 7.2}, {'x': 7.1, 'y': 6.6}, {'x': 2.1, 'y': 0.1}, {'x': 5.1, 'y': 4.5}, {'x': 1.1, 'y': 3.2}, {'x': 3.1, 'y': 2.5}]}, {'id': '1', 'data': [{'x': 1.1, 'y': 2.5}, {'x': 1.1, 'y': 3.5}, {'x': 4.7, 'y': 4.9}, {'x': 8.3, 'y': 2.9}, {'x': 2.5, 'y': 4.5}, {'x': 0.1, 'y': 4.3}, {'x': 0.1, 'y': 4.0}, {'x': 31.1, 'y': 4.7}, {'x': 2.2, 'y': 8.5}, {'x': 1.1, 'y': 8.5}]}]
    """
    X = kwargs[Xin]
    y = kwargs[yin]
    result = []
    for m in dict(zip(y, repeat(None))):
        inner = []
        for k in range(len(X)):
            left = m if isinstance(m, str) else str(float(m))
            if isinstance(y[k], str):
                right = y[k]
            else:
                right = str(float(y[k]))
            if left == right:
                x_ = tofloat(X, k, colx)
                y_ = tofloat(X, k, coly)
                inner.append({"x": x_, "y": y_})
        result.append({"id": str(m), "data": inner})
    return {output: result, "_history": ...}


X2histogram.metadata = {
    "id": "-----------------------------X2histogram",
    "name": "X2histogram",
    "description": "Generate a histogram for the specified column of a field.",
    "parameters": ...,
    "code": ...,
}
Xy2scatterplot.metadata = {
    "id": "--------------------------Xy2scatterplot",
    "name": "Xy2scatterplot",
    "description": "Generate a scatterplot for the specified two columns of a field.",
    "parameters": ...,
    "code": ...,
}
