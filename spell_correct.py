# http://www.aoky.net/articles/peter_norvig/spell-correct.htm
import re, collections

def words(text: str) -> list:
    return re.findall('[a-z]+', text.lower())

def train(features: list) -> collections.defaultdict:
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train(words(open('big.txt').read()))

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word: str) -> set:
    """wordからの編集距離が1である語の集合を返す."""
    n = len(word)
    deletion = [word[:i] + word[i+1:] for i in range(n)]
    transposition = [word[:i] + word[i+1] + word[i] + word[i+2:] for i in range(n-1)]
    alteration = [word[:i] + c + word[i+1:] for c in alphabet for i in range(n)]
    insertion = [word[:i] + c + word[i:] for c in alphabet for i in range(n+1)]
    return set(deletion + transposition + alteration + insertion)

def edits2(word: str) -> set:
    """wordからの編集距離が2である語の集合を返す."""
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1))

def known_edits2(word: str) -> set:
    """
    既知(big.txtから学習済み)の語のうち、wordからの編集距離が2であるものの集合を返す.
    """
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words: list) -> set:
    """wordsに含まれる語のうち、既知のものを抽出する"""
    return set(w for w in words if w in NWORDS)

def correct(word: str) -> str:
    word = word.lower()
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or {word}
    result = max(candidates, key=lambda w: NWORDS[w])
    if result != word:
        result = "もしかして：" + result
    return result
