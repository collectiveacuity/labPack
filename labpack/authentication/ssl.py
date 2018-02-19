''' a package of methods for managing ssl authentication '''
__author__ = 'rcj1492'
__created__ = '2018.02'
__license__ = 'MIT'

def generate_keystore(key_alias, key_folder='./', root_cert='', truststore='', password='', organization='', organization_unit='', locality='', state='', country=''):
    
    ''' a function to generate a keystore and cert files for ssl authentication '''

# import dependencies
    import os
    from subprocess import call, STDOUT, Popen, PIPE
    DEVNULL = open(os.devnull, 'w')

# define system call
    def _call(sys_command, ignore=''):
        p = Popen(sys_command, shell=True, stdout=PIPE, stderr=STDOUT)
        if p.returncode != 0:
            cmd_err = p.stdout.read().decode()
            if ignore:
                if not cmd_err.find(ignore) > -1:
                    raise Exception(cmd_err)
            else:
                raise Exception(cmd_err)

# verify libraries
    try:
        call('openssl version', shell=True, stdout=DEVNULL)
    except:
        raise Exception('generate_keystore requires openssl library. try: sudo apt-get install openssl')
    try:
        _call('keytool -help', ignore='Key and Certificate Management Tool')
    except:
        raise Exception('generate_keystore requires keytool library. try: sudo apt-get install openjdk-8-jre')

# validate input
    if not isinstance(key_alias, str):
        raise ValueError('generate_keystore(key_alias="...") must be a string datatype.')
    import re
    input_fields = {
        'organization': organization,
        'organization_unit': organization_unit,
        'locality': locality,
        'state': state,
        'country': country
    }
    for key, value in input_fields.items():
        if re.findall('[^\w_\-\s]', value):
            raise ValueError('generate_keystore(%s="%s") must contain only alphanumeric characters, _, - and spaces.' % (key, value))

# construct key folder
    from os import path, makedirs
    if not path.exists(key_folder):
        makedirs(key_folder)
    elif not path.isdir(key_folder):
        raise ValueError('generate_keystore(key_folder="%s") must be a directory.' % key_folder)

# validate root cert and truststore
    if root_cert:
        if not path.exists(root_cert):
            raise ValueError('generate_keystore(root_cert="%s") is not a valid path.' % root_cert)
    if truststore:
        if not path.exists(truststore):
            raise ValueError('generate_keystore(truststore="%s") is not a valid path.' % truststore)

# construct cert subject
    if not organization:
        organization = 'None'
    organization = organization.replace(' ', '\ ')
    if not organization_unit:
        organization_unit = 'None'
    organization_unit = organization_unit.replace(' ', '\ ')
    if not locality:
        locality = 'None'
    locality = locality.replace(' ', '\ ')
    if not state:
        state = 'None'
    state = state.replace(' ', '\ ')
    if not country:
        country = 'None'
    country = country.replace(' ', '\ ')
    cert_subject = '-subj /CN=root/OU=%s/O=%s/L=%s/S=%s/C=%s' % (
        organization_unit,
        organization,
        locality,
        state,
        country
    )

# create root certs
    if not root_cert:
        password_text = '-passout pass:%s' % password
        key_path = path.join(key_folder, 'root.key')
        cert_path = path.join(key_folder, 'root.crt')
        sys_command = 'openssl req -new -x509 -nodes -keyout %s -out %s -days 36500 %s %s' % (key_path, cert_path, cert_subject, password_text)
        print([sys_command])
        _call(sys_command, ignore='writing new private key')

if __name__ == '__main__':
    
    generate_keystore(
        key_alias='123.456.789.0', 
        key_folder='../../data/keys', 
        root_cert='', 
        truststore='', 
        password='cassandra', 
        organization='Collective Acuity', 
        organization_unit='Cassandra Cluster', 
        locality='', 
        state='', 
        country='US'
    )