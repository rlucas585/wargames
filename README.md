# Wargames - Bandit Walkthrough

Walkthrough of the bandit wargames series on [OvertheWire][OTW].

### Bandit0

Level 0's consists of two steps - log onto the bandit server for the first time,
and read the contents of a file.

To accomplish this first step, all we have to do is follow the instructions on
the OvertheWire Bandit0 page. `ssh bandit0@bandit.labs.overthewire.org -p 2220`
will connect us to the server through port 2220, and we will be asked for a
password. This password is simple, as it has been handed straight to us. Type in
bandit0, and you will be welcomed to the server as the user bandit0.

We enter the server's filesystem in our own home directory, named bandit0. The
command `pwd` will inform us of our location in the server, /home/bandit0.
Next, the command `ls` shall show us the contents of the current directory.
We see a file called 'readme'. Finally, by running the `cat` command (
`cat readme`), we can read the contents of the file, clearly a password key of
some sort. This is the password for the next level, bandit1.

> Password for bandit1: boJ9jbbUNNfktd78OOpsqOltutMc3MY1

### Bandit1

After ssh'ing back into the server, as bandit1 this time, we are in a new home
directory, /home/bandit1. `ls` reveals the contents of the directory to us, a
single file named '-'. The solution is not as simple as `cat -` however, and
trying this will bring us to a strange state where everything we type and enter
is simply repeated back to us. This is because `cat -` will instruct the cat
command to read the contents of standard input, and display them on the screen.
`CTRL-D` will send an end-of-file (EOF) signal to `cat`, and allow us to regain
control of the shell.

But how do we now read the contents of the file? We cannot address the file
by it's name alone, we must also specify the directory to make clear that we
are looking for a file in the filesystem, with a name beginning with a hyphen.

To do this, we simply append our `cat` command with `./`, to mark that we are
looking for a file in the *current directory*. (`./` represents the current
directory, `../` represents the parent directory in our filesystem).

So, `cat ./`, and the password appears before us.

> Password for bandit2: CV1DtqXWVFXTvM2F0k09SHz0YwRINYA9

### Bandit2

Upon entry and a quick `ls` to get our bearings, we immediately see a file
named 'spaces in this filename', and our challenge is pretty self explanatory.

This task is actually rendered even easier than the previous one due to the
bash shell's builtin autocomplete feature. If we simply type `cat sp<TAB>` then
bash will fill in the name of the file for us, supply escape characters `\ ` in
the place of spaces, as is required to distinguish between spaces in a filename,
and spaces to separate arguments given to cat. Our final command should look
like this:

```
cat spaces\ in\ this\ filename
```

And upon entering this command we see our password for bandit3.

> Password for bandit3: UmHadQclWmgdLOKQ3YNgjWxGoRMb5luK

### Bandit3

The first major difference we see in bandit3, is a different color of our ls
output (depending on your terminal of course). This is because `inhere` is not
a file, but a directory, and we now must learn to navigate a file system by the
use of the `cd` command, which stands for **c**hange **d**irectory.

After running `cd inhere` and `ls` however, there is no output. We shouldn't
give up on this directory just yet though. By adding the `-a` option to our `ls`
command, we can instruct `ls` to display ALL the contents of a directory,
including hidden files.

```
ls -a
```

And we are met with a file named ".hidden". Once we are aware of its presence,
`cat .hidden` will read the hidden file's contents and give us the password to
bandit4.

> Password for bandit4: pIwrPrtPN36QITSp3EQaw936yaFoFgAB

### Bandit4

Another directory greets us, which we simple `cd inhere` into. ls shows us a
number of files, all beginning with hyphens, to make life difficult for us.
`ls -l` will give us some more information about their contents, but all the
files appear to be identical, each with a size of 33 bytes and the same creation
date.

