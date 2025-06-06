import re
from collections import Counter

def load_words(filepath):
    with open(filepath, 'r') as f:
        words = f.read().lower().split()
    return words

def build_vocab(words):
    return Counter(words)

def build_frequency_from_corpus(corpus_file):
    with open(corpus_file, 'r') as f:
        text = f.read().lower()
    words = re.findall(r'\b[a-z]+\b', text)
    return Counter(words)

def word_probability(word, N, word_counts):
    return word_counts[word] / N if word in word_counts else 0

def edit_one_letter(word):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    inserts = [L + c + R for L, R in splits for c in letters]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    return set(deletes + inserts + replaces + transposes)

def edit_two_letters(word):
    return set(e2 for e1 in edit_one_letter(word) for e2 in edit_one_letter(e1))

def known(words, dictionary_set):
    return set(w for w in words if w in dictionary_set)

def autocorrect(word, dictionary_set, word_counts):
    word = word.lower()
    if word in dictionary_set:
        return word
    
    candidates = (known(edit_one_letter(word), dictionary_set)
                  or known(edit_two_letters(word), dictionary_set)
                  or [word])
    
    N = sum(word_counts.values())
    return max(candidates, key=lambda w: word_probability(w, N, word_counts))
