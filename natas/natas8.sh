#!/bin/bash

HEX=$(printf $1 | awk '{ print toupper($1) }')
BIN=$(BC_LINE_LENGTH=200 bc <<< "obase=2; ibase=16; $HEX")
COPY=${BIN}
LEN=${#BIN}
for (( i=$LEN-1 ; i >= 0; i--));
do
	rev="$rev${COPY:$i:1}";
done
echo $rev
# echo $rev | base64 -d
