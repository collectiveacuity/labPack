__author__ = 'rcj1492'
__created__ = '2017.04'
__license__ = 'MIT'

'''
PLEASE NOTE:    watson package requires watson-developer-cloud, moviepy 
                and ffmpy module along with ffmpeg C dependency

(install)       pip install watson-developer-cloud
                pip install moviepy
                pip install ffmpy
                
                python -m imageio.plugins.ffmpeg.download
                 - or -
                from imageio.plugins import ffmpeg
                ffmpeg.download()
'''

from labpack import __team__, __module__
try:
    from watson_developer_cloud.speech_to_text_v1 import SpeechToTextV1
    from watson_developer_cloud.text_to_speech_v1 import TextToSpeechV1
    from watson_developer_cloud import WatsonException
except:
    import sys
    print('watson package requires watson-cloud-developer module and ffmpeg dependencies.')
    sys.exit(1)

# TODO watson text to speech methods

class watsonSpeechClient(object):

    ''' 
        a class of methods to convert speech to text using IBM Watson api 
    
        https://console.ng.bluemix.net/catalog/services/text-to-speech
    '''

    _class_fields = {
        'schema': {
            'auth_endpoint': 'https://stream.watsonplatform.net/authorization/api/v1',
            'api_endpoint': 'https://stream.watsonplatform.net/speech-to-text/api/v1',
            'service_username': 'a32559de-1ecf-11e7-bc7c-10604bdb70a4',
            'service_password': 'IhE1AP2PmpBQ',
            'file_path': 'data/watson_test.ogg',
            'clip_length': 10,
            'file_url': 'https://justsomeaudioclips.com/watson_test.wav',
            'audio_mimetype': 'audio/ogg',
            'new_mimetype': 'audio/ogg',
            'audio_extensions': {
                '.+\\.flac$': { 'mimetype': 'audio/flac', 'extension': '.flac' },
                '.+\\.l16$': { 'mimetype': 'audio/l16', 'extension': '.l16' },
                '.+\\.wav$': { 'mimetype': 'audio/wav', 'extension': '.wav' },
                '.+\\.ogg$': { 'mimetype': 'audio/ogg', 'extension': '.ogg' },
                '.+\\.mulaw$': { 'mimetype': 'audio/mulaw', 'extension': '.mulaw' },
                '.+\\.au$': { 'mimetype': 'audio/basic', 'extension': '.au' },
                '.+\\.snd$': { 'mimetype': 'audio/basic', 'extension': '.snd' }
            }
        },
        'components': {
            '.audio_mimetype': {
                'discrete_values': []
            },
            '.clip_length': {
                'integer_data': True,
                'min_value': 1
            }
        }
    }

    def __init__(self, service_username, service_password, requests_handler=None, magic_file=''):

        title = '%s.__init__' % self.__class__.__name__

    # construct class field model
        from jsonmodel.validators import jsonModel
        for key, value in self._class_fields['schema']['audio_extensions'].items():
            self._class_fields['components']['.audio_mimetype']['discrete_values'].append(value['mimetype'])
        self.fields = jsonModel(self._class_fields)

    # validate inputs
        input_fields = {
            'service_username': service_username,
            'service_password': service_password
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)

    # define class properties
        self.username = service_username
        self.password = service_password

    # construct watson client
        self.client = SpeechToTextV1(username=self.username, password=self.password)

    # construct handlers
        self.requests_handler = requests_handler

    # construct magic format checker
        self.magic = None
        if magic_file:
            from labpack.parsing.magic import labMagic
            self.magic = labMagic(magic_file)

    # import validate extension
        from labpack.parsing.regex import validate_extension
        self._validate_extension = validate_extension

    def _get_data(self, file_url, file_name='', method_title='', argument_title=''):

        ''' a helper method to retrieve data buffer for a file url

        :param file_url: string with url to file
        :param file_name: [optional] string with name to affix to file buffer
        :param method_title: [optional] string with name of class method calling
        :param argument_title: [optional] string with name of method argument key
        :return: byte data buffer with file data
        '''

        # https://docs.python.org/3/library/io.html#io.BytesIO

        import io
        import requests

    # fill empty values
        if not file_name:
            file_name = 'file'
        if not method_title:
            method_title = '%s._get_data' % self.__class__.__name__
        if not argument_title:
            argument_title = 'file_url'

    # request file from url
        try:
            remote_file = requests.get(file_url)
        except requests.exceptions.ConnectionError as err:
            if self.requests_handler:
                return self.requests_handler(err)
            else:
                raise
        except:
            raise ValueError('%s(%s=%s) is not a valid url.' % (method_title, argument_title, file_url))

    # add contents to buffer
        file_buffer = io.BytesIO(remote_file.content)
        file_buffer.name = '%s' % file_name

        return file_buffer

    def _create_folder(self):

        ''' a helper method for creating a temporary audio clip folder '''

    # import dependencies
        import os
        from labpack.platforms.localhost import localhostClient
        from labpack.records.id import labID

    # create folder in user app data
        record_id = labID()
        collection_name = 'Watson Speech2Text'
        localhost_client = localhostClient()
        app_folder = localhost_client.app_data(org_name=__team__, prod_name=__module__)
        if localhost_client.os in ('Linux', 'FreeBSD', 'Solaris'):
            collection_name = collection_name.replace(' ', '-').lower()
        collection_folder = os.path.join(app_folder, collection_name)
        clip_folder = os.path.join(collection_folder, record_id.id24)
        if not os.path.exists(clip_folder):
            os.makedirs(clip_folder)

        return clip_folder

    def _transcribe_files(self, file_list, file_mimetype):

        ''' a helper method for multi-processing file transcription '''

    # import dependencies
        import queue
        from threading import Thread

    # define multithreading function
        def _recognize_file(file_path, file_mimetype, queue):

            details = {
                'error': '',
                'results': []
            }

            file_data = open(file_path, 'rb')
            try:
                transcript = self.client.recognize(file_data, file_mimetype, continuous=True)
                if transcript['results']:
                    for result in transcript['results']:
                        details['results'].append(result['alternatives'][0])
            except Exception as err:
                details['error'] = err

            queue.put(details)

    # construct queue
        q = queue.Queue()

    # send clips to watson for transcription in separate threads
        threads = []
        for file in file_list:
            watson_job = Thread(target=_recognize_file, args=(file, file_mimetype, q))
            watson_job.start()
            threads.append(watson_job)

    # wait for threads to end
        for t in threads:
            t.join()

    # construct result
        transcript_details = {
            'error': '',
            'segments': []
        }
        for i in range(len(file_list)):
            job_details = q.get()
            if job_details['error']:
                transcript_details['error'] = job_details['error']
            transcript_details['segments'].extend(job_details['results'])

        return transcript_details

    def convert_audio(self, file_path, new_mimetype, overwrite=False):

        '''
            a method to convert an audio file into a different codec
            
        :param file_path: string with path to file on localhost 
        :param new_mimetype: string with mimetype for new file
        :param overwrite: [optional] boolean to overwrite existing file
        :return: string with path to new file on localhost
        
            SEE: https://github.com/Ch00k/ffmpy
        '''

        title = '%s.convert_audio' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'file_path': file_path,
            'new_mimetype': new_mimetype
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)

    # retrieve file extension
        new_extension = ''
        mimetype_list = []
        mime_arg = '%s(new_mimetype=%s)' % (title, new_mimetype)
        for key, value in self.fields.schema['audio_extensions'].items():
            mimetype_list.append(value['mimetype'])
            if value['mimetype'] == new_mimetype:
                new_extension = value['extension']
                break
        if not new_extension:
            raise ValueError('%s must be one of %s mimetypes' % (mime_arg, mimetype_list))

    # import dependencies
        from os import path
        import ffmpy

    # validate existence of file
        file_arg = '%s(file_path=%s)' % (title, file_path)
        if not path.exists(file_path):
            raise ValueError('%s is not a valid path', file_arg)

    # construct new file
        file_name, file_extension = path.splitext(file_path)
        output_path = file_name + new_extension

    # construct inputs
        ffmpeg_kwargs = {
            'inputs': {file_path: None},
            'outputs': {output_path: None},
            'global_options': [ '-v error']
        }
        if overwrite:
            ffmpeg_kwargs['global_options'].append('-y')
        ffmpeg_client = ffmpy.FFmpeg(**ffmpeg_kwargs)

    # run conversion
        ffmpeg_client.run()

        return output_path

    def transcribe_file(self, file_path, clip_length=10, compress=True):

        '''
            a method to transcribe the text from an audio file
        
        EXAMPLE: https://github.com/dannguyen/watson-word-watcher
        
        :param file_path: string with path to audio file on localhost
        :param clip_length: [optional] integer with seconds to divide clips into
        :param compress: [optional] boolean to convert file to audio/ogg
        :return: dictionary with transcribed text segments in 'segments' key
        '''

        title = '%s.transcribe_file' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'file_path': file_path,
            'clip_length': clip_length
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)

    # run conversion
        import os
        if compress:
            file_name, file_extension = os.path.splitext(file_path)
            if file_extension != '.ogg':
                file_path = self.convert_audio(file_path, 'audio/ogg', True)

    # construct empty file details
        file_details = {
            'name': '',
            'mimetype': '',
            'extension': ''
        }

    # retrieve file name
        file_arg = '%s(file_path=%s)' % (title, str(file_path))
        split_file = os.path.split(file_path)
        file_details['name'] = split_file[0]
        if len(split_file) > 1:
            file_details['name'] = split_file[1]
        if not file_details['name']:
            raise ValueError('%s must have a file name.' % file_arg)

    # validate file extension
        ext_kwargs = {
            'file_name': file_details['name'],
            'extension_map': self.fields.schema['audio_extensions'],
            'method_title': title,
            'argument_title': file_path
        }
        regex_details = self._validate_extension(**ext_kwargs)
        file_details.update(**regex_details)

    # retrieve byte data
        if not os.path.exists(file_path):
            raise ValueError('%s is not a valid file path.' % file_arg)

    # validate file mimetype
        if self.magic:
            magic_details = self.magic.analyze(file_path)
            mimetype_text = file_details['mimetype'][6:]
            if mimetype_text not in magic_details['mimetype']:
                raise ValueError('%s byte data mimetype %s does not match %s file extension.' % (file_arg, magic_details['mimetype'], file_details['extension']))

    # import dependencies
        from math import ceil
        from moviepy.editor import AudioFileClip

    # open audio file
        audio = AudioFileClip(file_path)
        audio_duration = audio.duration

    # construct list of files to transcribe
        file_list = []
        if audio_duration < clip_length:
            file_list.append(file_path)
        else:
    # create temporary audio files
            clip_folder = self._create_folder()
            count = 0
            t_start = 0
            while t_start < audio_duration:
                t_end = t_start + clip_length
                if t_end > audio_duration:
                    t_end = ceil(audio_duration)
                    segment = audio.subclip(t_start)
                else:
                    segment = audio.subclip(t_start, t_end)
                clip_name = 'audio%s.%s' % (count, file_details['extension'])
                clip_path = os.path.join(clip_folder, clip_name)
                segment.write_audiofile(clip_path, verbose=False)
                file_list.append(clip_path)
                count += 1
                t_start = t_end

    # run file transcription method
        transcription_result = self._transcribe_files(file_list, file_details['mimetype'])

    # remove temp files
        if len(file_list) > 1:
            from labpack.records.settings import remove_settings
            for file in file_list:
                remove_settings(file, remove_dir=True)

        return transcription_result

    def transcribe_url(self, file_url, clip_length=None, compress=True):

        '''
            a method to transcribe the text from an audio url

        :param file_path: string with url to audio file on web
        :param clip_length: [optional] integer with seconds to divide clips into
        :param compress: [optional] boolean to convert file to audio/ogg
        :return: dictionary with transcribed text segments in 'segments' key
        '''

        title = '%s.transcribe_url' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'file_url': file_url,
        }
        if clip_length is not None:
            input_fields['clip_length'] = clip_length
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)

    # construct empty file details
        file_details = {
            'name': '',
            'mimetype': '',
            'extension': ''
        }

    # retrieve file name
        from urllib.parse import urlsplit
        file_arg = '%s(file_url=%s)' % (title, str(file_url))
        url_path = urlsplit(file_url).path
        path_segments = url_path.split('/')
        file_details['name'] = path_segments[-1]
        if not file_details['name']:
            raise ValueError('%s must have a file name.' % file_arg)

    # validate file extension
        ext_kwargs = {
            'file_name': file_details['name'],
            'extension_map': self.fields.schema['audio_extensions'],
            'method_title': title,
            'argument_title': 'file_url'
        }
        file_details = self._validate_extension(**ext_kwargs)

    # retrieve file data
        file_buffer = self._get_data(file_url, file_details['name'], title, 'file_url')
        if isinstance(file_buffer, dict):
            raise Exception(str(file_buffer))

    # validate file mimetype
        if self.magic:
            file_data = file_buffer.getvalue()
            magic_details = self.magic.analyze(byte_data=file_data)
            mimetype_text = file_details['mimetype'][6:]
            if mimetype_text not in magic_details['mimetype']:
                raise ValueError('%s byte data mimetype %s does not match %s file extension.' % (file_arg, magic_details['mimetype'], file_details['extension']))

    # construct default return
        transcript_details = {
            'error': '',
            'segments': []
        }

    # transcribe entire buffer
        if clip_length is None:
            try:
                file_data = file_buffer.getvalue()
                transcript = self.client.recognize(file_data, file_details['mimetype'], continuous=True)
                if transcript['results']:
                    for result in transcript['results']:
                        transcript_details['segments'].append(result['alternatives'][0])
            except Exception as err:
                transcript_details['error'] = err

    # save buffer to disk, segment and transcribe in multiple threads
        else:
            import os
            from time import sleep
            from math import ceil
            from moviepy.editor import AudioFileClip

        # save buffer to disk
            clip_folder = self._create_folder()
            full_name = 'audio_full.%s' % file_details['extension']
            full_path = os.path.join(clip_folder, full_name)
            with open(full_path, 'wb') as f:
                f.write(file_buffer.getvalue())
                f.close()

        # convert file
            if compress:
                file_name, file_extension = os.path.splitext(full_path)
                if file_extension != '.ogg':
                    full_path = self.convert_audio(full_path, 'audio/ogg', True)
                    file_details = {
                        'name': 'audio_full.ogg',
                        'extension': '.ogg',
                        'mimetype': 'audio/ogg'
                    }

        # open audio file
            count = 0
            retry_count = 10
            while True:
                try:
                    audio = AudioFileClip(full_path)
                    break
                except PermissionError:
                    sleep(.05)
                    count += 1
                    if count > retry_count:
                        raise
            audio_duration = audio.duration

        # construct list of files to transcribe
            file_list = []
            if audio_duration < clip_length:
                file_list.append(full_path)
            else:

        # create temporary audio files
                count = 0
                t_start = 0
                while t_start < audio_duration:
                    t_end = t_start + clip_length
                    if t_end > audio_duration:
                        t_end = ceil(audio_duration)
                        segment = audio.subclip(t_start)
                    else:
                        segment = audio.subclip(t_start, t_end)
                    clip_name = 'audio%s.%s' % (count, file_details['extension'])
                    clip_path = os.path.join(clip_folder, clip_name)
                    segment.write_audiofile(clip_path, verbose=False)
                    file_list.append(clip_path)
                    count += 1
                    t_start = t_end

        # run file transcription method
            transcript_details = self._transcribe_files(file_list, file_details['mimetype'])

        # remove temp files
            if len(file_list) > 1:
                from labpack.records.settings import remove_settings
                for file in file_list:
                    remove_settings(file, remove_dir=True)

        return transcript_details

    def transcribe_bytes(self, byte_data, clip_length=None, audio_mimetype='', compress=True):

        '''
            a method to transcribe text from audio byte data
            
        :param byte_data: byte data in buffer with audio data 
        :param clip_length: [optional] integer with seconds to divide clips into
        :param compress: [optional] boolean to convert file to audio/ogg
        :param audio_mimetype: [optional] string with byte data mimetype
        :return: dictionary with transcribed text segments in 'segments' key
        '''

        title = '%s.transcribe_bytes' % self.__class__.__name__
        bytes_arg = "%s(byte_data=b'...')" % title

    # validate inputs
        input_fields = {
            'clip_length': clip_length,
            'audio_mimetype': audio_mimetype
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # validate data mimetype
        if audio_mimetype:
            file_extension = ''
            for key, value in self.fields.schema['audio_extensions'].items():
                if value['mimetype'] == audio_mimetype:
                    file_extension = value['extension']
        else:
            if self.magic:
                magic_details = self.magic.analyze(byte_data=byte_data)
                file_name = magic_details['name']
                if not file_name:
                    file_name = 'audio'
                file_name += magic_details['extension']
                ext_kwargs = {
                    'file_name': file_name,
                    'extension_map': self.fields.schema['audio_extensions'],
                    'method_title': title,
                    'argument_title': 'byte_data'
                }
                file_details = self._validate_extension(**ext_kwargs)
                audio_mimetype = file_details['mimetype']
                file_extension = file_details['extension']
            else:
                raise ValueError('%s argument requires audio_mimetype (or magic) to determine its mimetype.' % bytes_arg)

    # construct default return
        transcript_details = {
            'error': '',
            'segments': []
        }

    # transcribe entire buffer
        if clip_length is None:
            try:
                transcript = self.client.recognize(byte_data, audio_mimetype, continuous=True)
                if transcript['results']:
                    for result in transcript['results']:
                        transcript_details['segments'].append(result['alternatives'][0])
            except Exception as err:
                transcript_details['error'] = err

    # save buffer to disk, segment and transcribe in multiple threads
        else:
            import os
            from time import sleep
            from math import ceil
            from moviepy.editor import AudioFileClip

        # save buffer to disk
            clip_folder = self._create_folder()
            full_name = 'audio_full.%s' % file_extension
            full_path = os.path.join(clip_folder, full_name)
            with open(full_path, 'wb') as f:
                f.write(byte_data)
                f.close()

        # convert file
            if compress:
                file_name, file_extension = os.path.splitext(full_path)
                if file_extension != '.ogg':
                    full_path = self.convert_audio(full_path, 'audio/ogg', True)
                    file_details = {
                        'name': 'audio_full.ogg',
                        'extension': '.ogg',
                        'mimetype': 'audio/ogg'
                    }
                    audio_mimetype = file_details['mimetype']
                    file_extension = file_details['extension']

        # open audio file
            count = 0
            retry_count = 10
            while True:
                try:
                    audio = AudioFileClip(full_path)
                    break
                except PermissionError:
                    sleep(.05)
                    count += 1
                    if count > retry_count:
                        raise
            audio_duration = audio.duration

        # construct list of files to transcribe
            file_list = []
            if audio_duration < clip_length:
                file_list.append(full_path)
            else:

        # create temporary audio files
                count = 0
                t_start = 0
                while t_start < audio_duration:
                    t_end = t_start + clip_length
                    if t_end > audio_duration:
                        t_end = ceil(audio_duration)
                        segment = audio.subclip(t_start)
                    else:
                        segment = audio.subclip(t_start, t_end)
                    clip_name = 'audio%s.%s' % (count, file_extension)
                    clip_path = os.path.join(clip_folder, clip_name)
                    segment.write_audiofile(clip_path, verbose=False)
                    file_list.append(clip_path)
                    count += 1
                    t_start = t_end

        # run file transcription method
            transcript_details = self._transcribe_files(file_list, audio_mimetype)

        # remove temp files
            if len(file_list) > 1:
                from labpack.records.settings import remove_settings
                for file in file_list:
                    remove_settings(file, remove_dir=True)

        return transcript_details

    def transcribe_stream(self, data_stream):

        ''' a method to perform rolling transcription '''

        return True
