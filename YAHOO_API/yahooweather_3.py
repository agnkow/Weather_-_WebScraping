
import urllib
import calendar
import time
import random
import base64
import hashlib
import hmac
import urllib
import json


def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


def hash_string(string):
    return base64.b64encode(hashlib.sha1(string).digest())


class YahooWeather(object):
    def __init__(self, app_id, client_id, client_secret):
        self._url = 'https://weather-ydn-yql.media.yahoo.com/forecastrss';
        self._app_id = app_id
        self._client_id = client_id
        self._client_secret = client_secret
        self._data = {}
        self._oauth = {
            'oauth_consumer_key': client_id,
            'oauth_nonce': hash_string(str(random.randint(1, 1000)).encode('utf-8')),
            'oauth_signature_method': 'HMAC-SHA1',
            'oauth_timestamp': str(int(time.time())),
            'oauth_version': '1.0'
        }
    
    def get_authorization(self, query=None):
        base_info = self.build_base_string(self._url, 'GET', merge_two_dicts(query, self._oauth))
        composite_key = urllib.parse.quote(self._client_secret, safe='') + '&'
        hash_hmac = hmac.new(composite_key.encode('utf-8'), base_info.encode('utf-8'), hashlib.sha1).digest()

        oauth_signature = base64.b64encode(hash_hmac)
        authorization = self.build_auth_header(self._oauth, oauth_signature)

        return authorization
    
    def build_auth_header(self, oauth, oauth_signature):
        r = 'OAuth {}'
        values = []
        for key in sorted(oauth.keys()):
            values.append('{}="{}"'.format(key, urllib.parse.quote(oauth.get(key, ""), safe='')))
        
        values.append('{}="{}"'.format("oauth_signature", urllib.parse.quote(oauth_signature, safe='')))
        
        return r.format(', '.join(values))

    def build_base_string(self, base_uri, method_name, params):
        r = []
        keys = params.keys()

        for key in sorted(keys):
            r.append(key + "=" + urllib.parse.quote(params[key], safe=''))
        
        base_string = (method_name + "&" + urllib.parse.quote(base_uri, safe='') + "&") + urllib.parse.quote('&'.join(r), safe='')

        return base_string
    
    def request(self, params=None):
        params = params or {
            'location': 'sunnyvale,ca',
            'format': 'json',
        }

        headers = {
            "Authorization": self.get_authorization(params),
            "Yahoo-App-Id": self._app_id
        }

        handler = urllib.request.HTTPHandler()
        opener = urllib.request.build_opener(handler)
        query_string = urllib.parse.urlencode(params)

        request = urllib.request.Request("{}?{}".format(self._url, query_string))

        for header in (headers or {}):
            request.add_header(header, headers[header])
        
        request.get_method = lambda: "GET"
        
        try:
            connection = opener.open(request, timeout=60)
        except urllib.error.HTTPError as e:
            connection = e

        if connection.code == 200:
            data = json.loads(connection.read())
            response = {
                "status": 200,
                "message": "success",
                "data": data
            }

        else:
            response = { 
                "status": 500,
                "message": connection.read()
            }

        return response



# sample usage
app_id = ''
client_id = ''
client_secret = ''


yahooweather = YahooWeather(app_id, client_id, client_secret)
response = yahooweather.request(params={
    'location': 'sunnyvale,ca',
    'format': 'json',
})
print(response)



