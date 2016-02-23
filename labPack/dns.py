__author__ = 'rcj1492'
__created__ = '2015'

'''
Google Locations
geo location based upon wiki & cell towers
https://developers.google.com/maps/documentation/geolocation/

import netifaces
'''

import re
import os
from urllib.request import urlopen
import json
import socket
from timeit import default_timer as timer

class geoLocateByIP(object):

    '''
        a class of methods used to determine location from IP
        http://ip-api.com/docs/api:json
        http://www.iplocation.net/
        from stored database: https://github.com/appliedsec/pygeoip
        from stored database: http://lite.ip2location.com/
        import re
        from urllib.request import urlopen
        import json
        from config.apiCredentials import *
        from timeit import default_timer as timer
    '''

    def __init__(self, dpip_credentials):
        self.dpIPCred = dpip_credentials

    def ipAPI(self, ip_address):
        '''
            method for using ip-api.com api to locate an IP address
            ipAPIAPIThrottle = 60 / 250
            250 req per minute
            get request format
            ipv6 format [2001:db8:85a3:8d3:1319:8a2e:370:7348]
            import re
            from urllib.request import urlopen
            import json
            from config.apiCredentials import *
            from timeit import default_timer as timer
        :param ip_address: string in ipv4 or ipv6 format
        :return: dictionary of location information
        '''
        urlTitle = 'IP-API API'
        ipv4pattern = re.compile('\d+.\d+.\d+.\d+')
        ipv6pattern = re.compile('[0-9a-fA-F]+:[0-9a-fA-F]+:[0-9a-fA-F]+:[0-9a-fA-F:]*:[0-9a-fA-F]+$')
        if not ip_address:
            raise Exception('input does not contain all required parameters')
        elif not isinstance(ip_address, str):
            raise Exception('input is not the correct datatype')
        elif not ipv6pattern.match(ip_address) and not ipv4pattern.match(ip_address):
            raise Exception('input is not a valid internet address')
        else:
            url = 'http://ip-api.com/json/' + ip_address
            t1 = timer()
            r = urlopen(url).read().decode()
            t2 = timer()
            print(urlTitle + ': ' + format((t2 - t1), '.5f') + ' seconds')
            d = json.loads(r)
            k = ['query', 'status', 'org']
            for i in k:
                if i in d.keys():
                    del d[i]
            return d

    def dbIP(self, ip_address):
        '''
            method for using db-ip.com api to locate an IP address
            dbIPAPIThrottle = (60 * 60 * 24) / 2000
            2000 req per day
            get request format
            ipv6 format [2001:db8:85a3:8d3:1319:8a2e:370:7348]
            import re
            from urllib.request import urlopen
            import json
            from config.apiCredentials import *
            from timeit import default_timer as timer
        :param ip_address: string in ipv4 or ipv6 format
        :return: dictionary of location information
        '''
        urlTitle = 'DB-IP API'
        ipv4pattern = re.compile('\d+.\d+.\d+.\d+')
        ipv6pattern = re.compile('[0-9a-fA-F]+:[0-9a-fA-F]+:[0-9a-fA-F]+:[0-9a-fA-F:]*:[0-9a-fA-F]+$')
        if not ip_address:
            raise Exception('input does not contain all required parameters')
        elif not isinstance(ip_address, str):
            raise Exception('input is not the correct datatype')
        elif not ipv6pattern.match(ip_address) and not ipv4pattern.match(ip_address):
            raise Exception('input is not a valid internet address')
        else:
            url = 'http://api.db-ip.com/addrinfo?addr=' + ip_address + '&api_key=' + self.dpIPCred
            t1 = timer()
            r = urlopen(url).read().decode()
            t2 = timer()
            print(urlTitle + ': ' + format((t2 - t1), '.5f') + ' seconds')
            d = json.loads(r)
            k = ['address']
            for i in k:
                if i in d.keys():
                    del d[i]
            return d

