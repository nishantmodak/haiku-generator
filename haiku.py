#!/usr/bin/python3

import re
import random
import sys

tempMapping = {}
mapping = {}
starts = []

def fixCaps(word):
    if word.isupper() and word != "I":
        word = word.lower()
    elif word[0].isupper():
        word = word.lower().capitalize()
    else:
        word = word.lower()
    return word

def toHash(lst):
    return tuple(lst)

def wordlist(filename):
    with open(filename, 'r') as f:
        wordlist = [fixCaps(w) for w in re.findall(r"[\w']+|[.,!?;]", f.read())]
    return wordlist

def addItemToTempMapping(history, word):
    global tempMapping
    while len(history) > 0:
        first = toHash(history)
        if first in tempMapping:
            if word in tempMapping[first]:
                tempMapping[first][word] += 1.0
            else:
                tempMapping[first][word] = 1.0
        else:
            tempMapping[first] = {}
            tempMapping[first][word] = 1.0
        history = history[1:]

def buildMapping(wordlist, mStrLength):
    global tempMapping
    starts.append(wordlist[0])
    for i in range(1, len(wordlist) - 1):
        if i <= mStrLength:
            history = wordlist[: i + 1]
        else:
            history = wordlist[i - mStrLength + 1: i + 1]
        follow = wordlist[i + 1]
        if history[-1] == "." and follow not in ".,!?;":
            starts.append(follow)
        addItemToTempMapping(history, follow)
    for first, followset in tempMapping.items():
        total = sum(followset.values())
        mapping[first] = dict([(k, v / total) for k, v in followset.items()])

def next(prevList):
    sum = 0.0    
    retval = ""
    index = random.random()

    while toHash(prevList) not in mapping:
        prevList.pop(0)

    for k, v in mapping[toHash(prevList)].items():
        sum += v
        if sum >= index and retval == "":
            retval = k
    return retval

def genSentence(mStrLength):
    curr = random.choice(starts)
    sent = curr.capitalize()
    prevList = [curr]

    while (curr not in "."):
        curr = next(prevList)
        prevList.append(curr)
        if len(prevList) > mStrLength:
            prevList.pop(0)
        if (curr not in ".,!?;"):
            sent += " " 
        sent += curr
    return sent

def main():
    if len(sys.argv) < 2:
        sys.stderr.write('Usage: ' + sys.argv[0] + ' text_source [chain_length=1 by default]\n')
        sys.exit(1)

    filename = sys.argv[1]
    mStrLength = 1
    if len(sys.argv) == 3:
        mStrLength = int(sys.argv[2])

    buildMapping(wordlist(filename), mStrLength)
    ast = genSentence(mStrLength)
    print(ast)

if __name__ == "__main__":
    main()
