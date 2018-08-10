#!/bin/bash

BIN=""

for dir in "$(locate mailsender | grep -m 1 mailsender)"
do
	if [ -d "$dir" ]; then
		echo $dir 
		BIN="$dir"
		break
	fi 
done

python "$BIN/mailsender.pyc" "$BIN" || ( echo "$0: file not found: $BIN/mailsender.pyc" &&  exit 1)
	