class localPublicIP(object):

    '''
        a class of methods to determine local public IP address

    '''

    def __init__(self):
        pass

    def httpBin(self):

        '''
            from urllib.request import urlopen
            import json
            from timeit import default_timer as timer
        :return: local public ip address as string
        '''
        urlTitle = 'HTTP BIN API'
        url = 'http://httpbin.org/ip'
        t1 = timer()
        r = urlopen(url).read().decode()
        t2 = timer()
        print(urlTitle + ': ' + format((t2 - t1), '.5f') + ' seconds')
        return json.loads(r)['origin']

    def jsonIP(self):
        '''
            from urllib.request import urlopen
            import json
            from timeit import default_timer as timer
        :return: local public ip address as string
        '''
        urlTitle = 'JSON IP API'
        url = 'http://jsonip.com'
        t1 = timer()
        r = urlopen(url).read().decode()
        t2 = timer()
        print(urlTitle + ': ' + format((t2 - t1), '.5f') + ' seconds')
        return json.loads(r)['ip']

    def ip42(self):
        '''
            from urllib.request import urlopen
            import json
            from timeit import default_timer as timer
        :return: local public ip address as string
        '''
        urlTitle = 'IP 42 API'
        url = 'http://ip.42.pl/raw'
        t1 = timer()
        r = urlopen(url).read().decode()
        t2 = timer()
        print(urlTitle + ': ' + format((t2 - t1), '.5f') + ' seconds')
        return r

    def ipify(self):

        '''
            from urllib.request import urlopen
            import json
            from timeit import default_timer as timer
        :return: local public ip address as string
        '''

        urlTitle = 'Ipify API'
        url = 'https://api.ipify.org/?format=json'
        t1 = timer()
        r = urlopen(url).read().decode()
        t2 = timer()
        print(urlTitle + ': ' + format((t2 - t1), '.5f') + ' seconds')
        return json.loads(r)['ip']

class localPrivateIP(object):

    def __init__(self):
        pass

    def pingHTTP(self, ip_address):
        '''
            method for determining local IP assignment from public HTTP callback request
            get request format
            ipv6 format 2001:db8:85a3:8d3:1319:8a2e:370:7348 or 2001:4860:4860::8888
            import re
            import json
            from timeit import default_timer as timer
        :param ip_address: string in ipv4 or ipv6 format
        :return: dictionary of location information
        '''
        ipv4pattern = re.compile('\d+.\d+.\d+.\d+')
        ipv6pattern = re.compile('[0-9a-fA-F]+:[0-9a-fA-F]+:[0-9a-fA-F]+:[0-9a-fA-F:]*:[0-9a-fA-F]+$')
        if not ip_address:
            raise Exception('input does not contain all required parameters')
        elif not isinstance(ip_address, str):
            raise Exception('input is not the correct datatype')
        elif not ipv6pattern.match(ip_address) and not ipv4pattern.match(ip_address):
            raise Exception('input is not a valid internet address')
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((ip_address,80)) # 8.8.8.8 google's DNS server
            localSock = s.getsockname()[0]
            patternIP = re.compile('\d+.\d+.\d+.\d+')
            pIP = patternIP.match(localSock)
            if pIP:
                return localSock
            s.close()

    def askSocket(self):
        host = socket.getfqdn()
        addresses = socket.getaddrinfo(host, None)
        testList = []
        ipv4pattern = re.compile('\d+.\d+.\d+.\d+')
        ipv6pattern = re.compile('[0-9a-fA-F]+:[0-9a-fA-F]+:[0-9a-fA-F]+:[0-9a-fA-F:]*:[0-9a-fA-F]+$')
        for i in addresses:
            addr = i[4][0]
            if ipv6pattern.match(addr) or ipv4pattern.match(addr):
                testList.append(addr)
        return testList

    def socketHost(self):
        d = []
        host = socket.gethostname()
        for ip in socket.gethostbyname_ex(host)[2]:
            if not ip.startswith("127."):
                d.append(ip)
        return d

class wipMethods(object):

    def __init__(self):
        pass

    def get_lan_ip(self):
        # if os.name != "nt":
        import fcntl
        import struct
        def get_interface_ip(ifname):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            return socket.inet_ntoa(fcntl.ioctl(
                    s.fileno(),
                    0x8915,  # SIOCGIFADDR
                    struct.pack('256s', bytes(ifname[:15], 'utf-8'))
                )[20:24])
        ip = socket.gethostbyname(socket.gethostname())
        if ip.startswith("127.") and os.name != "nt":
            interfaces = ["eth0","eth1","eth2","wlan0","wlan1","wifi0","ath0","ath1","ppp0"]
            for ifname in interfaces:
                try:
                    ip = get_interface_ip(ifname)
                    break
                except IOError:
                    pass
        return ip

    def netifaces(self):
        '''
            import netifaces
            # pip install netifaces
            # requires C compiler
        :return:
        '''
        uuidList = netifaces.interfaces()
        deviceList = []
        null_address = '00:00:00:00:00:00:00:e0'
        for i in uuidList:
            res = netifaces.ifaddresses(i)
            if -1000 in res.keys() and 2 in res.keys():
                if res[-1000][0]['addr'] and not res[-1000][0]['addr'] == null_address:
                    deviceList.append(res[2][0]['addr'])
        return deviceList

    def getNetworkIp(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.connect(('<broadcast>', 0))
        return s.getsockname()[0]

    def unitTest(self):
        print(self.get_lan_ip())
        print(self.netifaces())
        print(self.getNetworkIp())




