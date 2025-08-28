import re

def tokenize_words(s: str):
    return re.findall(r'\w+', s.lower())

def lcs_length_words(a: str, b: str) -> int:
    """Return length (in words) of LCS between a and b using dynamic programming (space optimized)."""
    A = tokenize_words(a)
    B = tokenize_words(b)
    m, n = len(A), len(B)
    if m == 0 or n == 0:
        return 0
    prev = [0] * (n + 1)
    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        for j in range(1, n + 1):
            if A[i-1] == B[j-1]:
                curr[j] = prev[j-1] + 1
            else:
                curr[j] = prev[j] if prev[j] >= curr[j-1] else curr[j-1]
        prev = curr
    return prev[n]
