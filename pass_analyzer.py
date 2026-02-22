# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 18:15:31 2026

@author: Varad
"""


import re
import hashlib
import requests
import math
import json
import os
from concurrent.futures import ThreadPoolExecutor

# CONFIG

MARKOV_MODEL_FILE = "markov_model.json"

with open(MARKOV_MODEL_FILE, "r") as f:
    markov_model = json.load(f)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = os.path.join(BASE_DIR, "token_cache.json")

HEADERS = {
    "User-Agent": "PasswordAnalyzerHackathon/1.0 (contact: example@email.com)"
}

GLOBAL_MAX_VIEWS = 100_000_000
GLOBAL_MAX_TREND = 10
GLOBAL_MAX_LEAK = 10_000_000

# OBFUSCATION MAP

OBFUSCATION_MAP = {
    '@': 'a',
    '3': 'e',
    '!': 'i',
    '0': 'o',
    '$': 's',
    '1': 'l'
}

def smart_deobfuscate(password):
    chars = list(password)

    for i, ch in enumerate(chars):
        if ch in OBFUSCATION_MAP:
            left = chars[i-1] if i > 0 else ''
            right = chars[i+1] if i < len(chars)-1 else ''

            if left.isalpha() and right.isalpha():
                chars[i] = OBFUSCATION_MAP[ch]

    return ''.join(chars)

# KEYBOARD GRAPH

KEYBOARD_ROWS = [
    "1234567890",
    "qwertyuiop",
    "asdfghjkl",
    "zxcvbnm"
]

keyboard_graph = {}

for row in KEYBOARD_ROWS:
    for i in range(len(row)):
        neighbors = []
        if i > 0:
            neighbors.append(row[i-1])
        if i < len(row)-1:
            neighbors.append(row[i+1])
        keyboard_graph[row[i]] = neighbors

# CACHE SYSTEM

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=4)

cache = load_cache()

# TOKEN EXTRACTION

def extract_tokens(password):
    rough = re.split(r"[^a-zA-Z0-9]+", password)
    tokens = []

    for token in rough:
        if not token:
            continue

        camel_parts = re.findall(r'[A-Z][a-z]*|[a-z]+|\d+', token)

        if len(camel_parts) > 1:
            tokens.extend([p.lower() for p in camel_parts])
        else:
            tokens.append(token.lower())

    return tokens

# HAVE I BEEN PWNED

def check_pwned(password):
    try:
        sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
        prefix = sha1[:5]
        suffix = sha1[5:]

        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        response = requests.get(url, timeout=5, headers=HEADERS)

        if response.status_code != 200:
            return 0

        for line in response.text.splitlines():
            returned_suffix, count = line.split(":")
            if returned_suffix == suffix:
                return int(count)

        return 0
    except:
        return 0

# WIKIPEDIA METRICS

def wiki_metrics(term):
    term = term.lower()

    if term in cache and "wiki" in cache[term]:
        return tuple(cache[term]["wiki"])

    try:
        search_url = "https://en.wikipedia.org/w/api.php"

        params = {
            "action": "query",
            "list": "search",
            "srsearch": term,
            "format": "json"
        }

        r = requests.get(search_url, params=params, timeout=5, headers=HEADERS)
        if r.status_code != 200:
            return 0, 0

        data = r.json()
        if "query" not in data or not data["query"]["search"]:
            return 0, 0

        title = data["query"]["search"][0]["title"].replace(" ", "_")

        pageviews_url = (
            f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
            f"en.wikipedia/all-access/all-agents/{title}/daily/20250101/20250228"
        )

        pv = requests.get(pageviews_url, timeout=5, headers=HEADERS)
        if pv.status_code != 200:
            return 0, 0

        pv_data = pv.json()
        if "items" not in pv_data:
            return 0, 0

        views = [item["views"] for item in pv_data["items"]]
        total_views = sum(views)
        avg = total_views / len(views)
        trend = views[-1] / (avg + 1)

        cache.setdefault(term, {})["wiki"] = (total_views, trend)
        save_cache(cache)

        return total_views, trend

    except:
        return 0, 0

# SMART POPULARITY

def get_popularity(token):
    clean = re.sub(r"[^a-z]", "", token.lower())

    # Ignore very short semantic tokens
    if len(clean) < 3:
        return 0, 0

    views, trend = wiki_metrics(clean)

    if views == 0:
        return 0.05, 0.05

    popularity_score = math.log(views + 1) / math.log(GLOBAL_MAX_VIEWS + 1)
    trend_score = math.log(min(trend, GLOBAL_MAX_TREND) + 1) / math.log(GLOBAL_MAX_TREND + 1)

    return popularity_score, trend_score

# TOKEN GENERATION

def generate_tokens(password):
    normalized = smart_deobfuscate(password)
    tokens = extract_tokens(normalized)

    results = []

    with ThreadPoolExecutor(max_workers=4) as executor:
        popularity_results = list(executor.map(get_popularity, tokens))

    for token, (popularity, trend) in zip(tokens, popularity_results):

        if token in cache and "leak" in cache[token]:
            leak_count = cache[token]["leak"]
        else:
            leak_count = check_pwned(token)
            cache.setdefault(token, {})["leak"] = leak_count

        leak_score = math.log(leak_count + 1) / math.log(GLOBAL_MAX_LEAK + 1)

        results.append({
            "word": token,
            "popularity": popularity,
            "trend": trend,
            "leak_frequency": leak_score
        })

    save_cache(cache)
    return results

# ENTROPY + SCORES

def expectation_entropy(tokens):
    entropy = 0

    for t in tokens:
        # Weighted risk probability
        risk = (
            0.5 * t["leak_frequency"] +
            0.3 * t["popularity"] +
            0.2 * t["trend"]
        )

        # Clamp to avoid log(0)
        risk = max(risk, 1e-6)

        entropy += -math.log2(risk)

    return entropy

def shannon_entropy(password):
    if not password:
        return 0

    freq = {}
    for char in password:
        freq[char] = freq.get(char, 0) + 1

    entropy = 0
    length = len(password)

    for count in freq.values():
        p = count / length
        entropy += -p * math.log2(p)

    return entropy * length

def dcai_score(tokens):
    if not tokens:
        return 0
    raw = sum(t["popularity"] * t["leak_frequency"] for t in tokens) / len(tokens)
    return min(raw, 1)

def markov_score(password):
    score = 0
    for i in range(len(password) - 1):
        a = password[i]
        b = password[i+1]
        prob = markov_model.get(a, {}).get(b, 1e-6)
        score += -math.log2(prob)
    return score

def keyboard_penalty(password):
    penalty = 0
    for i in range(len(password) - 1):
        a = password[i].lower()
        b = password[i+1].lower()
        if a in keyboard_graph and b in keyboard_graph[a]:
            penalty += 1
    return penalty

def final_security_score(password, tokens):
    shannon = shannon_entropy(password)
    markov = markov_score(password)
    expectation = expectation_entropy(tokens)
    dcai = dcai_score(tokens)
    keyboard = keyboard_penalty(password)

    shannon_norm = min(shannon / 100, 1)
    markov_norm = min(markov / 95, 1)
    expectation_norm = expectation / (expectation+15)  # slightly tighter scale
    keyboard_penalty_norm = min(keyboard / len(password), 1)
    dcai_inverse = 1 - dcai

    final = (
        0.06 * shannon_norm +
        0.39 * markov_norm +
        0.25 * expectation_norm +
        0.30 * dcai_inverse
    )

    final *= (1 - 0.5 * keyboard_penalty_norm)

    return round(min(final, 1), 4)

def generate_suggestions(password, tokens):
    suggestions = []

    shannon = shannon_entropy(password)
    markov = markov_score(password)
    expectation = expectation_entropy(tokens)
    dcai = dcai_score(tokens)
    keyboard = keyboard_penalty(password)

    # Low randomness (structure predictable)
    if markov < 40:
        suggestions.append("Increase randomness. Avoid predictable character sequences.")

    # Low character diversity
    if shannon < 25:
        suggestions.append("Use a wider mix of uppercase, lowercase, numbers, and symbols.")

    #  Keyboard pattern detected
    if keyboard >= 3:
        suggestions.append("Avoid sequential keyboard patterns like '1234' or 'qwerty'.")

    # High semantic familiarity
    if dcai >= 0.01:
        suggestions.append("Avoid common or leaked words found in public datasets.")

    # High expectation entropy from semantic tokens
    if expectation < 9:
        suggestions.append("Avoid using trending names, places, or common terms.")

    # Too short
    if len(password) < 10:
        suggestions.append("Increase password length for better security.")

    if not suggestions:
        suggestions.append("Strong password. Maintain unpredictability and length.")

    return suggestions
# ==============================
# MAIN
# ==============================

def analyze_password(password):
    tokens = generate_tokens(password)

    return {
        "tokens": tokens,
        "expectation_entropy": expectation_entropy(tokens),
        "dcai_score": dcai_score(tokens),
        "shannon_entropy": shannon_entropy(password),
        "markov_score": markov_score(password),
        "final_security_score": final_security_score(password, tokens),
        "suggestions": generate_suggestions(password, tokens)
    }

if __name__ == "__main__":
    password = input("Enter password: ")
    result = analyze_password(password)

    print("\nToken Data:")
    for t in result["tokens"]:
        print(t)

    print("\nExpectation Entropy:", result["expectation_entropy"])
    print("DCAI Score:", result["dcai_score"])
    print("Shannon Entropy:", result["shannon_entropy"])
    print("Markov Score:", result["markov_score"])
    print("Final Security Score:", result["final_security_score"])
    print("\nSuggestions:")
    for s in result["suggestions"]:
        print("-", s)
