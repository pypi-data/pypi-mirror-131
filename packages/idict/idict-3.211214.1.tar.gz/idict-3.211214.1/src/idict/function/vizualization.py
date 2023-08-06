import numpy
import numpy as np
import pandas


def X2histogram(col=0, input="X", output="histogram", **kwargs):
    """
    >>> import numpy as np
    >>> X = np.array([[0, 2.1, 1.6], [3.2, 3, 2], [8, 7, 3]])
    >>> X2histogram(X=X, col=1)
    {'histogram': [{'x': '(1.1, 1.59]', 'count': 0}, {'x': '(1.59, 2.08]', 'count': 0}, {'x': '(2.08, 2.57]', 'count': 1}, {'x': '(2.57, 3.06]', 'count': 1}, {'x': '(3.06, 3.55]', 'count': 0}, {'x': '(3.55, 4.04]', 'count': 0}, {'x': '(4.04, 4.53]', 'count': 0}, {'x': '(4.53, 5.02]', 'count': 0}, {'x': '(5.02, 5.51]', 'count': 0}, {'x': '(5.51, 6.0]', 'count': 0}, {'x': '(6.0, 6.49]', 'count': 0}, {'x': '(6.49, 6.98]', 'count': 0}, {'x': '(6.98, 7.47]', 'count': 1}, {'x': '(7.47, 7.96]', 'count': 0}], '_history': Ellipsis}
    >>> from idict import idict
    >>> from idict.function.dataset import df2Xy
    >>> d = idict.fromtoy(output_format="df") >> df2Xy >> X2histogram
    >>> d.histogram
    [{'x': '(-0.9, 2.2]', 'count': 8}, {'x': '(2.2, 5.3]', 'count': 6}, {'x': '(5.3, 8.4]', 'count': 3}, {'x': '(8.4, 11.5]', 'count': 2}, {'x': '(11.5, 14.6]', 'count': 0}, {'x': '(14.6, 17.7]', 'count': 0}, {'x': '(17.7, 20.8]', 'count': 0}, {'x': '(20.8, 23.9]', 'count': 0}, {'x': '(23.9, 27.0]', 'count': 0}, {'x': '(27.0, 30.1]', 'count': 0}]
    """
    from pandas import DataFrame

    X = kwargs[input]
    idxs = X.iloc[:, col] if isinstance(X, DataFrame) else X[:, col]
    cut = list(map(float, idxs))
    maximum = max(cut)
    minimum = min(cut)
    step = (maximum - minimum) / 10
    ranges = np.arange(minimum - 1, maximum + 1, step)

    df = pandas.DataFrame(cut)
    df2 = df.groupby(pandas.cut(cut, ranges)).count()
    result = [{"x": str(k), "count": v} for k, v in df2.to_dict()[0].items()]
    return {output: result, "_history": ...}


def Xy2scatterplot(colx=0, coly=1, Xin="X", yin="y", output="scatterplot", **kwargs):
    """
    >>> import numpy as np
    >>> X = np.array([[0, 2.1, 1.6], [3.2, 3, 2], [8, 7, 3]])
    >>> y = np.array([2, 1.1, 3.6])
    >>> Xy2scatterplot(X=X, y=y, colx=1, coly=2)
    {'scatterplot': [{'id': 1.1, 'data': [{'x': 3.0, 'y': 2.0}]}, {'id': 2.0, 'data': [{'x': 2.1, 'y': 1.6}]}, {'id': 3.6, 'data': [{'x': 7.0, 'y': 3.0}]}], '_history': Ellipsis}
    >>> from idict import idict
    >>> from idict.function.dataset import df2Xy
    >>> d = idict.fromtoy(output_format="df") >> df2Xy >> Xy2scatterplot
    >>> d.scatterplot
    [{'id': 0, 'data': [{'x': 5.1, 'y': 6.4}, {'x': 6.1, 'y': 3.6}, {'x': 3.1, 'y': 2.5}, {'x': 9.1, 'y': 3.5}, {'x': 9.1, 'y': 7.2}, {'x': 7.1, 'y': 6.6}, {'x': 2.1, 'y': 0.1}, {'x': 5.1, 'y': 4.5}, {'x': 1.1, 'y': 3.2}, {'x': 3.1, 'y': 2.5}]}, {'id': 1, 'data': [{'x': 1.1, 'y': 2.5}, {'x': 1.1, 'y': 3.5}, {'x': 4.7, 'y': 4.9}, {'x': 8.3, 'y': 2.9}, {'x': 2.5, 'y': 4.5}, {'x': 0.1, 'y': 4.3}, {'x': 0.1, 'y': 4.0}, {'x': 31.1, 'y': 4.7}, {'x': 2.2, 'y': 8.5}, {'x': 1.1, 'y': 8.5}]}]
    """
    from pandas import DataFrame

    X = kwargs[Xin]
    y = kwargs[yin]
    result = []
    for m in numpy.unique(y):
        inner = []
        for k in range(len(X)):
            left = m if isinstance(m, str) else str(float(m))
            if isinstance(y[k], str):
                right = y[k]
            else:
                right = str(float(y[k]))
            if left == right:
                inner.append(
                    {
                        "x": float(X.iloc[k, colx] if isinstance(X, DataFrame) else X[k, colx]),
                        "y": float(X.iloc[k, coly] if isinstance(X, DataFrame) else X[k, coly]),
                    }
                )
        result.append({"id": m, "data": inner})
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