Another command to give us information about files, is the `file` command, which
will tell us the type of file. We will also use something called a **wildcard**,
which will allow us to run the command on every file at once. The wildcard in
the shell is the **"\*"** character, and as once again all files begin with
hyphens, we'll have to specify the directory again and use the command `file
./*`.

We can see that all the files but "-file07" are data files, with "-file07" being
an ASCII text file. `cat ./-file07` displays it's contents, the password for
bandit5.

> Password for bandit5: koReBOKuIDDepwhWk7jZC0RTdopnAYKh

### Bandit5

An important clue for this challenge: The file we are looking for is **1033**
bytes in size, as stated in the instructions.

This challenge is made simple using a new command, the `find` command. There
are several options for this command, for this exercise we'll use the `-size`
option, and specify a size of 1033 bytes by using the suffix `c`.
The period in our command is to specify which directory to search, and we can
simply use a period to specify the current directory. `find` will search
recursively by default.

```
find . -size 1033c
```

And we can see the file that fits the bill: in ./maybehere07/.file2. Reading the
contents of this file we find the password for bandit6.

> Password for bandit6: DXjZPULLxYr17uwoI01bNLQbtFemEgo7

### Bandit6

For this exercise, our file to find is **somewhere on the server**, not
necessarily within bandit6's filesystem.

We could travel up and down the server's filesystem, checking every directory
for the file, but there's a much easier way of going about this, using the
`find` command again. This time we'll use two new options, fitting with our new
information: the `-user` option, with 'bandit7' as an argument, and `-group`,
with 'bandit6' as an argument. We can also use the `-size` option with '33c' as
argument.

```
find / -user bandit7 -group bandit6 -size 33c
```

This will give us the correct file, but also a lot of error output informing us
that we don't have permission for certain directories. It's always useful to
be able to omit these, which can be done using a pipe to `grep` command. We also
have to redirect all error output to standard output, with `2>&1`.

```
find / -user bandit7 -group bandit6 -size 33c 2>&1 | grep -v "Permission denied"
```

And we've found our file, tucked away in '/var/lib/dpkg/info/bandit7.password'.
A simple cat command later, and we have the password for bandit7.

> Password for bandit7: HKBPTKQnIay4Fw76bEy8PVxKEDQRKTzs

### Bandit7

Our bandit7 directory contains only one file, 'data.txt', and we have the
instruction that our password is next to the word "millionth". The file is huge
however, and would take forever to comb through.

There's several routes to an answer here, but a simple grep can solve our issue.
We can cat our file, pipe the output to grep, searching for the word "millionth"
, and a single line with the word "millionth" and the password is displayed.

```
cat data.txt | grep "millionth"
```

> Password for bandit8: cvX2JJa4CFALtqS87jk27qwqGhBM9plV

### Bandit8

We have a single file again, 'data.txt', with 1001 lines. Many lines are
duplicated, and we must find the one line that appears only once.

For this challenge, we'll cat our file, and pipe the output to two new commands:
`sort`, which will organize all lines alphabetically, and `uniq -u`, which will
only print lines that are unique. Together, these commands will isolate and
print the only unique line in the file, giving the password for bandit9.

```
cat data.txt | sort | uniq -u
```

> Password for bandit9: UsvVyFSfZZWbi6wgC7dAFyFuR6jQQUhR

### Bandit9

Another similar exercise, this time with a data.txt file with unreadable text.
We need a new command to isolate the human-readable text in the file: `strings`.
We run `strings data.txt`, and along with a lot of nonsense characters, we can
easily spot one line that looks very much like our password for bandit10.

```
strings data.txt
```

> Password for bandit10: truKLdjsbJ5g7yyJ2X2R0o3a5HQJFuLk

### Bandit10

Another single 'data.txt' file. This one we have been told is 'base64 encoded
data'. `man base64` gives us all the info we need - specifically that to decode
base64 encoded data, we use `base64 -d`, with the -d option standing for
`--decode`.

`base64 -d data.txt` and we're handed the bandit11 password.

> Password for bandit11: IFukwKGsFW8MOq3IRFqrxE1hxTNEbUPR

### Bandit11

Our instruction is clear - to rotate all characters in our file by 13. A new
command will help here, the `tr` command, standing for **translate**. We pipe
output to `tr`, and supply `tr` with two sets of information. Each set must be
the same size, `tr` will convert any character from the first set into the
corresponding character in the second set.

To create our sets, we choose `[a-z]` for our first set, all characters of the
alphabet, and correspond them to the characters of the alphabet shifted 13
places: `[n-za-m]`. We pipe this output to another `tr` command that does the
same for the uppercase letters, and get our password for bandit12.

```
cat data.txt | tr "[a-z]" "[n-za-m]" | tr "[A-Z]" "[N-ZA-M]"
```

> Password for bandit12: 5Te8Y4drgCRfCx8ugdwuEX8KFC6k2EUu

### Bandit12

We have another data.txt file, but this one looks very different from those
we've previously seen. It is the contents of a compressed file, represented in a
hexadecimal format.

First, we must convert the file from hexadecimal back to its original format.
There's a really easy tool for this: `xxd` with `-r` option, to turn back from
hex into a normal file.

We can't do this in our home directory however, as we don't have permissions to
create new files on the server. We must make a temporary directory in /tmp, by
navigating to the /tmp directory and running `mkdir newdir` (where newdir is the
name of the new temporary directory). Then the `cp` command can be used to copy
our data.txt file to our new directory: `cp ~/data.txt /tmp/newdir` ('~'
represents the home directory of the user).

After moving our file to our new directory, we `xxd` to give us our non-hex
file: `xxd -r data.txt | cat > newfile`.

Our newfile doesn't give us the answer however, as it is compressed. The `file`
command will be of use here again, as it can inform us of what type of
compression has been used. There are several different types of compression that
can be done, so we will have to use a different extraction command each time:

1) Run `file filename` to determine compression type.
2) If the file type is compressed data, change the suffix of the file
depending on compression type:
	* gzip compressed: `mv filename filename.gz`
	* bzip2 compressed: `mv filename filename.bz`
	* tar compressed: `mv filename filename.tar`
3) Run the extraction command for the compression type:
	* gzip compressed: `gunzip filename.gz`
	* bzip2 compressed: `bunzip2 filename.bz`
	* tar compressed: `tar -xf filename.tar`
4) Go back to step 1.

Eventually, the filetype of the data will be "ASCII text", and `cat` will
reveal to us the password. It takes around 8 extractions to get there however,
making this a pretty time-consuming exercise.

> Password for bandit13: 8ZjyCRiBWFYkneahHwxCv3wb2a1ORpYL

### Bandit13

For the first time since bandit6, this exercise does not involve a data.txt
file. Instead, we are met with a file named "sshkey.private".
`file sshkey.private` shows us the file type: PEM RSA private key.

To understand this exercise, we need to check the manual for ssh `man ssh`. From
this, we learn that it is possible to log into a server with a key rather than
a password - and that two keys are required:

* A private key to be kept by the user.
* A public key corresponding to the user's private key. This public key is
stored in the home directory of the server user we are going to log into, in
this case bandit14. The public key is in the file ~/.ssh/authorized_keys (so
in our case: /home/bandit14/.ssh/authorized_keys).

If we move to /home/bandit14/.ssh/, we do find a file authorized_keys, which as
bandit13 we do not have the permission to read. It seems very likely that if we
use `ssh` with our private key from bandit13. To do this, we need the `-i`
option. So we go back to our bandit13 home directory:

`ssh -i sshkey.private bandit14@localhost`

localhost refers to the current machine - equivalent to
bandit.labs.overthewire.org -p 2220.

After entering this command, we are successfully logged in as bandit14.
To avoid having to always log into bandit13 to then enter bandit14, we can read
the password for bandit14 from /etc/bandit_pass/bandit14.

`cat /etc/bandit_pass/bandit14`

And we can now log into bandit14 directly with this password.

> Password for bandit14: 4wcYUJFw0k0XLShlDzztnTBHiqxU3b3e

### Bandit14

We need to use the password from bandit14 for this level, which as stated before
can be retrieved from /etc/bandit_pass/bandit14.

We have to submit the bandit14 password to port 30000 on the server. To do this,
we can use the `nc` commmand. From `man nc`, we learn that the simplest way to
use `nc` is in the format `nc host port`.

Our host is the current machine, so `localhost` can be used. We've been told
to submit to port `30000`, so entering `nc localhost 30000` will open the
connection we need.

```
nc localhost 30000
```

Now, our input will be directed to port 30000. We simply enter the password
to bandit14, hit enter, and are handed the password to bandit15.

> Password for bandit15: BfMYroe26WYalil77FoDi9qh59eK5xNr

### Bandit15

This exercise is very similar to the previous one - the only difference being
that we need to SSL encrypt our communications with port 30001. `nc` does not
have a simple option for this, but strangely, `ncat`, which is **NOT** the same
tool, does. (`nc` = `netcat`, but `ncat` is from a separate project)

Our command is almost identical to the last exercise (and we could have in fact
used `ncat localhost 30000` for the last exercise), except this time we need
to specify an option for ssl encryption as well (`--ssl`).

```
ncat --ssl localhost 30001
```

We open up a connection with SSL encryption this time, and after entering our
bandit15 password - we receive the password for bandit16 in reply.

> Password for bandit16: cluFn7wTiGryunymYOu4RcffSxQluehd

### Bandit16

This time, we have to find which port to communicate with. We have a known
range, 31000-32000, but attempting to `ncat` with each of these one by one is
out of the question. Luckily, a powerful tool named `nmap` exists for us, which
can probe all ports on a network and return information about them.

For this exercise, all we need to do is a basic scan, specifying the network
localhost and the port range between 31000 and 32000.

```
nmap localhost -p31000-32000
```

Only three results! Enough to simply try one by one.

```
ncat -ssl localhost (portnumber)
```

After trying the password on our second port, 31790, we receive a correct
response! But instead of receiving a password, we get a sequence beginning
"-----BEGIN RSA PRIVATE KEY-----". What we have here, is a copy of a private
ssh key - similar to the key we received in bandit13.

We need to copy this text into a file in bandit16. There's a couple ways to do
this, the simplest being to redo the `ncat`, and this time pipe the output to
a file (make sure to do this in a tmp directory, where you have permission
to write files).

```
ncat --ssl localhost 31790 | cat > output.private
```

Then, using an ssh command similar to that in bandit13:

```
ssh -i output.private bandit17@localhost
```

The first time this is attempted, you'll get a message informing you that the
private key file is unprotected. This is because our output.private file will
have the default permissions - meaning only bandit16 can write to it, but
anybody can read it. This is unacceptable for a private sshkey, and ssh is
letting us know. Change the permissions with `chmod 400 output.private`, and
try again.

And we're into bandit17. Head over to /etc/bandit_pass/bandit17 to get the
password.

> Password for bandit17: xLYVMN9WE5zQ5vHacb0sZEVqbrp7nBTn

### Bandit17

Moving away from networking, we are back onto a challenge investigating files.
This one has a pretty nice one-step solution. We have two files, passwords.old
and passwords.new, identical except for a single line. We must find this line
in passwords.new, and again we have a very effective tool that will tell us the
difference between the two files: `diff`.

```
diff passwords.old passwords.new
```

Instantly we are shown the only conflicting lines in the two files, with the
greater than symbol (>) pointing to our new line in passwords.new.

Using this password to log into bandit18 gives us a new issue, to be dealt with
in the next challenge.

> Password for bandit18: kfBf3eYk5BPBRzwjqutbbfE887SVc5Yd

### Bandit18

So we login to bandit18 successfully, and are immediately met with the line
"Byebye !", and our connection is closed.

We're given a massive clue to this however: "Unfortunately, someone has modified
.bashrc to log you out when you log in with SSH.". Whenever we login to the
bandit server, we are using the **bash** shell - the program from which
we run other programs and navigate our filesystem. bash is configured via
the .bashrc file contained in our home directory. In this case, the config
file immediately ends our connection.

To get around this, we need to run `ssh` with an option specifying that we want
to enter a shell other than bash - such as the simpler **sh** shell. This is
easily done by using the `-t` option:

```
ssh bandit18@bandit.labs.overthewire.org -p 2220 -t /bin/sh
```

(The shells are located in the "binaries" folder /bin). After entering our
simpler shell, with no prompt but a $ sign, we can run `ls` to find our file
waiting for us, and `cat readme` will gift us the next password.

> Password for bandit19: IueksS7Ubh8G3DCwVzrTd8rAVOwq3M5x

### Bandit19

For Bandit19, we learn a little more about user ID, and how to use an
executable. The only contents of our directory is an executable called
"bandit20-do", and our instructions direct us to execute it without arguments
to find out how to use it. We do this by naming the executable within the
current directory: `./bandit20-do`.

We're told that "bandit20-do" can run a command as another user - similar to
the `su` command. The benefit of the executable, is that we don't need to
use bandit20's password to execute.

We know where the file we need to read is, in /etc/bandit_pass/ with the rest
of the passwords, so we simply run:

```
./bandit20-do cat /etc/bandit_pass/bandit20
```

And we find our password.

> Password for bandit20: GbKksEFF4yrVs6il55v6gwY5aVje5f0j

### Bandit20

Back to networking, and in this challenge we learn how to open a port on a
server in the most basic fashion: using our `nc` command.

For this exercise we have to open two terminals on the server - we can do this
with the `tmux` command. `tmux` has many uses and options, but for our purpose
we can simply open a tmux server after logging in (`tmux`), then split into
two windows with `<CTRL-B> "`. `<CTRL-B> + 'arrowkey'` will switch between
windows, we can use on as a listener, and one to send a message.

For our listener window, we open a port to listen using the `-l` option of `nc`,
using any port we'd like (if it's available).

```
nc -l -p <portnum>
"bandit20 password"
```

In our home directory in bandit20, the `suconnect` executable will connect to
a given port on localhost - and check for a single line of text that matches
the bandit20 password. Thus we must enter this line into our listener window.

In our messaging window, we put our executable into use:

```
./suconnect <portnum>
```

And provided the listener contained the correct password, we should receive
the bandit21 password, sent from suconnect.

> Password for bandit21: gE269g2h3mw3pwgrj0Ha9Uoqen1c9DGr

### Bandit21

For the next couple of exercises we'll be investigating `cron` events. `cron`
is a time-based job scheduler - it can be instructed to carry out a script
at specified times.

We're told to look for the task in /etc/cron.d, and upon entering this directory
we find 4 different cron jobs - **cronjob_bandit22** is the one we're looking
for here. `cat cronjob_bandit22` shows the following output:

```
@reboot bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null
* * * * * bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null
```

This actually consists of two instructions for cron:

1. @reboot is one of 8 special strings that can be specified instead of the
first five fields - it means run the script once, upon the start of the server.
2. \* \* \* \* \*: Specifies minute (0-59), hour (0-23), day of month (1-31),
month (1-12) and day of week (0-7) to run cron's task. An asterisk (\*) will
direct the task to run for every value.
So in this case, the script will be run every minute, of every day, of every
month.

Note the `&> /dev/null` in the cron tasks, this directs all output of the task
to /dev/null - deleting it to prevent any visible sign of the task having run.

The `bandit22` specifies which user to run the command under. More information
on cron and cron tables can be found by `man 8 cron` and `man 5 crontab`.

To discover what script is being run, `cat /usr/bin/cronjob_bandit22.sh`

What we discover is a shell script, that gives bandit22 write permissions on
a file /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv, and importantly, read permissions
to all users. It then `cat`'s the password for bandit22 from 
/etc/bandit_pass/bandit22 into this temp file.

So, to find the password, we just have to read the password by
`cat /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv`, and we are ready for bandit22.

> Password for bandit22: Yk7owGAcWjwMVRwrTesJEwB7WVOiILLI

### Bandit22

Another cron challenge. The first part of this exercise is identical to
bandit21, with the difference being the script that is executed. This time,
the script first defines two variables.

The first variable is simple, the result of a `whoami` command. If we run this
command, we'll get `bandit22` as output - it's important to remember however
that this script is being run as bandit23, so the **myname** variable will be
**bandit23**.

The second variable is a bit more complicated, but is made simpler by breaking
it down into it's components. First, the string "I am user bandit23" is echoed,
then taken as input into the command `md5sum`. `md5sum` will print
the MD5 checksum for our string. Then, the `cut` command will separate the
output into separate fields by spaces, (determined by the `-d ' '` option), and
select the first field (determined by the `-f 1` option).

This **mytarget** variable will then be the name of a temporary file that will
contain the bandit23 password. So to find the name, all we have to do is
run the command:

```
echo "I am user bandit23" | md5sum | cut -d ' ' -f 1
```

and we'll find the name of our temporary file. `cat /tmp/(name of file)` and
we have our password.

> Password for bandit23: jc1udXuA1tiHqjIsL8yaapX5XIAI6i0n

### Bandit23

Another cron task, and the script for this one is a little more complicated.
The name variable is set to bandit24, /var/spool/bandit24 is set as the active
directory, and a for loop executes every script within the directory. The
`timeout -s 9 60 ./$i` means that the current script ($i) will be executed, but
if it isn't complete within 60 seconds SIG 9 will be sent to the script,
terminating it.

We are able to create files in the /var/spool/bandit24, so if we create a
small script to copy the contents of the bandit24 password into a temp file, in
a directory that we've created.

A couple key points to consider: To place new files in a directory, a user
must have execute permissions on the directory. So before creating your script,
make a temp directory `mktemp`, make sure that the directory has free
permissions for everyone: `chmod 777 (your directory)`.

Additionally, make sure that the script has execute permissions, then place it
into the /var/spool/bandit24/ directory.

```
#!/bin/bash

cat /etc/bandit_pass/bandit24 > /tmp/(your directory)/output.txt
```

After waiting for a moment (you can try `cat`ting your script until it's
deleted), your script will be executed and deleted by `cron`, and your output
file should contain the password for bandit24.

> Password for bandit24: UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ

### Bandit

Text

> Password for bandit: 

[OTW]: https://overthewire.org
