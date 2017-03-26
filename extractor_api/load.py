import random
import datetime as dt

from extractor_api import ExtractorAPI


def random_load(argv):
    token = argv[1]
    dataset_name = argv[2]
    year = argv[3]

    doy = random.randint(1, 100)

    hours = random.randint(0, 23)
    minutes = random.randint(0, 59)

    start_date = dt.datetime.strptime('{0} {1:03d}'.format(year, doy), '%Y %j')
    start_date += dt.timedelta(hours=hours, minutes=minutes)

    dur_days = random.randint(0, 0)
    dur_hours = random.randint(0, 23)
    dur_minutes = random.randint(0, 59)
    duration = dt.timedelta(days=dur_days, hours=dur_hours, minutes=dur_minutes)

    end_date = start_date + duration

    extapi = ExtractorAPI(token=token, chatty=False)
    variables = extapi.get_dataset(dataset_name)['variables']
    varnames = [v['var'] for v in variables]
    req_vars = random.sample(varnames, len(varnames) / 2)

    try:
        df = extapi.get_data(dataset_name, start_date, end_date, req_vars)
        print('{} - {}: Extracted {} rows'.format(start_date, end_date, len(df)))
    except Exception as e:
        print(e)
        print(e.message.content)
