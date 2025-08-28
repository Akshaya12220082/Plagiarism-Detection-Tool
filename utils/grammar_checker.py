import re
from spellchecker import SpellChecker
from textblob import TextBlob
import nltk

# ensure wordnet corpus
try:
    nltk.data.find('corpora/wordnet')
except Exception:
    nltk.download('wordnet')

from nltk.corpus import wordnet

spell = SpellChecker()

def check_spelling_and_grammar(text: str, max_suggestions: int = 20):
    """
    Returns a list of dicts with keys:
      - word: the misspelled word
      - suggestions: list of candidate corrections
      - context: small snippet
    """
    words = re.findall(r'\w+', text.lower())
    miss = list(spell.unknown(words))
    results = []
    for w in miss[:max_suggestions]:
        suggestions = list(spell.candidates(w))[:5]
        idx = text.lower().find(w)
        context = text[max(0, idx-30): idx+30] if idx != -1 else ''
        results.append({'word': w, 'suggestions': suggestions, 'context': context})
    return results

def rephrase_snippet(snippet: str, max_changes: int = 3):
    """
    Replace up to max_changes words with a WordNet synonym when available.
    """
    tokens = re.findall(r"\w+|\W+", snippet)
    changes = 0
    out = []
    for t in tokens:
        if re.match(r'\w+', t) and changes < max_changes:
            syns = wordnet.synsets(t)
            replacement = None
            for s in syns:
                for l in s.lemmas():
                    name = l.name().replace('_', ' ')
                    if name.lower() != t.lower() and name.isalpha():
                        replacement = name
                        break
                if replacement:
                    break
            if replacement:
                out.append(replacement)
                changes += 1
                continue
        out.append(t)
    return ''.join(out)
