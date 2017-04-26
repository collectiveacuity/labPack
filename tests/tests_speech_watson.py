__author__ = 'rcj1492'
__created__ = '2017.04'
__license__ = 'MIT'

from labpack.speech.watson import watsonSpeechClient

if __name__ == '__main__':

# construct client
    from labpack.records.settings import load_settings
    from labpack.handlers.requests import handle_requests
    config_path = '../../cred/watson.yaml'
    audio_path = '../data/watson_test2.ogg'
    magic_path = '../data/magic.mgc'
    audio_path2 = '../data/test_voice.ogg'
    bluemix_config = load_settings(config_path)
    username = bluemix_config['watson_speech2text_username']
    password = bluemix_config['watson_speech2text_password']
    watson_client = watsonSpeechClient(username, password, magic_file=magic_path)

# test file conversion
    from os import path
    new_path = watson_client.convert_audio(audio_path, 'audio/ogg', overwrite=True)
    assert path.exists(new_path)

# test file transcription
    details = watson_client.transcribe_file(audio_path)
    assert details['segments'][0]['transcript'].find('listen') > -1

# test byte data transcription
    byte_data = open(audio_path2, 'rb').read()
    details = watson_client.transcribe_bytes(byte_data, audio_mimetype='audio/ogg')
    assert details['segments'][0]['transcript'].find('again') > -1