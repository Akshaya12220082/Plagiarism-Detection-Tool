import re

def tokenize_words(s: str):
    return re.findall(r'\w+', s.lower())

def edit_distance_words(a: str, b: str) -> int:
    """Compute Levenshtein distance at word-level between a and b."""
    A = tokenize_words(a)
    B = tokenize_words(b)
    m, n = len(A), len(B)
    if m == 0:
        return n
    if n == 0:
        return m
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if A[i-1] == B[j-1] else 1
            dp[i][j] = min(dp[i-1][j] + 1, dp[i][j-1] + 1, dp[i-1][j-1] + cost)
    return dp[m][n]
