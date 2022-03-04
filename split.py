import pickle
words = []
with open('words8/words.txt') as fin:
    for _ in range(9000):
        text = fin.readline().strip().split()
        words.append(text[0])
    with open('words8/answers8.list','wb') as fout:
        pickle.dump(words[:2500], fout)
    with open('words8/guesses8.set', 'wb') as fout:
        pickle.dump(set(words), fout)
