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
            'second': 59
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

    # construct model
        from jsonmodel.validators import jsonModel
        self.fields = jsonModel(self._class_fields)

    # validate input
        object_title = '%s(scheduler_url=%s)' % (self.__class__.__name__, str(scheduler_url))
        self.url = self.fields.validate(scheduler_url, '.scheduler_url', object_title)

    # add request handler
        self.handler = requests_handler

    def _get_request(self, url, title):

        try:
            response = requests.get(url=url)
        except Exception as err:
            if self.handler:
                return self.handler(err, title)
            else:
                raise
        return response.json()

    def _post_request(self, url, json_kwargs, title):

        try:
            response = requests.post(url=url, json=json_kwargs)
        except Exception as err:
            if self.handler:
                return self.handler(err, title)
            else:
                raise
        return response.json()

    def _delete_request(self, url, title):

        try:
            response = requests.delete(url=url)
        except Exception as err:
            if self.handler:
                return self.handler(err, title)
            else:
                raise
        return response.status_code

    def get_info(self):
        title = '%s.get_info' % self.__class__.__name__
        url = '%s/scheduler' % self.url
        return self._get_request(url, title)

    def list_jobs(self):
        title = '%s.list_jobs' % self.__class__.__name__
        url = '%s/scheduler/jobs' % self.url
        return self._get_request(url, title)

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
        json_kwargs = {
            'id': id,
            'func': function,
            'trigger': 'date'
        }
        if args:
            json_kwargs['args'] = args
        if kwargs:
            json_kwargs['kwargs'] = kwargs
        if dt:
            from datetime import datetime
            json_kwargs['run_date'] = datetime.utcfromtimestamp(dt).isoformat()
        if name:
            json_kwargs['name'] = name

    # send post request
        return self._post_request(url, json_kwargs, title)

    def add_interval_job(self, id, function, interval, args=None, kwargs=None, name=''):

    # construct request fields
        title = '%s.add_interval_job' % self.__class__.__name__
        url = '%s/scheduler/jobs' % self.url

    # validate inputs
        input_args = {
            'id': id,
            'function': function,
            'kwargs': kwargs,
            'interval': interval,
            'name': name
        }
        for key, value in input_args.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)
        if args:
            if not isinstance(args, list):
                raise ValueError('%s(args=[...] must be a list datatype.' % title)

    # determine interval fields
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
            'trigger': 'interval'
        }
        if args:
            json_kwargs['args'] = args
        if kwargs:
            json_kwargs['kwargs'] = kwargs
        if name:
            json_kwargs['name'] = name
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

    # send post request
        return self._post_request(url, json_kwargs, title)

    def add_cron_job(self, id, function, month=None, day=None, weekday=None, hour=None, minute=None, second=None, args=None, kwargs=None, name=''):

    # construct request fields
        title = '%s.add_cron_job' % self.__class__.__name__
        url = '%s/scheduler/jobs' % self.url

    # validate normal inputs
        input_args = {
            'id': id,
            'function': function,
            'kwargs': kwargs,
            'name': name
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

    # construct request fields
        json_kwargs = {
            'id': id,
            'func': function,
            'trigger': 'cron'
        }
        if args:
            json_kwargs['args'] = args
        if kwargs:
            json_kwargs['kwargs'] = kwargs
        if name:
            json_kwargs['name'] = name
        if weekday:
            json_kwargs['day_of_week'] = weekday
        if month:
            json_kwargs['month'] = month
        if day:
            json_kwargs['day'] = day
        if hour:
            json_kwargs['hour'] = hour
        if minute:
            json_kwargs['minute'] = minute
        if second:
            json_kwargs['second'] = second

    # send post request
        return self._post_request(url, json_kwargs, title)

    def delete_job(self, id):

    # construct request fields
        title = '%s.delete_jobs' % self.__class__.__name__

    # validate input
        object_title = '%s(id=%s)' % (title, str(id))
        self.fields.validate(id, '.id', object_title)

    # send delete request
        url = '%s/scheduler/jobs/%s' % (self.url, id)
        return self._delete_request(url, title)

if __name__ == '__main__':
    from labpack.records.settings import load_settings
    system_config = load_settings('../../../cred/system.yaml')
    scheduler_url = 'http://%s:%s' % (system_config['system_ip_address'], system_config['scheduler_system_port'])
    scheduler_client = apschedulerClient(scheduler_url)
    scheduler_info = scheduler_client.get_info()
    assert scheduler_info['running']
    from time import time, sleep
    job_function = 'launch:app.logger.debug'
    date_kwargs = {
        'id': '%s.%s' % (job_function, str(time())),
        'function': job_function,
        'dt': time() + 2,
        'kwargs': { 'msg': 'Add date job is working.'}
    }
    date_job = scheduler_client.add_date_job(**date_kwargs)
    interval_kwargs = {
        'id': '%s.%s' % (job_function, str(time())),
        'function': job_function,
        'interval': 1,
        'kwargs': {'msg': 'Add interval job is working.'}
    }
    interval_job = scheduler_client.add_interval_job(**interval_kwargs)
    sleep(2)
    job_list = scheduler_client.list_jobs()
    assert job_list
    for job in job_list:
        if job['id'] == interval_kwargs['id']:
            assert scheduler_client.delete_job(job['id']) == 204
    cron_kwargs = {
        'id': '%s.%s' % (job_function, str(time())),
        'function': job_function,
        'kwargs': {'msg': 'Add nye cron job is working.'},
        'month': 12,
        'day': 31,
        'hour': 23,
        'minute': 59,
        'second': 59
    }
    cron_job_a = scheduler_client.add_cron_job(**cron_kwargs)
    job_list = scheduler_client.list_jobs()
    assert job_list
    for job in job_list:
        if job['id'] == cron_kwargs['id']:
            assert scheduler_client.delete_job(job['id']) == 204
    cron_kwargs = {
        'id': '%s.%s' % (job_function, str(time())),
        'function': job_function,
        'kwargs': {'msg': 'Add ny cron job is working.'},
        'month': 1,
        'day': 1,
        'hour': 0,
        'minute': 0,
        'second': 0
    }
    cron_job_b = scheduler_client.add_cron_job(**cron_kwargs)
    job_list = scheduler_client.list_jobs()
    assert job_list
    for job in job_list:
        if job['id'] == cron_kwargs['id']:
            assert scheduler_client.delete_job(job['id']) == 204
    cron_kwargs = {
        'id': '%s.%s' % (job_function, str(time())),
        'function': job_function,
        'kwargs': {'msg': 'Add weekday cron job is working.'},
        'weekday': 5,
        'hour': 5,
        'minute': 5,
        'second': 5
    }
    cron_job_c = scheduler_client.add_cron_job(**cron_kwargs)
    job_list = scheduler_client.list_jobs()
    assert job_list
    for job in job_list:
        if job['id'] == cron_kwargs['id']:
            assert scheduler_client.delete_job(job['id']) == 204