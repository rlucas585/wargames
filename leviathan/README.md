# Wargames - Leviathan Walkthrough

Walkthrough of the leviathan wargames series on [OvertheWire][OTW].

Leviathan can be a bit unwelcoming after bandit, as there are no instructions
on any of the challenge pages, and we're left to our own devices to figure out
any answers.

> Password for leviathan0: leviathan0

### Leviathan0

Simple ssh into the first level, as we've learned for bandit:

```
ssh leviathan0@leviathan.labs.overthewire.org -p 2223
```

We find an empty home directory, but searching for hidden files finds a
directory named ".backup". Inside, there is only one file, a bookmarks.html
file. The first thought I had is to just `grep` the file for "password":

```
cat bookmarks.html | grep password
```

And we immediately find what we're looking for. On to leviathan1.

> Password for leviathan1: rioGegei8m

### Leviathan1

This challenge immediately became a lot more complicated than the previous one.
Our home directory contains an executable called "check", which when run,
asks for a password. The difference from this and similar exercises in bandit
however, is that we don't know any of the rules for the password: numbers or
characters, or both, or how long the password is. The number of possibilities is
huge - it would be better if there were more clues we could look for.

We have a binary, we don't know the language it was compiled from, but it is
possible to disassemble it into **assembly language**, a very low-level
language where commands are translated almost 1-to-1 into actions to perform
on the processor. To do this, we run:

```
objdump -d -M intel check
```

`-d` is the disassemble option, `-M intel` specifies to output the assembly
in the intel syntax (as opposed to AT&T syntax). By taking a look within the
**main** within our output, we see a few valuable clues:

1) A call to printf - this seems very likely to be the "password: " output we
get when we run `./check`.
2) 3 calls to getchar - strongly suggesting that only the first three
characters of the password are relevant.
3) Most importantly, a call to **strcmp** - This must be the comparison between
input and actual password. If we take a look at the two values pushed onto the
stack before this strcmp call, we can see that they are **[ebp-0x10]** and
**[ebp-0xc]**. From our getchar calls, we can see that [ebp-0xc] corresponds
to the input, so [ebp-0x10] must be the password! We look earlier in the main,
to the stack allocations, and we can see that the hexadecimal values:
**0x786573** have been entered into this address. A run of `man ascii` allows
us to look up the characters these hex values correspond to: 78 = x, 65 = e,
and 73 = s. Reverse these (due to the direction that memory is read in), and
we'll have our password: **sex**.

We enter our password into `./check`, and are rewarded with entry into the
shell, but a run of the `whoami` command will show us that we are now
logged in as leviathan2! `cat /etc/leviathan_pass/leviathan2` and we have the
password for the next level.

> Password for leviathan2: ougahZi8Ta

### Leviathan2

A new binary: "printfile". Running it without arguments will give us some
minimal instructions, informing us that it is a simple file printer.

Another thing to note about our **printfile** binary is that it has a slightly
strange output to `ls -l`, with the permissions reading: `-r-sr-x---`. What is
this 's' in our permissions? This means that our binary is a **setuid** binary,
it will allow us to run a command as another user (like in bandit19 of the
bandit wargame), presumably as leviathan3.

Running `./printfile` for the leviathan3 password returns
an output of "You cant have that file...", contrasting with our output
if we should try to `cat` the file, where we get a "Permission denied"
response.

We can get more information on the workings of our binary by running it with
the `ltrace` command: `ltrace ./printfile /etc/leviathan_pass/leviathan3`.
`ltrace` intercepts and records dynamic library calls from a process, so it
will show us what external functions are being used by our binary.

Running `ltrace` with leviathan2 and leviathan3, we can find what is occurring
within the binary: When reading leviathan3, a function called **access** is
returning a value of -1, whereas reading leviathan2 it returns a value of 0.
Maybe it's possible to trick this access function?

If we read the manual for **access()**, we see that it will check whether the
calling process can access a file, and **access()** will check using the
calling process's **real** UID (user idenfication) instead of the **effective**
UID (the ID of the setuid binary).

The manual for **access()** also contains a great clue in the notes section.
Using these calls to check user authorization before actually doing something
can create a security hole, in our case:

1. printfile checks whether the file given can be accessed.
2. A string is printed into another with snprintf.
3. User id's are retrieved and set.
4. Then, the file is read to standard output.

The security hole in a program like this, is that the file can change between
the **access()** check, and the actions upon the file. We can exploit this
using a shell script that will execute **printfile** with a symbolic link to a
file we have permissions to read (e.g. /tmp/tmpdir/link => file_we_can_read),
then immediately change that symlink to a file we normally would not be
able to read (e.g. /tmp/tmpdir/link => file_we_CANNOT_read).

