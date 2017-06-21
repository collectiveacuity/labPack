__author__ = 'rcj1492'
__created__ = '2016.11'
__license__ = 'MIT'

'''
PLEASE NOTE:    magic package requires the python-magic module.
                python-magic requires a number of C libraries to install.

(alpine):       apk add gcc
                apk add g++
                apk add libmagic
                pip install python-magic

(debian):       pip install python-magic

(macOS):        brew install libmagic
                pip install python-magic

(windows):      (32bit) http://gnuwin32.sourceforge.net/packages/file.htm
                http://downloads.sourceforge.net/gnuwin32/file-5.03-bin.zip
                (64bit) https://github.com/pidydx/libmagicwin64
                add dll files to path in systems settings
                copy magic and magic.mgc files to project path
                pip install python-magic

                magic_file='path/to/magic.mgc'
'''

# https://github.com/ahupp/python-magic

# https://docs.python.org/3.5/library/mimetypes.html#module-mimetypes

# https://www.iana.org/assignments/media-types/media-types.xhtml
# application_url = 'https://www.iana.org/assignments/media-types/application.csv'
# audio_url = 'https://www.iana.org/assignments/media-types/audio.csv'
# image_url = 'https://www.iana.org/assignments/media-types/image.csv'
# message_url = 'https://www.iana.org/assignments/media-types/message.csv'
# model_url = 'https://www.iana.org/assignments/media-types/model.csv'
# multipart_url = 'https://www.iana.org/assignments/media-types/multipart.csv'
# text_url = 'https://www.iana.org/assignments/media-types/text.csv'
# video_url = 'https://www.iana.org/assignments/media-types/video.csv'

# EXIFTOOL
# http://www.sno.phy.queensu.ca/~phil/exiftool/
# https://github.com/smarnach/pyexiftool

class labMagic(object):

    _class_fields = {
        'schema': {
            'magic_file': './magic.mgc',
            'mimetype_urls': {
                'httpd/conf/mime.types': 'https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types'
            },
            'file_path': '../test-audio.ogg',
            'file_url': 'https://pbs.twimg.com/profile_images/479475632158408704/Zelyz-xr_400x400.png'
        },
        'components': {
            '.magic_file': {
                'must_contain': [ 'magic\\.mgc$' ]
            }
        }
    }

    def __init__(self, magic_file=''):

        ''' initialization method for labMagic class

        :param magic_file: [optional] string with local path to magic.mgc file
        '''

        title = '%s.__init__' % self.__class__.__name__

    # construct class field model
        from jsonmodel.validators import jsonModel
        self.fields = jsonModel(self._class_fields)

    # validate inputs
        input_fields = {
            'magic_file': magic_file
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct magic method
        magic_kwargs = {
            'mime': True,
            'uncompress': True
        }
        from labpack.platforms.localhost import localhostClient
        sys_name = localhostClient().os.sysname
        if sys_name == 'Windows':
            if not magic_file:
                raise IndexError('%s(magic_file="...") is required on Windows systems.')
        import os
        if magic_file:
            if not os.path.exists(magic_file):
                raise ValueError('%s(magic_file=%s) is not a valid file path.' % (title, magic_file))
            magic_kwargs['magic_file'] = magic_file
        try:
        # workaround for module namespace conflict
            from sys import path as sys_path
            sys_path.append(sys_path.pop(0))
            import magic
            sys_path.insert(0, sys_path.pop())
            self.magic = magic.Magic(**magic_kwargs)
        except:
            raise Exception('\nmagiclab requires the python-magic module. try: pip install python-magic\npython-magic requires the C library libmagic. See documentation in labpack.parsing.magic.')

    # construct mimetypes method
        import mimetypes
        self.mimetypes = mimetypes.MimeTypes()

    # retrieve updates to mimetypes
        mimetype_urls = self.fields.schema['mimetype_urls']
        from labpack.storage.appdata import appdataClient
        mime_collection = appdataClient('Mime Types')
        mime_filter = mime_collection.conditional_filter([{-1:{'must_contain': ['mime.types']}}])
        mime_list = mime_collection.list(mime_filter)
        for key in mimetype_urls.keys():
            file_path = os.path.join(mime_collection.collection_folder, key)
            if key not in mime_list:
                file_dir = os.path.split(file_path)[0]
                if not os.path.exists(file_dir):
                    os.makedirs(file_dir)
                import requests
                try:
                    response = requests.get(mimetype_urls[key])
                except Exception:
                    from labpack.handlers.requests import handle_requests
                    request_kwargs = {'url': mimetype_urls[key]}
                    response_details = handle_requests(requests.Request(**request_kwargs))
                    print('magiclab attempted to retrieve latest mimetype registry resource at %s but ran into this non-fatal error: %s' % (mimetype_urls[key], response_details['error']))
                    break
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                    f.close()
            ext_map = mimetypes.read_mime_types(file_path)
            for key, value in ext_map.items():
                self.mimetypes.add_type(value, key)

    def analyze(self, file_path='', file_url='', byte_data=None):

        ''' a method to determine the mimetype and extension of a file from its byte data

        :param file_path: [optional] string with local path to file
        :param file_url: [optional] string with url of file
        :param byte_data: [optional] byte data from a file
        :return: dictionary with file details

        {
            'name': 'filename.ext',
            'mimetype': 'type/sub-type',
            'extension': '.ext'
        }
        '''

        title = '%s.analyze' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'file_path': file_path,
            'file_url': file_url
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)
        if byte_data:
            if not isinstance(byte_data, bytes):
                raise ValueError("%s(byte_data=b'...') must be byte data" % title)

    # construct empty type map
        file_details = {
            'name': '',
            'mimetype': '',
            'extension': ''
        }
        magic_results = None

    # analyze file
        if file_path:
            import os
            if not os.path.exists(file_path):
                raise ValueError('%s(file_path=%s) is not a valid path.' % (title, file_path))
            split_file = os.path.split(file_path)
            file_details['name'] = split_file[0]
            if len(split_file) > 1:
                file_details['name'] = split_file[1]
            magic_results = self.magic.from_file(file_path)

    # analyze url
        elif file_url:
            from urllib.parse import urlsplit
            url_path = urlsplit(file_url).path
            path_segments = url_path.split('/')
            file_details['name'] = path_segments[-1]
            import requests
            try:
                response = requests.get(file_url)
            except Exception:
                from labpack.handlers.requests import handle_requests
                response_details = handle_requests(requests.Request(url=file_url))
                raise ValueError('%s(file_url=%s) created this error: %s' % (title, file_url, response_details['error']))
            magic_results = self.magic.from_buffer(response.content)

    # analyze buffer
        elif byte_data:
            magic_results = self.magic.from_buffer(byte_data)

        else:
            raise IndexError('%s(...) requires either a file_path, file_url or byte_data argument' % title)

        if magic_results:
            file_details['mimetype'] = magic_results
            mime_results = self.mimetypes.guess_extension(magic_results)
            if mime_results:
                file_details['extension'] = mime_results

        return file_details
