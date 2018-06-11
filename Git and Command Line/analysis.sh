#!/usr/bin/env bash 
## analysis.sh

# Download the sonnets
curl http://www.gutenberg.org/files/1041/1041.txt -o Documents/511Assignments/a1-git-and-cli-shreyasabharwal/sonnets/sonnets.txt

# Trim introduction and concluding lines
# Remove leading blank characters 
head -n2662 Documents/511Assignments/a1-git-and-cli-shreyasabharwal/sonnets/sonnets.txt | tail +45 | cut -c 3- > Documents/511Assignments/a1-git-and-cli-shreyasabharwal/sonnets/cleaned-sonnets.txt
 
# Split sonnets into individual files. This will involve *many* commands.
cd Documents/511Assignments/a1-git-and-cli-shreyasabharwal/sonnets/

head -n1666 cleaned-sonnets.txt > sonnet-1.txt
head -n1685 cleaned-sonnets.txt | tail -n18 > sonnet-2-aa.txt
head -n2126 cleaned-sonnets.txt | tail +1686> sonnet-3.txt
head -n2142 cleaned-sonnets.txt | tail -n15 > sonnet-4-aa.txt
tail +2143 cleaned-sonnets.txt> sonnet-5.txt

split -l 17 --additional-suffix=.txt sonnet-1.txt sonnet-1-
split -l 17 --additional-suffix=.txt sonnet-3.txt sonnet-3-
split -l 17 --additional-suffix=.txt sonnet-5.txt sonnet-5-

rm sonnet-1.txt
rm sonnet-3.txt
rm sonnet-5.txt

# Find the longest sonnet (most words)
wc -w sonnet-*-*.txt | sort -n -r > lengths.txt

# Search for specific words in  the sonnets
grep -F 'truth' sonnet-*-*.txt > truth.txt
grep -F 'love' sonnet-*a.txt > love.txt

