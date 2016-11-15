__author__ = 'rcj1492'
__created__ = '2016.11'
__license__ = 'MIT'

from labpack.platforms.apscheduler import apschedulerClient

if __name__ == '__main__':
    from labpack.records.settings import load_settings
    system_config = load_settings('../../cred/system.yaml')
    scheduler_url = 'http://%s:%s' % (system_config['system_ip_address'], system_config['scheduler_system_port'])
    scheduler_client = apschedulerClient(scheduler_url)
    scheduler_info = scheduler_client.get_info()
    assert scheduler_info['running']
    from time import time, sleep
    job_function = 'init:app.logger.debug'
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
        'kwargs': {'msg': 'Add interval job is working.'},
        'start': time() + 0.5,
        'end': time() + 10.5
    }
    interval_job = scheduler_client.add_interval_job(**interval_kwargs)
    cron_a_kwargs = {
        'id': '%s.%s' % (job_function, str(time())),
        'function': job_function,
        'kwargs': {'msg': 'Add nye cron job is working.'},
        'month': 12,
        'day': 31,
        'hour': 23,
        'minute': 59,
        'second': 59
    }
    cron_job_a = scheduler_client.add_cron_job(**cron_a_kwargs)
    cron_b_kwargs = {
        'id': '%s.%s' % (job_function, str(time())),
        'function': job_function,
        'kwargs': {'msg': 'Add ny cron job is working.'},
        'month': 1,
        'day': 1,
        'hour': 0,
        'minute': 0,
        'second': 0
    }
    cron_job_b = scheduler_client.add_cron_job(**cron_b_kwargs)
    cron_c_kwargs = {
        'id': '%s.%s' % (job_function, str(time())),
        'function': job_function,
        'kwargs': {'msg': 'Add weekday cron job is working.'},
        'weekday': 5,
        'hour': 5,
        'minute': 5,
        'second': 5
    }
    cron_job_c = scheduler_client.add_cron_job(**cron_c_kwargs)
    try:
        interval_filter = [{'.id': {'must_contain': [ 'app\\.logger']}, '.function': {'must_contain': [ 'debug' ]}, '.interval': { 'discrete_values': [1] }}]
        interval_list = scheduler_client.list_jobs(argument_filters=interval_filter)
        dt_filter = [{'.dt': { 'min_value': time() }}]
        dt_list = scheduler_client.list_jobs(argument_filters=dt_filter)
        cron_filter = [{'.weekday': { 'discrete_values': [ 5 ]}}]
        cron_list = scheduler_client.list_jobs(argument_filters=cron_filter)
        print(interval_list)
        print(dt_list)
        print(cron_list)
    except:
        pass
    sleep(2)
    job_list = scheduler_client.list_jobs()
    assert job_list
    id_list = [ interval_kwargs['id'], date_kwargs['id'], cron_a_kwargs['id'], cron_b_kwargs['id'], cron_c_kwargs['id'] ]
    for job in job_list:
        if job['id'] in id_list:
            assert scheduler_client.delete_job(job['id']) == 204