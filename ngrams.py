# process word list from https://github.com/hackerb9/gwordlist

words = []
for _ in range(9):
    words.append([])
with open('/home/saul/Downloads/1gramsbyfreq.txt') as fin:
    for line in fin:
        text = line.split()
        if len(text) != 2:
            continue
        if not text[0].isalpha():
            continue
        if not text[0].isascii():
            continue
        if not text[0].islower():
            continue
        n = len(text[0])
        if 5 <= n <= 8:
            words[n].append(line)
with open('words5/words.txt','w') as fout:
    for line in words[5]:
        fout.write(line) 
with open('words6/words.txt','w') as fout:
    for line in words[6]:
        fout.write(line) 
with open('words7/words.txt','w') as fout:
    for line in words[7]:
        fout.write(line) 
with open('words8/words.txt','w') as fout:
    for line in words[8]:
        fout.write(line) 
        