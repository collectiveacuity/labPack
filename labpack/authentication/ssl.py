''' a package of methods for managing ssl authentication '''
__author__ = 'rcj1492'
__created__ = '2018.02'
__license__ = 'MIT'

def generate_keystore(key_alias, key_folder='./', root_cert='', truststore='', password='', organization='', organization_unit='', locality='', country='', key_size=2048, verbose=True, overwrite=False):

    ''' a function to generate a keystore and cert files for self-signed ssl authentication '''

    title = 'generate_keystore'
    
# import dependencies
    import os
    from subprocess import call, STDOUT, Popen, PIPE
    DEVNULL = open(os.devnull, 'w')

# define system call
    def _call(sys_command, ignore='', prompt_input='', title=''):
        if title and verbose:
            print('%s ... ' % title, end='', flush=True)
        p = Popen(sys_command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        if prompt_input:
            stdout, stderr = p.communicate(str('%s\n' % prompt_input).encode('utf-8'))
        if p.returncode != 0:
            cmd_err = p.stdout.read().decode()
            if not cmd_err:
                pass
            elif ignore:
                if not cmd_err.find(ignore) > -1:
                    raise Exception(cmd_err)
            else:
                if title and verbose:
                    print('ERROR.')
                raise Exception(cmd_err)
        if title and verbose:
            print('done.')

# verify libraries
    try:
        call('openssl version', shell=True, stdout=DEVNULL)
    except:
        raise Exception('%s requires openssl library. try: sudo apt-get install openssl' % title)
    try:
        _call('keytool -help', ignore='Key and Certificate Management Tool')
    except:
        raise Exception('%s requires keytool library. try: sudo apt-get install openjdk-8-jre' % title)

# validate input
    if not isinstance(key_alias, str):
        raise ValueError('%s(key_alias="...") must be a string datatype.' % title)
    if not key_size in (2048, 4096):
        raise ValueError('%s(key_size=%s must be either 2048 or 4096' % (title, key_size))
    import re
    input_fields = {
        'organization': organization,
        'organization_unit': organization_unit,
        'locality': locality,
        'country': country
    }
    for key, value in input_fields.items():
        if re.findall('[^\w_\-\s]', value):
            raise ValueError('%s(%s="%s") must contain only alphanumeric characters, _, - and spaces.' % (title, key, value))

# construct key folder
    from os import path, makedirs, remove
    if not path.exists(key_folder):
        makedirs(key_folder)
    elif not path.isdir(key_folder):
        raise ValueError('%s(key_folder="%s") must be a directory.' % (title, key_folder))

# validate cert path
    cert_path = path.join(key_folder, '%s.crt' % key_alias)
    if path.exists(cert_path) and not overwrite:
        raise ValueError('%s.crt already exists in %s. to overwrite, set overwrite=true' % (key_alias, key_folder))

# validate root path
    from copy import deepcopy
    root_cert_copy = deepcopy(root_cert)
    if root_cert_copy:
        if not path.exists(root_cert_copy):
            root_cert_copy = path.join(key_folder, root_cert_copy)
            if not path.exists(root_cert_copy):
                raise ValueError('%s(root_cert="%s") is not a valid path.' % (title, root_cert_copy))
        root_node, root_ext = path.splitext(root_cert_copy)
        root_key = root_node + '.key'
        if not root_ext in ('.crt', '.pem'):
            raise ValueError('%s(root_cert="%s") must be a .crt or .pem file type.' % (title, root_cert_copy))
        elif not path.exists(root_key):
            key_path, key_name = path.split(root_key)
            raise ValueError('%s(root_cert="%s") requires a matching private key %s' % (title, root_cert_copy, key_name))
        root_path = root_cert_copy
        key_path = root_path.replace('.crt', '.key')
    else:
        key_path = path.join(key_folder, 'root.key')
        root_path = path.join(key_folder, 'root.crt')
        if path.exists(root_path) and not overwrite:
            raise ValueError('root.crt already exists in %s. to overwrite, set overwrite=true' % key_folder)

# validate truststore path
    truststore_copy = deepcopy(truststore)
    if truststore_copy:
        if not path.exists(truststore_copy):
            truststore_copy = path.join(key_folder, truststore_copy)
            if not path.exists(truststore_copy):
                raise ValueError('%s(truststore="%s") is not a valid path.' % (title, truststore_copy))
        trust_node, trust_ext = path.splitext(truststore_copy)
        if not trust_ext in ('.jks'):
            raise ValueError('%s(truststore="%s") must be a .jks file type.' % (title, truststore_copy))
        truststore_path = truststore_copy
        trust_root, trust_node = path.split(truststore_path)
        trust_alias, trust_ext = path.splitext(trust_node)
    else:
        truststore_path = path.join(key_folder, 'truststore.jks')
        trust_alias = 'truststore'
        if path.exists(truststore_path) and not overwrite:
            raise ValueError('%s.jks already exists in %s. to overwrite, set overwrite=true' % (trust_alias, key_folder))

# format DNAME fields
    if not organization:
        organization = 'None'
    if not organization_unit:
        organization_unit = 'None'
    if not locality:
        locality = 'None'
    if not country:
        country = 'None'

# create root certificate
    if not root_cert_copy:
        subject_args = '/CN=root/OU=%s/O=%s/L=%s/C=%s' % (
            organization_unit,
            organization,
            locality,
            country
        )
        root_subject = '-subj %s' % subject_args.replace(' ', '\ ')
        password_text = '-passout pass:%s' % password
        sys_command = 'openssl req -newkey rsa:%s -x509 -nodes -keyout %s -out %s -days 36500 %s %s' % (key_size, key_path, root_path, root_subject, password_text)
        _call(sys_command, ignore='writing new private key', title='Generating root certificate')

# generate server cert
    server_dname = '-dname "CN=%s, OU=%s, O=%s, L=%s, C=%s"' % (
        key_alias, organization_unit, organization, locality, country
    )
    keystore_path = path.join(key_folder, '%s.jks' % key_alias)
    if path.exists(keystore_path) and not overwrite:
        raise ValueError('%s.jks already exists in %s. to overwrite, set overwrite=true' % (key_alias, key_folder))
    elif path.exists(keystore_path):
        remove(keystore_path)
    sys_command = 'keytool -genkey -keyalg RSA -alias %s -validity 36500 -keystore %s -storepass %s -keypass %s -keysize %s %s' % (key_alias, keystore_path, password, password, key_size, server_dname)
    _call(sys_command, ignore='JKS keystore uses a proprietary format', title='Generating keystore for %s' % key_alias)

# convert cert to pkcs12
    sys_command = 'keytool -importkeystore -srckeystore %s -destkeystore %s -deststoretype pkcs12 -storepass %s -keypass %s' % (keystore_path, keystore_path, password, password)
    _call(sys_command, prompt_input=password, title='Converting keystore to pkcs12 standard')
    remove('%s.old' % keystore_path)

# generate certificate request
    request_path = path.join(key_folder, '%s.csr' % key_alias)
    sys_command = 'keytool -certreq -alias %s -file %s -keystore %s -storepass %s -keypass %s %s' % (
        key_alias, request_path, keystore_path, password, password, server_dname
    )
    _call(sys_command, title='Generating certificate signing request for %s'% key_alias)

# sign server cert with root cert
    cert_path = path.join(key_folder, '%s.crt' % key_alias)
    sys_command = 'openssl x509 -req -CA %s -CAkey %s -in %s -out %s -days 36500 -CAcreateserial -passin pass:%s' % (root_path, key_path, request_path, cert_path, password)
    _call(sys_command, ignore='Getting CA Private Key', title='Signing certificate for %s with root certificate' % key_alias)

# add root cert to server keystore
    root_root, root_node = path.split(root_path)
    root_alias, root_ext = path.splitext(root_node)
    sys_command = 'keytool -importcert -keystore %s -alias %s -file %s -noprompt -keypass %s -storepass %s' % (keystore_path, root_alias, root_path, password, password)
    _call(sys_command, ignore='Certificate was added to keystore', title='Adding root certificate to keystore for %s' % key_alias)

# add server cert to server keystore
    sys_command = 'keytool -importcert -keystore %s -alias %s -file %s -noprompt -keypass %s -storepass %s' % (keystore_path, key_alias, cert_path, password, password)
    _call(sys_command, ignore='Certificate reply was installed in keystore', title='Adding certificate for %s to keystore for %s' % (key_alias, key_alias))

# add root certificate to truststore
    if not truststore_copy:
        if path.exists(truststore_path):
            remove(truststore_path)
        sys_command = 'keytool -importcert -keystore %s -alias %s -file %s -noprompt -keypass %s -storepass %s' % (truststore_path, root_alias, root_path, password, password)
        _call(sys_command, ignore='Certificate was added to keystore', title='Generating truststore for root certificate')

# add server cert to truststore
    sys_command = 'keytool -importcert -keystore %s -alias %s -file %s -noprompt -keypass %s -storepass %s' % (truststore_path, key_alias, cert_path, password, password)
    _call(sys_command, ignore='Certificate was added to keystore', title='Adding certificate for %s to truststore' % key_alias)

# remove .srl files
    from os import listdir
    for file_name in listdir('./'):
        if file_name == '.srl':
            remove(file_name)
    for file_name in listdir(key_folder):
        file_alias, file_ext = path.splitext(file_name)
        if file_ext == '.srl':
            remove(path.join(key_folder, file_name))

    return True

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
        country='US'
    )
    generate_keystore(
        key_alias='123.456.789.1', 
        key_folder='../../data/keys', 
        root_cert='root.crt', 
        truststore='truststore.jks', 
        password='cassandra', 
        organization='Collective Acuity', 
        organization_unit='Cassandra Cluster', 
        locality='',
        country='US'
    )