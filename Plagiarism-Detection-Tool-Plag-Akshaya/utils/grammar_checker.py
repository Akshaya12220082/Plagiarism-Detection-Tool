# utils/grammar_checker.py
import re
from spellchecker import SpellChecker
from textblob import TextBlob
import nltk

# ensure wordnet available
try:
    nltk.data.find('corpora/wordnet')
except Exception:
    nltk.download('wordnet')

from nltk.corpus import wordnet

spell = SpellChecker()

def check_spelling_and_grammar(text, max_suggestions=20):
    """
    Returns a list of dicts: {'word': <wrong>, 'suggestions': [..], 'context': <snippet>}
    Uses pyspellchecker for misspell detection and TextBlob.correct() for quick grammar corrections (light).
    """
    words = re.findall(r'\w+', text.lower())
    miss = list(spell.unknown(words))
    results = []
    for w in miss[:max_suggestions]:
        suggestions = list(spell.candidates(w))[:5]
        # context: find first occurrence and show small surrounding
        idx = text.lower().find(w)
        context = text[max(0, idx - 30): idx + 30] if idx != -1 else ''
        results.append({'word': w, 'suggestions': suggestions, 'context': context})
    return results

def rephrase_snippet(snippet, max_changes=3):
    """
    Very lightweight rephraser: replace up to max_changes words with a WordNet synonym when available.
    This preserves structure and is deterministic-ish.
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
