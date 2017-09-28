__author__ = 'rcj1492'
__created__ = '2017.06'
__licence__ = 'MIT'

def get_ip(source='aws'):
    
    ''' a method to get current public ip address of machine '''
    
    if source == 'aws':
        source_url = 'http://checkip.amazonaws.com/'
    else:
        raise Exception('get_ip currently only supports queries to aws')
    
    import requests
    try:
        response = requests.get(url=source_url)
    except Exception as err:
        from labpack.handlers.requests import handle_requests
        from requests import Request
        request_object = Request(method='GET', url=source_url)
        request_details = handle_requests(request_object)
        raise Exception(request_details['error'])
    current_ip = response.content.decode()
    current_ip = current_ip.strip()
    
    return current_ip

def describe_ip(ip_address, source='whatismyip'):

    ''' a method to get the details associated with an ip address '''
    
# determine url
    if source == 'nekudo':
        source_url = 'https://geoip.nekudo.com/api/%s' % ip_address
    elif source == 'geoip':
        source_url = 'https://freegeoip.net/json/%s' % ip_address
    elif source == 'whatismyip':
        # http://whatismyipaddress.com/ip-lookup
        source_url = 'https://whatismyipaddress.com/ip/%s' % ip_address
    else:
        raise Exception('describe_ip currently only supports queries to nekudo')

    # TODO incorporate geoip module and c dependencies with local database
    # http://tech.marksblogg.com/ip-address-lookups-in-python.html

# send request
    ip_details = {
        'accuracy_radius': 0,
        'asn': '',
        'assignment': '',
        'city': '',
        'continent': '',
        'country': '',
        'hostname': '',
        'ip': '',
        'isp': '',
        'latitude': 0.0,
        'longitude': 0.0,
        'organization': '',
        'postal_code': '',
        'region': '',
        'timezone': '',
        'type': ''
    }
    import requests
    try:
        response = requests.get(url=source_url)
    except Exception as err:
        from labpack.handlers.requests import handle_requests
        from requests import Request
        request_object = Request(method='GET', url=source_url)
        request_details = handle_requests(request_object)
        raise Exception(request_details['error'])

# extract response
    if source == 'whatismyip':
        import re
        response_text = response.content.decode()
        table_regex = re.compile('<table>\n<tr><th>IP.*?</table>\n<span\sstyle', re.S)
        table_search = table_regex.findall(response_text)
        if table_search:
            table_text = table_search[0]
            field_list = [ 'IP', 'Hostname', 'ISP', 'Organization', 'Type', 'ASN', 'Assignment', 'Continent', 'Country', 'State/Region', 'City', 'Latitude', 'Longitude', 'Postal Code']
            for field in field_list:
                field_regex = re.compile('<tr><th>%s:</th><td>(.*?)</td>' % field, re.S)
                field_search = field_regex.findall(table_text)
                if field_search:
                    ip_details[field.lower().replace(' ','_')] = field_search[0]
        for field in ('longitude', 'latitude'):
            if field in ip_details.keys():
                coord_regex = re.compile('\-?\d+\.\d+')
                coord_search = coord_regex.findall(ip_details[field])
                if coord_search:
                    ip_details[field] = float(coord_search[0])
        if 'country' in ip_details.keys():
            country_regex = re.compile('([\w\s]+?)($|\s<img)')
            country_search = country_regex.findall(ip_details['country'])
            if country_search:
                ip_details['country'] = country_search[0][0]
        for field in ('type', 'assignment'):
            if field in ip_details.keys():
                link_regex = re.compile('>(.*?)<')
                link_search = link_regex.findall(ip_details[field])
                if link_search:
                    ip_details[field] = link_search[0]
        if 'state/region' in ip_details.keys():
            ip_details['region'] = ip_details['state/region']
            del ip_details['state/region']
    elif source == 'nekudo':
        response_details = response.json()
        ip_details['country'] = response_details['country']['name']
        ip_details['latitude'] = response_details['location']['latitude']
        ip_details['longitude'] = response_details['location']['longitude']
        ip_details['accuracy_radius'] = response_details['location']['accuracy_radius']
        if response_details['city']:
            ip_details['city'] = response_details['city']
        ip_details['ip'] = response_details['ip']
        for key in response_details.keys():
            if key not in ip_details.keys() and key != 'location':
                ip_details[key] = response_details[key]
    else:
        response_details = response.json()
        for field in ('city', 'ip', 'latitude', 'longitude'):
            ip_details[field] = response_details[field]
        ip_details['country'] = response_details['country_name']
        ip_details['region'] = response_details['region_name']
        ip_details['postal_code'] = response_details['zip_code']
        ip_details['timezone'] = response_details['time_zone']
    
    return ip_details

if __name__ == '__main__':
    
    from pprint import pprint
    ip_address = get_ip()
    ip_details = describe_ip(ip_address)
    pprint(ip_details)
    pprint(describe_ip(ip_address, 'nekudo'))
    pprint(describe_ip(ip_address, 'geoip'))