import datetime
from urllib.parse import urlparse, parse_qs
import requests

OS_CLUSTER_URL = 'https://oauth-openshift.apps-crc.testing'
USERNAME = 'dsuser1'
PASSWORD = 'dsuser1'

params = {'client_id': 'openshift-challenging-client',
          'response_type': 'token'}

response = requests.get("{}/oauth/authorize".format(OS_CLUSTER_URL),
                        params=params,
                        allow_redirects=False,
                        verify=False,
                        auth=(USERNAME, PASSWORD))
now_date = datetime.datetime.now()

response.raise_for_status()

if response.status_code == 302:
    url_parts = urlparse(response.headers['Location'])
    fragment_parts = parse_qs(url_parts.fragment)
    access_token = fragment_parts['access_token'][0]
    expires_in = fragment_parts['expires_in'][0]

    expiry_date = now_date + datetime.timedelta(seconds=86400)

    print(access_token)
    print(expiry_date)
else:
    raise RuntimeError("Didn't get the expected 302 redirect")