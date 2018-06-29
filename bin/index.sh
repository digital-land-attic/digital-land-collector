#!/bin/bash

dir=$1

echo "path"
cd "${dir:=.}" &&
	find . -name \*.md |
	sed -e 's/^\.\///' -e "/README.md$/d" |
	sort
