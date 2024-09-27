#!/usr/bin/env bash
#
# User input to 3x3 block ascii

# 1 2 3 4 5 6 7
# 🬭 🬋 🬂 🬎 🬹 🬰 🮋

one='🬭'
two='🬋'
thr='🬂'
fou='🬎'
fiv='🬹'
six='🬰'
sev='🮋'

a=$fiv$fou$fiv
b=$sev$sev$fiv
c=$sev$six$six
d=$sev$six$two
e=$sev$sev$six
f=$sev$fou$thr
g=$sev$six$fiv
h=$sev$two$sev
i=$six$sev$six
j=$fiv$one$sev
k=$sev$two$six
l=$sev$one$one
m=$sev$fou$sev
n=$sev$thr$sev
o=$sev$six$sev
p=$sev$fou$fou
q=$fou$fou$sev
r=$sev$fou$six
s=$one$sev$thr
t=$thr$sev$thr
u=$sev$one$sev
v=$fou$one$fou
w=$sev$fiv$sev
x=$six$two$six
y=$thr$fiv$thr
z=$thr$sev$one

input=$1
len=${#input}

for ((iter = 0; iter < len; iter++)); do
    char="${input:iter:1}"
    case $char in
        "a"|"A") printf $a" ";;
        "b"|"B") printf $b" ";;
        "c"|"C") printf $c" ";;
        "d"|"D") printf $d" ";;
        "e"|"E") printf $e" ";;
        "f"|"F") printf $f" ";;
        "g"|"G") printf $g" ";;
        "h"|"H") printf $h" ";;
        "i"|"I") printf $i" ";;
        "j"|"J") printf $j" ";;
        "k"|"K") printf $k" ";;
        "l"|"L") printf $l" ";;
        "m"|"M") printf $m" ";;
        "n"|"N") printf $n" ";;
        "o"|"O") printf $o" ";;
        "p"|"P") printf $p" ";;
        "q"|"Q") printf $q" ";;
        "r"|"R") printf $r" ";;
        "s"|"S") printf $s" ";;
        "t"|"T") printf $t" ";;
        "u"|"U") printf $u" ";;
        "v"|"V") printf $v" ";;
        "w"|"W") printf $w" ";;
        "x"|"X") printf $x" ";;
        "y"|"Y") printf $y" ";;
        "z"|"Z") printf $z" ";;
        " ") echo -n "   ";;
        *) echo "$char";;
    esac
done
echo
