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
statement with `preg_match` for these character (which performs a regular 
expression search).

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

### Natas

Text

> Password for natas:

[OTW]: https://overthewire.org
