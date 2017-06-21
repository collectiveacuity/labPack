__author__ = 'rcj1492'
__created__ = '2016.11'
__license__ = 'MIT'

from labpack.parsing.magic import labMagic

if __name__ == '__main__':
    from labpack.platforms.localhost import localhostClient
    localhost_client = localhostClient()
    file_path = '../data/test_photo.diy'
    file_url = 'https://pbs.twimg.com/profile_images/479475632158408704/Zelyz-xr_400x400.png'
    byte_data = open('../data/test_pdf.pde', 'rb').read()
    if localhost_client.os.sysname in ('Windows'):
        lab_magic = labMagic('../data/magic.mgc')
    else:
        lab_magic = labMagic()
    analysis = lab_magic.analyze(file_path)
    assert analysis['extension'] == '.png'
    analysis = lab_magic.analyze(file_url=file_url)
    assert analysis['name'] == 'Zelyz-xr_400x400.png'
    analysis = lab_magic.analyze(byte_data=byte_data)
    assert analysis['mimetype'] == 'application/pdf'
    not_a_file = 'happy'.encode('utf-8')
    analysis = lab_magic.analyze(byte_data=not_a_file)
    assert analysis['mimetype'] == 'text/plain'