import datetime as dt

import requests
import simplejson
import pandas as pd


class ExtractorAPI(object):
    LOCAL_URL_HOST = 'http://127.0.0.1:5000'
    REMOTE_URL_HOST = 'http://uor-geoserver.uksouth.cloudapp.azure.com/ext'
    GET_DATA_URL_TPL = '/dataset/{dataset}/get_data?{token}start_date={start_date}&end_date={end_date}&{variables}'
    DATE_FMT ='%Y-%m-%d-%H:%M:%S'

    def __init__(self, token=None, local=False, chatty=True):
        self.token = token
        if local:
            self.url_host = self.LOCAL_URL_HOST
            self.get_data_tpl = self.LOCAL_URL_HOST + self.GET_DATA_URL_TPL
        else:
            self.url_host = self.REMOTE_URL_HOST
            self.get_data_tpl = self.REMOTE_URL_HOST + self.GET_DATA_URL_TPL
        self._chatty = chatty

    def _say(self, msg):
        if self._chatty:
            print(msg)

    def _get_json(self, url):
        self._say(url)
        req = requests.get(url)
        json = simplejson.loads(req.content)
        return json

    def get_data(self, dataset, start_date, end_date, variables):
        assert dataset in self.datasets, 'dataset {} not in datasets'.format(dataset)
        assert start_date < end_date, 'start date must be before end date'

        variable_str = '&'.join(['var={}'.format(f) for f in variables])
        if self.token:
            token = 'token=' + self.token + '&'
        else:
            token = ''

        req_url = self.get_data_tpl.format(dataset=dataset,
                                           token=token,
                                           start_date=start_date.strftime(self.DATE_FMT),
                                           end_date=end_date.strftime(self.DATE_FMT),
                                           variables=variable_str)
        req = requests.get(req_url)
        json = simplejson.loads(req.content)
        df = pd.DataFrame(columns=json['header'], data=json['data'])
        return df

    def get_datasets(self):
        req_url = self.url_host + '/datasets.json'
        return self._get_json(req_url)['datasets']

    def get_dataset(self, name):
        req_url = self.url_host + '/dataset/' + name + '.json'
        return self._get_json(req_url)['dataset']

    def get_vars(self, name):
        req_url = self.url_host + '/dataset/' + name + '/vars.json'
        return self._get_json(req_url)

    def get_all_data(self):
        all_data = {}
        datasets = self.get_datasets()
        for dataset in datasets:
            all_data[dataset] = self.get_dataset(dataset)
        return all_data

