import datetime as dt

import pylab as plt

from extractor_api import ExtractorAPI


if __name__ == '__main__':
    extapi = ExtractorAPI(token='t4')
    df = extapi.get_data('5min_Level1', dt.datetime(2015, 1, 1), dt.datetime(2015, 1, 1, 5), ['Tw'])
    #plt.plot(df.values[:, 1])
    #plt.show()
