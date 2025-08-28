def build_lps(pattern: str):
    l = len(pattern)
    lps = [0] * l
    length = 0
    i = 1
    while i < l:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length-1]
            else:
                lps[i] = 0
                i += 1
    return lps


def kmp_search(text: str, pattern: str):
    """Return list of start indices where pattern occurs."""
    if not pattern or not text:
        return []
    lps = build_lps(pattern)
    res = []
    i = j = 0
    n, m = len(text), len(pattern)
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == m:
                res.append(i - j)
                j = lps[j-1]
        else:
            if j != 0:
                j = lps[j-1]
            else:
                i += 1
    return res
