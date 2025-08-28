# utils/rabin_karp.py
import re
from collections import defaultdict

def rabin_karp_common_substrings(a, b, min_len=20, max_matches=10):
    """
    Character-level Rabin-Karp search for common substrings.
    Returns list of matched unique substrings (descending length).
    """
    a_norm = ' '.join(a.split()).lower()
    b_norm = ' '.join(b.split()).lower()
    la, lb = len(a_norm), len(b_norm)
    if la < min_len or lb < min_len:
        return []

    matches = []
    seen = set()

    base = 256
    mod = 2**61 - 1

    max_possible = min(la, lb)
    # limit start length to avoid too heavy work on huge docs
    start_len = min(max_possible, 300)

    for L in range(start_len, min_len - 1, -1):
        if len(matches) >= max_matches:
            break
        powL = pow(base, L, mod)
        hashes = defaultdict(list)
        h = 0
        # build hashes for 'a'
        for i in range(la):
            h = (h * base + ord(a_norm[i])) % mod
            if i >= L - 1:
                if i - L >= 0:
                    h = (h - ord(a_norm[i - L]) * powL) % mod
                start = i - L + 1
                hashes[h].append(start)
        # scan b
        h = 0
        for j in range(lb):
            h = (h * base + ord(b_norm[j])) % mod
            if j >= L - 1:
                if j - L >= 0:
                    h = (h - ord(b_norm[j - L]) * powL) % mod
                start_b = j - L + 1
                if h in hashes:
                    substr_b = b_norm[start_b:start_b + L]
                    for start_a in hashes[h]:
                        substr_a = a_norm[start_a:start_a + L]
                        if substr_a == substr_b:
                            if substr_a not in seen:
                                matches.append(substr_a.strip())
                                seen.add(substr_a)
                                break
                if len(matches) >= max_matches:
                    break

    matches.sort(key=lambda x: -len(x))
    return matches[:max_matches]