```
#!/bin/bash

touch file_we_can_read
while true; do
	ln -sf ./file_we_can_read link &
	~/printfile link &
	ln -sf /etc/leviathan_pass/leviathan3 link
done
```

IMPORTANT TO NOTE: Make sure that your temporary directory has executable
permissions for all users, as permission will be denied otherwise.

The script may have to run a few times before the symlink is changed in between
the calls to **access()** and **system()** in the binary, but eventually it
should line up correctly and print the password for leviathan3.

Notes: /tmp/tmp.sIqdC0r6Lf

> Password for leviathan3: Ahdiemoo1j

### Leviathan3

After the previous level, this one is a nice break. There's a binary called
"level3" in our home directory. We run it, and it requests a password.
After we inevitably get it wrong the first time, we can run the program again
with `ltrace`. After attempting another time, `ltrace` shows us that the binary
runs strcmp between our attempted password, and a string "snlprintf".

Running the binary a third and final time, and attempting "snlprintf" as the
password, we are told "You've got shell!". A quick `whoami` will show that
we are now **leviathan4**, and thus we can easily cat our password.

> Password for leviathan4: vuH0coox6m

### Leviathan4

In leviathan4, we start with a seemingly empty home directory, but it doesn't
take long to find that there is a hidden directory ".trash". Inside we find
an executable named "bin", which prints out a series of 1's and 0's, which is
binary of course. They are separated into 8-bit sequences - for one byte each.
One byte is also the memory required for a single ASCII character - so we
must convert the binary into its corresponding characters.

We can do this byte by byte, it's not a long sequence, but a small python
script can do our work for us too:

```
# Convert binary string (in specific 8-bit format) to characters

import sys

iowrapper = sys.stdin
nums = iowrapper.read()
for num in nums.split():
	power = 7
	char = 0
	for c in range( len(num) ):
		if num[c] == '1':
			char += 2 ** power
		power -= 1
	print (chr(char), end = '')
```

The `sys.stdin` line gets an IOWrapper object from stdin, then is converted
to a string in `nums = iowrapper.read()`. The first `for` loop then iterates
through the bytes, and the second loop iterates through each bit of a byte,
adding the relevant powers of 2 to convert the binary number to decimal.
`chr(char)` then converts the number into a character for printing. The
`end = ''` ensures that a newline isn't printed after each character.

After writing the script, the output of `bin` just needs to be piped to
the python script:

`~/.trash/bin | python3 script.py`

> Password for leviathan5 Tith4cokei: 

### Leviathan5

Another exploit of a **setuid** binary, we have an executable named 'leviathan5'
that can be executed by leviathan5, but sets uid to leviathan6. Attempting to
run the executable will inform us that there is no '/tmp/file.log' file
present.

Investigation of the binary through `objdump` or `ltrace` will quickly reveal
that the binary simply gets a character from the file one by one, and prints
it out. All we need to do for this exercise is to trick the binary into
printing out the file we want to see, /etc/leviathan_pass/leviathan6, which the
binary should be able to read as it sets uid as leviathan6.

We run:

`ln -s /etc/leviathan_pass/leviathan6 /tmp/file.log`

Making /tmp/file.log into a symbolic link to the file we really want to read.
Now when we execute the 'leviathan5' binary, we get the result we want to see.

> Password for leviathan6: UgaoFee4li

### Leviathan6

Immediately we find another setuid binary (leviathan6), setting our uid to
leviathan7. Running it without an argument informs us that we must enter
`./leviathan6 <4 digit code>`. Presumably we need to enter the correct number.
A quick run of `ltrace` and a random 4-digit code shows that the binary runs
`atoi`, a function to convert a string of characters (our input) into an
integer.

If we run our `objdump` command from leviathan1 again: `objdump -d -M intel
leviathan6`, we can use the same trick as before. Find where `atoi` is called
in the main, and you'll see a comparison of the `atoi` return value (stored
in `rax`) with an address `[rbp - 0xc]`. If we look a little higher in the
assembly, we can actually see exactly what is placed into this address, the
hexadecimal value 0x1bd3. A quick conversion to integer (either by an online
service or the below tiny python script or bash command) and we find the
value **7123**.

```
# python to convert hex
print (0x1bd3)

# bash to convert hex
echo "obase=10; ibase=16; 1BD3"
```

Running `./leviathan6 7123` will enter us into a shell as leviathan7, and
we can easily read the password for leviathan7.

> Password for leviathan7 ahy7MaeBo9: 

### Leviathan7

We've reached the final level, and are rewarded with a CONGRATULATIONS
file, which congratulates us, and asks us please to not make any writeups for
Leviathan (whoops...).

[OTW]: https://overthewire.org
