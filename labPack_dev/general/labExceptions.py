__author__ = 'rcj1492'
__created__ = '2015.09'

class ConnectionTimeout(Exception):
    def __init__(self, message='', errors=None):
        text = '\nTimeout trying to connect to %s' % message
        super(ConnectionTimeout, self).__init__(text)
        self.errors = errors

# try:
#     self.connection.put_item(**kw_args)
# except Exception as ClientError:
#     if ClientError.args[0].find('ConditionalCheckFailedException'):
#         print('[WARNING]: Item with primary key "%s" in table "%s" already exists. Add item aborted.' % (item_dict[p_key], table_name))
#     else:
#         raise DDBConnectionError('addItem')
