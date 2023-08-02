#!/bin/bash
#
# Output random sequential line(s) from input text file
#
# Arg 1: path to text file
# Arg 2: number of sequential lines to output
#
# $ scriptname.sh /path/to/file.txt 10

lines=$(cat $1 | wc -l)
range=$(expr $lines - $2)
rand=$(shuf -i 1-$range -n 1)
end=$(expr $rand + $2 - 1)
cmd="sed -n '${rand},${end}p' $1"
output="$(eval $cmd)"

if [[ $2 == 1 ]]; then
    if [[ $output == "" ]]; then
        $(basename $0) && exit
    fi
fi

echo "$output"
