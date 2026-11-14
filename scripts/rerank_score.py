"""Score title+abstract text with the saved v1.3 re-ranking classifier (queries/rerank_model_v1.json).

Same arithmetic as scikit-learn's TfidfVectorizer (token [a-z]{2,}, 1-2-grams, sublinear tf, l2 norm) followed by the
logistic-regression decision function, so scores match the browser scorer used in earlier rounds.

    from rerank_score import score
    score(title, abstract)  -> float (higher = more likely relevant)
"""
import json
import math
import re
from collections import Counter
from pathlib import Path

_M = json.loads((Path(__file__).resolve().parent.parent / "queries" / "rerank_model_v1.json").read_text())
_TOK = re.compile(_M["token"])
_TERMS = _M["terms"]


def score(title, abstract=""):
    toks = _TOK.findall(f"{title or ''} {abstract or ''}".lower())
    grams = Counter(t for t in toks + [f"{a} {b}" for a, b in zip(toks, toks[1:])] if t in _TERMS)
    num = ss = 0.0
    for g, tf in grams.items():
        idf, coef = _TERMS[g]
        w = (1 + math.log(tf)) * idf
        num += w * coef
        ss += w * w
    return (num / math.sqrt(ss) if ss else 0.0) + _M["intercept"]
