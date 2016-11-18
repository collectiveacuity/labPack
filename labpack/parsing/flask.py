__author__ = 'rcj1492'
__created__ = '2016.10'
__license__ = 'MIT'

'''
app.test_request_context(**kwargs):
# query_string=None,
# method='GET'
# input_stream=None
# content_type=None
# content_length=None
# errors_stream=None
# multithread=False,
# multiprocess=False
# run_once=False
# headers=None
# data=None
# environ_base=None
# environ_overrides=None
# charset='utf-8'
'''

def extract_request_details(request_object, session_object=None):

    '''
        a method for extracting request details from request and session objects

        NOTE:   method is also a placeholder funnel for future validation
                processes, request logging, request context building and
                counter-measures for the nasty web

    :param request_object: request object generated by flask from request route
    :param session_object: session object generated by flask from client cookie
    :return: dictionary with request details, status code
    '''

    request_details = {
        'errors': [],
        'status': 200,
        'session': {},
        'root': request_object.url_root,
        'route': request_object.path,
        'headers': {},
        'form': {},
        'params': {},
        'json': {},
        'data': ''
    }

# retrieve session details
    if session_object:
        for key, value in session_object.items():
            request_details['session'][key] = value

# automatically add header and query field data
    for key, value in request_object.headers.items():
        request_details['headers'][key] = value
    for key, value in request_object.args.items():
        request_details['params'][key] = value

# add data based upon type
    if request_object.is_json:
        try:
            json_details = request_object.get_json(silent=True)
            if isinstance(json_details, dict):
                request_details['json'] = json_details
        except:
                pass
    else:
        try:
            from base64 import b64encode
            request_details['data'] = b64encode(request_object.data).decode()
        except:
            pass
        try:
            for key, value in request_object.form.items():
                request_details['form'][key] = value
        except:
            pass

# TODO: handle non-json data parsing (such as by mimetype and request.files)
# TODO: check content type against buffer values
# TODO: status code and error handling

    return request_details

def validate_request_details(request_details, request_model):

    from jsonmodel.validators import jsonModel
    from jsonmodel.exceptions import InputValidationError

    title = 'validate_request_details'

# validate inputs
    if not isinstance(request_details, dict):
        raise TypeError('%s(request_details={...}) must be a dictionary.' % title)
    elif not isinstance(request_model, jsonModel):
        raise TypeError('%s(request_model=<...>) must be a %s object.' % (title, jsonModel.__class__))

# construct default status details
    status_details = {
        'code': 200,
        'error': ''
    }

# validate request details
    for key in request_model.schema.keys():
        if not key in request_details.keys():
            status_details['code'] = 400
            status_details['error'] = "request is missing a value for field '%s'" % key
            break
        try:
            object_title = "request field '%s'" % key
            request_model.validate(request_details[key], '.%s' % key, object_title)
        except InputValidationError as err:
            status_details['error'] = err.message.replace('\n',' ').lstrip()
            status_details['code'] = 400
            break

    return status_details

if __name__ == '__main__':
# work around for namespace collision
    from sys import path as sys_path
    sys_path.append(sys_path.pop(0))
    from flask import Flask, jsonify, request
    sys_path.insert(0, sys_path.pop())
    app = Flask(import_name=__name__)
    @app.route('/test')
    def test_route():
        return jsonify({'status':'ok'}), 200
    import json
    request_kwargs = {
        'content_type': 'application/json',
        'data': json.dumps({'test':'request'}).encode('utf-8'),
        'query_string': 'test=yes'
    }
    with app.test_request_context('/test', **request_kwargs):
        request_details = extract_request_details(request)
        print(request_details)