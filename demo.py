import datetime as dt

import pylab as plt

from extractor_api import ExtractorAPI


if __name__ == '__main__':
    xtapi = ExtractorAPI()
    xtapi.connect()
    print(xtapi.datasets)
    df = xtapi.get_data('5min_Level1', dt.datetime(2015, 1, 1), dt.datetime(2015, 1, 5), ['Tw'])
    plt.plot(df.values[:, 1])
    plt.show()
