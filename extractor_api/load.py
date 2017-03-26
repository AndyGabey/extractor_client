import random
import datetime as dt

from extractor_api import ExtractorAPI, GetDataError


def random_load(argv):
    "Picks a random dataset based on the token, ask for random selection of data"
    token_name = argv[1]

    extapi = ExtractorAPI(token=token_name, chatty=False)

    # Pick a random dataset and get its info.
    # N.B. token's know which datasets they can be used for.
    token = extapi.get_token()
    dataset_names = token['datasets']
    dataset_name = random.choice(dataset_names)
    dataset = extapi.get_dataset(dataset_name)
    variables = dataset['variables']

    # Calculate a duration that's less than the token's max.
    max_dur = token['max_request_time_hours']
    req_dur = random.random() * max_dur
    req_duration = dt.timedelta(hours=req_dur)

    # Get the dataset start and end dates, and the total duration less how long 
    # the request is for.
    ds_start_date = dt.datetime.strptime(dataset['start_date'], extapi.DATE_FMT)
    ds_end_date = dt.datetime.strptime(dataset['end_date'], extapi.DATE_FMT)
    total_seconds = (ds_end_date - ds_start_date).total_seconds()
    total_seconds -= req_duration.total_seconds()

    # Get start and end dates.
    req_start_date = ds_start_date + dt.timedelta(seconds=int(random.random() * total_seconds))
    req_end_date = req_start_date + req_duration

    # Pick 2/3rds of the variables to return.
    varnames = [v['var'] for v in variables]
    req_vars = random.sample(varnames, int(2. * len(varnames) / 3))

    try:
        # Fire off request.
        df = extapi.get_data(dataset_name, req_start_date, req_end_date, req_vars)
        print('{0: <20}: {1} - {2}: Extracted {3} rows'.format(dataset_name, req_start_date, req_end_date, len(df)))
    except GetDataError as gde:
        # Something went wrong!
        for line in gde.message.content.split('\n'):
            if 'error_message' in line:
                break
        print('{0: <20}: FAILED: {1}: {2}'.format(dataset_name, gde, line))
    except Exception as e:
        # Something went badly wrong!
        print('{0: <20}: FAILED: {1}'.format(dataset_name, e))
