# -*- coding: utf-8 -*-
"""
Created on Sun Feb 22 13:27:08 2026

@author: Varad
"""

import json
import math
from collections import defaultdict

MODEL_FILE = "markov_model.json"

def train_markov(file_path):
    transitions = defaultdict(lambda: defaultdict(int))
    totals = defaultdict(int)

    with open(file_path, "r", encoding="latin-1", errors="ignore") as f:
        for line in f:
            pwd = line.strip()
            for i in range(len(pwd) - 1):
                a = pwd[i]
                b = pwd[i+1]
                transitions[a][b] += 1
                totals[a] += 1

    model = {}

    for a in transitions:
        model[a] = {}
        for b in transitions[a]:
            model[a][b] = transitions[a][b] / totals[a]

    return model

model = train_markov("leaked_passwords.txt")

with open(MODEL_FILE, "w") as f:
    json.dump(model, f)

print("Markov model trained and saved.")