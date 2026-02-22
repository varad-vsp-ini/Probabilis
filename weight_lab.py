# -*- coding: utf-8 -*-
"""
Created on Sun Feb 22 18:46:37 2026

@author: Varad
"""

from pass_analyzer import analyze_password
import matplotlib.pyplot as plt
import random

passwords = {
    "weak": [
        "aaaa1111",
        "abcd1234",
        "1111aaaa",
        "abcabc12",
        "zzzz9999",
        "12121212",
        "passpass1",
        "qazwsx12",
        "asdf1234",
        "0000aaaa"
    ],
    "semantic": [
        "RedPlanet2024!",
        "BlueOcean#77",
        "QuantumLeap88",
        "HiddenTiger#3",
        "SilentStorm22",
        "NeuralBridge5",
        "SolarFlare!9",
        "IronLogic2023",
        "FrozenMind#8",
        "GoldenRatio21"
    ],
    "random": [
        "g7#Lz2!Qp9@x",
        "T4$vN8#kR1!m",
        "xP9!qL3@zT7#",
        "bR2$kM8!vQ4@",
        "nL7#tZ1$Vp6!",
        "Qx3!mR9@kT2#",
        "vT8$zL4!qP1@",
        "kM2#rQ7$vT9!",
        "zP6!tL3@xR8#",
        "R9@vK1#tM4$z"
    ]
}

raw_metrics = {}

for category in passwords:
    for pwd in passwords[category]:
        result = analyze_password(pwd)
        raw_metrics[pwd] = {
            "category": category,
            "shannon": result["shannon_entropy"],
            "markov": result["markov_score"],
            "expectation": result["expectation_entropy"],
            "dcai": result["dcai_score"]
        }
        
        
def custom_score(metrics, w1, w2, w3, w4):
    shannon_norm = min(metrics["shannon"] / 100, 1)
    markov_norm = min(metrics["markov"] / 60, 1)
    expectation_norm = metrics["expectation"] / (metrics["expectation"] + 15)
    dcai_inverse = 1 - metrics["dcai"]

    return (
        w1 * shannon_norm +
        w2 * markov_norm +
        w3 * expectation_norm +
        w4 * dcai_inverse
    )

def random_weights():
    a = random.random()
    b = random.random()
    c = random.random()
    d = random.random()
    total = a + b + c + d
    return a/total, b/total, c/total, d/total

def constrained_weights():
    # Step 1: Fix Shannon in small band
    w_shannon = random.uniform(0.02, 0.08)

    # Step 2: Remaining weight
    remaining = 1 - w_shannon

    # Step 3: Randomly split remaining into 3 parts
    a = random.random()
    b = random.random()
    c = random.random()
    total = a + b + c

    w_markov = remaining * (a / total)
    w_expectation = remaining * (b / total)
    w_dcai = remaining * (c / total)

    return w_shannon, w_markov, w_expectation, w_dcai

results = []

for _ in range(200):  # try 100 weight combinations
    w1, w2, w3, w4 = constrained_weights()

    scores = {"weak": [], "semantic": [], "random": []}

    for pwd, metrics in raw_metrics.items():
        score = custom_score(metrics, w1, w2, w3, w4)
        scores[metrics["category"]].append(score)

    weak_avg = sum(scores["weak"]) / len(scores["weak"])
    semantic_avg = sum(scores["semantic"]) / len(scores["semantic"])
    random_avg = sum(scores["random"]) / len(scores["random"])

    separation = (random_avg - semantic_avg) + (semantic_avg - weak_avg)

    results.append({
        "weights": (w1, w2, w3, w4),
        "weak": weak_avg,
        "semantic": semantic_avg,
        "random": random_avg,
        "separation": separation
    })
    
best = max(results, key=lambda x: x["separation"])

print("Best Weights:", best["weights"])
print("Weak:", best["weak"])
print("Semantic:", best["semantic"])
print("Random:", best["random"])

weak_scores = [r["weak"] for r in results]
semantic_scores = [r["semantic"] for r in results]
random_scores = [r["random"] for r in results]

plt.plot(weak_scores, label="Weak")
plt.plot(semantic_scores, label="Semantic")
plt.plot(random_scores, label="Random")

plt.legend()
plt.title("Score Distribution Across Weight Experiments")
plt.show()