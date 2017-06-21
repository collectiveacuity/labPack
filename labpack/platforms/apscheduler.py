__author__ = 'rcj1492'
__created__ = '2016.11'
__license__ = 'MIT'

'''
APScheduler Documentation
https://apscheduler.readthedocs.io/en/latest/index.html
'''

import requests

class apschedulerClient(object):

    _class_fields = {
        'schema': {
            'scheduler_url': 'http://127.0.0.1:5000',
            'id': 'launch:handle_request.1478291494.027648',
            'name': 'handle request with request kwargs',
            'function': 'launch:handle_request',
            'kwargs': {},
            'dt': 1478291565.372089,
            'interval': 10,
            'month': 12,
            'day': 31,
            'weekday': 6,
            'hour': 23,
            'minute': 59,
            'second': 59,
            'start': 1478291565.372089,
            'end': 1478291565.372089,
            'argument_filters': [ {
                '.id': {},
                '.function': {},
                '.name': {},
                '.dt': {},
                '.interval': {},
                '.month': {},
                '.day': {},
                '.weekday': {},
                '.hour': {},
                '.minute': {},
                '.second': {},
                '.start': {},
                '.end': {}
            } ]
        },
        'components': {
            '.scheduler_url': {
                'must_contain': [ '^https?://' ]
            },
            '.interval': {
                'integer_data': True
            },
            '.month': {
                'integer_data': True,
                'min_value': 1,
                'max_value': 12
            },
            '.day': {
                'integer_data': True,
                'min_value': 1,
                'max_value': 31
            },
            '.weekday': {
                'integer_data': True,
                'min_value': 0,
                'max_value': 6
            },
            '.hour': {
                'integer_data': True,
                'min_value': 0,
                'max_value': 23
            },
            '.minute': {
                'integer_data': True,
                'min_value': 0,
                'max_value': 59
            },
            '.second': {
                'integer_data': True,
                'min_value': 0,
                'max_value': 59
            }
        }
    }

    def __init__(self, scheduler_url, requests_handler=None):

        ''' initialization method for apschedulerClient class

        :param scheduler_url: string with url of scheduler service
        :param requests_handler: [optional] callable for handling requests errors
        '''

    # construct model
        from jsonmodel.validators import jsonModel
        self.fields = jsonModel(self._class_fields)

    # validate input
        object_title = '%s(scheduler_url=%s)' % (self.__class__.__name__, str(scheduler_url))
        self.url = self.fields.validate(scheduler_url, '.scheduler_url', object_title)

    # add request handler
        self.handler = requests_handler

    # construct job model
        job_schema = {
            'schema': {
                'id': 'launch:handle_request.1478291494.027648',
                'name': 'handle request with request kwargs',
                'function': 'launch:handle_request',
                'dt': 1478291565.372089,
                'interval': 10,
                'month': 12,
                'day': 31,
                'weekday': 6,
                'hour': 23,
                'minute': 59,
                'second': 59,
                'start': 1478291565.372089,
                'end': 1478291565.372089
            },
            'components': {
                '.interval': {
                    'integer_data': True
                },
                '.month': {
                    'integer_data': True,
                    'min_value': 1,
                    'max_value': 12
                },
                '.day': {
                    'integer_data': True,
                    'min_value': 1,
                    'max_value': 31
                },
                '.weekday': {
                    'integer_data': True,
                    'min_value': 0,
                    'max_value': 6
                },
                '.hour': {
                    'integer_data': True,
                    'min_value': 0,
                    'max_value': 23
                },
                '.minute': {
                    'integer_data': True,
                    'min_value': 0,
                    'max_value': 59
                },
                '.second': {
                    'integer_data': True,
                    'min_value': 0,
                    'max_value': 59
                }
            }
        }
        self.job_model = jsonModel(job_schema)

    def _get_request(self, url):

        try:
            response = requests.get(url=url)
        except Exception as err:
            if self.handler:
                request_kwargs = {
                    'method': 'GET',
                    'url': url
                }
                request_object = requests.Request(**request_kwargs)
                return self.handler(request_object)
            else:
                raise
        return response.json()

    def _post_request(self, url, json_kwargs):

        try:
            response = requests.post(url=url, json=json_kwargs)
        except Exception as err:
            if self.handler:
                request_kwargs = {
                    'method': 'POST',
                    'url': url,
                    'json': json_kwargs
                }
                request_object = requests.Request(**request_kwargs)
                return self.handler(request_object)
            else:
                raise
        return response.json()

    def _delete_request(self, url):

        try:
            response = requests.delete(url=url)
        except Exception as err:
            if self.handler:
                return self.handler(err)
            else:
                raise
        return response.status_code

    def _construct_details(self, raw):

        from labpack.records.time import labDT
        job_details = {}
        interval = 0
        for key, value in raw.items():
            if key == 'func':
                job_details['function'] = value
            elif key == 'weeks':
                interval += value * 604800
            elif key == 'days':
                interval += value * 86400
            elif key == 'hours':
                interval += value * 3600
            elif key == 'minutes':
                interval += value * 60
            elif key == 'seconds':
                interval += value
            elif key == 'run_date':
                job_details['dt'] = labDT.fromISO(value).epoch()
            elif key == 'day_of_week':
                job_details['weekday'] = int(value)
            elif key in ('month', 'day', 'hour', 'minute', 'second'):
                job_details[key] = int(value)
            elif key in ('next_run_time'):
                job_details[key] = labDT.fromISO(value).epoch()
            elif key == 'start_date':
                job_details['start'] = labDT.fromISO(value).epoch()
            elif key == 'end_date':
                job_details['end'] = labDT.fromISO(value).epoch()
            else:
                job_details[key] = value
        if interval:
            job_details['interval'] = interval

        return job_details

    def _construct_fields(self, id, function, dt=0.0, interval=0, month=None, day=None, weekday=None, hour=None, minute=None, second=None, args=None, kwargs=None, start=0.0, end=0.0, name=''):

        from datetime import datetime

    # determine interval fields
        weeks = None
        days = None
        hours = None
        minutes = None
        seconds = None
        if interval:
            weeks = interval // 604800
            remainder = interval % 604800
            days = remainder // 86400
            remainder = interval % 86400
            hours = remainder // 3600
            remainder = remainder % 3600
            minutes = remainder // 60
            seconds = remainder % 60

    # construct request fields
        json_kwargs = {
            'id': id,
            'func': function,
            'trigger': 'date'
        }
        if interval:
            json_kwargs['trigger'] = 'interval'
        if args:
            json_kwargs['args'] = args
        if kwargs:
            json_kwargs['kwargs'] = kwargs
        if name:
            json_kwargs['name'] = name
        if isinstance(weekday, int):
            json_kwargs['trigger'] = 'cron'
            json_kwargs['day_of_week'] = weekday
        if isinstance(month, int):
            json_kwargs['trigger'] = 'cron'
            json_kwargs['month'] = month
        if isinstance(day, int):
            json_kwargs['trigger'] = 'cron'
            json_kwargs['day'] = day
        if isinstance(hour, int):
            json_kwargs['trigger'] = 'cron'
            json_kwargs['hour'] = hour
        if isinstance(minute, int):
            json_kwargs['trigger'] = 'cron'
            json_kwargs['minute'] = minute
        if isinstance(second, int):
            json_kwargs['trigger'] = 'cron'
            json_kwargs['second'] = second
        if weeks:
            json_kwargs['weeks'] = weeks
        if days:
            json_kwargs['days'] = days
        if hours:
            json_kwargs['hours'] = hours
        if minutes:
            json_kwargs['minutes'] = minutes
        if seconds:
            json_kwargs['seconds'] = seconds
        if start:
            json_kwargs['start_date'] = datetime.utcfromtimestamp(start).isoformat()
        if end:
            json_kwargs['end_date'] = datetime.utcfromtimestamp(end).isoformat()
        if dt:
            json_kwargs['run_date'] = datetime.utcfromtimestamp(dt).isoformat()

        return json_kwargs

    def get_info(self):
        title = '%s.get_info' % self.__class__.__name__
        url = '%s/scheduler' % self.url
        return self._get_request(url)

    def list_jobs(self, argument_filters=None):

        '''
            a method to list jobs in the scheduler

        :param argument_filters: list of query criteria dictionaries for class argument keys
        :return: list of jobs (which satisfy the filters)

        NOTE:   query criteria architecture

                each item in the argument filters list must be a dictionary
                which is composed of one or more key names which represent the
                dotpath to a key in the job record to be queried with a value
                that is a dictionary of conditional operators used to test the
                value in the corresponding key in each record in the list of jobs.

                eg. argument_filters = [ { '.function': { 'must_contain': [ 'debug' ] } } ]

                this example filter looks in the function key of each job for a
                value which contains the characters 'debug'.

        NOTE:   the filter method uses a query filters list structure to represent
                the disjunctive normal form of a logical expression. a record is
                added to the results list if any query criteria dictionary in the
                list evaluates to true. within each query criteria dictionary, all
                declared conditional operators must evaluate to true.

                in this way, the argument_filters represents a boolean OR operator and
                each criteria dictionary inside the list represents a boolean AND
                operator between all keys in the dictionary.

        NOTE:   each query_criteria uses the architecture of query declaration in
                the jsonModel.query method

        the list of keys in each query_criteria is the same as the arguments for
        adding a job to the scheduler
        query_criteria = {
            '.id': {},
            '.function': {},
            '.name': {},
            '.dt': {},
            '.interval': {},
            '.month': {},
            '.day': {},
            '.weekday': {},
            '.hour': {},
            '.minute': {},
            '.second': {},
            '.start_date': {},
            '.end_date': {}
        }

        conditional operators for '.id', '.function', '.name':
            "byte_data": false,
            "discrete_values": [ "" ],
            "excluded_values": [ "" ],
            "greater_than": "",
            "less_than": "",
            "max_length": 0,
            "max_value": "",
            "min_length": 0,
            "min_value": "",
            "must_contain": [ "" ],
            "must_not_contain": [ "" ],
            "contains_either": [ "" ]

        conditional operators for '.dt', 'start', 'end':
            "discrete_values": [ 0.0 ],
            "excluded_values": [ 0.0 ],
            "greater_than": 0.0,
            "less_than": 0.0,
            "max_value": 0.0,
            "min_value": 0.0

        operators for '.interval', '.month', '.day', '.weekday', '.hour', '.minute', '.second':
            "discrete_values": [ 0 ],
            "excluded_values": [ 0 ],
            "greater_than": 0,
            "less_than": 0,
            "max_value": 0,
            "min_value": 0

        '''

        title = '%s.list_jobs' % self.__class__.__name__

    # validate inputs
        if argument_filters:
            self.fields.validate(argument_filters, '.argument_filters')

    # send request to get jobs
        url = '%s/scheduler/jobs' % self.url
        job_list = self._get_request(url)

    # construct filter function
        def query_function(**kwargs):
            job_details = {}
            for key, value in kwargs.items():
                if key in self.job_model.schema.keys():
                    job_details[key] = value
            for query_criteria in argument_filters:
                if self.job_model.query(query_criteria, job_details):
                    return True
            return False

    # construct empty list
        results_list = []

    # add refactored jobs to results list
        for job in job_list:
            job_details = self._construct_details(job)
            if argument_filters:
                if query_function(**job_details):
                    results_list.append(job_details)
            else:
                results_list.append(job_details)

        return results_list

    def add_date_job(self, id, function, args=None, kwargs=None, dt=0.0, name=''):

    # construct request fields
        title = '%s.add_date_job' % self.__class__.__name__
        url = '%s/scheduler/jobs' % self.url

    # validate inputs
        input_args = {
            'id': id,
            'function': function,
            'kwargs': kwargs,
            'dt': dt,
            'name': name
        }
        for key, value in input_args.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)
        if args:
            if not isinstance(args, list):
                raise ValueError('%s(args=[...] must be a list datatype.' % title)

    # construct request fields
        json_kwargs = self._construct_fields(id, function, dt=dt, args=args, kwargs=kwargs, name=name)

    # send post request
        response_details = self._post_request(url, json_kwargs)

        return self._construct_details(response_details)

    def add_interval_job(self, id, function, interval, args=None, kwargs=None, start=0.0, end=0.0, name=''):

    # construct request fields
        title = '%s.add_interval_job' % self.__class__.__name__
        url = '%s/scheduler/jobs' % self.url

    # validate inputs
        input_args = {
            'id': id,
            'function': function,
            'kwargs': kwargs,
            'interval': interval,
            'name': name,
            'start': start,
            'end': end
        }
        for key, value in input_args.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)
        if args:
            if not isinstance(args, list):
                raise ValueError('%s(args=[...] must be a list datatype.' % title)

    # validate start and end dates
        from time import time
        from datetime import datetime
        current_time = time()
        if start:
            if start < current_time:
                raise ValueError('%s(start=%s) must be an epoch datetime in the future.' % (title, start))
        if end:
            if end < current_time:
                raise ValueError('%s(end=%s) must be an epoch datetime in the future.' % (title, start))
        if start and end:
            if end < start:
                raise ValueError('%s(start=%s, end=%s) must have a start datetime after the end datetime.' % (title, start, end))

    # construct request fields
        json_kwargs = self._construct_fields(id, function, interval=interval, args=args, kwargs=kwargs, start=start, end=end, name=name)

    # send post request
        response_details = self._post_request(url, json_kwargs)

        return self._construct_details(response_details)

    def add_cron_job(self, id, function, month=None, day=None, weekday=None, hour=None, minute=None, second=None, args=None, kwargs=None, start=0.0, end=0.0, name=''):

    # construct request fields
        title = '%s.add_cron_job' % self.__class__.__name__
        url = '%s/scheduler/jobs' % self.url

    # validate normal inputs
        input_args = {
            'id': id,
            'function': function,
            'kwargs': kwargs,
            'name': name,
            'start': start,
            'end': end
        }
        for key, value in input_args.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)
        if args:
            if not isinstance(args, list):
                raise ValueError('%s(args=[...] must be a list datatype.' % title)

    # validate calendar inputs
        input_args = {
            'month': month,
            'day': day,
            'weekday': weekday,
            'hour': hour,
            'minute': minute,
            'second': second
        }
        for key, value in input_args.items():
            if value.__class__ != None.__class__:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)
        if weekday and (month or day):
            raise ValueError('%s(weekday=%s) cannot be declared along with month or day arguments.' % (title, str(weekday)))
        if month and day:
            if month in (4, 6, 9, 11):
                if day > 30:
                    raise ValueError('%s(month=%s) only has 30 days.' % (title, str(month)))
            elif month == 2:
                if day > 28:
                    raise ValueError('%s(month=%s) only has 28 days except on a leap year.' % (title, str(month)))

    # validate start and end dates
        from time import time
        from datetime import datetime
        current_time = time()
        if start:
            if start < current_time:
                raise ValueError('%s(start=%s) must be an epoch datetime in the future.' % (title, start))
        if end:
            if end < current_time:
                raise ValueError('%s(end=%s) must be an epoch datetime in the future.' % (title, end))
        if start and end:
            if end < start:
                raise ValueError('%s(start=%s, end=%s) must have a start datetime after the end datetime.' % (title, start, end))

    # construct request fields
        json_kwargs = self._construct_fields(id, function, month=month, day=day, weekday=weekday, hour=hour, minute=minute, second=second, args=args, kwargs=kwargs, start=start, end=end, name=name)

    # send post request
        response_details = self._post_request(url, json_kwargs)

        return self._construct_details(response_details)

    def delete_job(self, id):

    # construct request fields
        title = '%s.delete_jobs' % self.__class__.__name__

    # validate input
        object_title = '%s(id=%s)' % (title, str(id))
        self.fields.validate(id, '.id', object_title)

    # send delete request
        url = '%s/scheduler/jobs/%s' % (self.url, id)
        status_code = self._delete_request(url)

        return status_code