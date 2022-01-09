#! /usr/bin/python3
import os, sys

os.chdir('words')

def splitList(n):
    fn = f'wlist_match{n}.txt'
    dirname = f'match{n}'
    try:
        os.mkdir(dirname)
    except FileExistsError:
        pass
    with open(fn) as fin:
        words = [line.strip() for line in fin.readlines()]
    os.chdir(dirname)
    words = [word for word in words if word.isalpha()]
    len5 = [word for word in words if len(word)==5]
    len6 = [word for word in words if len(word)==6]
    len7 = [word for word in words if len(word)==7]
    len8 = [word for word in words if len(word)==8]
    with open('len5', 'w') as fout:
        for word in len5:
            fout.write(f'{word}\n')
    with open('len6', 'w') as fout:
        for word in len6:
            fout.write(f'{word}\n') 
    with open('len7', 'w') as fout:
        for word in len7:
            fout.write(f'{word}\n')
    with open('len8', 'w') as fout:
        for word in len8:
            fout.write(f'{word}\n')
            
    print(5, len(len5))
    print(6, len(len6))
    print(7, len(len7))
    print(8, len(len8))

n = int(sys.argv[1])
splitList(n)