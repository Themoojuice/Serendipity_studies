"""Train the tail re-ranker (protocol v1.3, 2026-11-10).

Priority screening for the unscreened tail of the Europe PMC broad set: a TF-IDF + logistic regression
classifier trained on our own decisions, exported as plain JSON so the laptop browser can score records as they
are fetched (no abstracts are stored or committed; only term weights).

  Positives: library case records (title + abstract fetched from Europe PMC), minus three held-out cases that
             sit deep in the old ranking (kraft-westman-2009 rank 6,182; solyom-1987 batch 2 rank 7,808;
             makris-2021 rank 9,842), used to test the new ranking.
  Negatives: records screened and excluded in phase 1c (title + abstract in /home/claude/work/raw/*.json).

usage: python3 scripts/rerank_train.py LIBTXT_FILE   (the browser export of library titles and abstracts)
writes queries/rerank_model_v1.json and prints cross-validated performance.
"""
import csv
import glob
import json
import sys
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold

HOLDOUT = {"kraft-westman-2009", "solyom-1987", "makris-2021"}
TOKEN = r"[a-z]{2,}"


def text(title, abs_):
    return f"{title or ''} {abs_ or ''}".lower()


def main(libfile):
    dec = json.JSONDecoder()
    lib = json.loads(dec.raw_decode(json.load(open(libfile))[0]["text"])[0])
    pos = [text(r["title"], r["abs"]) for r in lib if r["id"] not in HOLDOUT]

    rows = list(csv.DictReader(open("ledger/records.csv")))
    sup = {r["supersedes"] for r in rows if r["supersedes"]}
    cur = {r["other_id"]: r["decision"] for r in rows if r["record_id"] not in sup and r["query_id"] == "EPMC_broad_v1_2"}
    neg, seen = [], set()
    for f in glob.glob("/home/claude/work/raw/*.json"):
        try:
            data = json.load(open(f))
        except Exception:
            continue
        if not (isinstance(data, list) and data and isinstance(data[0], dict) and "abs" in data[0] and "key" in data[0]):
            continue
        for r in data:
            if r["key"] in seen or cur.get(r["key"]) != "excluded":
                continue
            seen.add(r["key"])
            neg.append(text(r["title"], r["abs"]))
    X_txt = pos + neg
    y = np.array([1] * len(pos) + [0] * len(neg))
    print(f"training: {len(pos)} positives, {len(neg)} negatives")

    def model():
        return (TfidfVectorizer(token_pattern=TOKEN, ngram_range=(1, 2), min_df=3, max_features=20000, sublinear_tf=True),
                LogisticRegression(C=4.0, class_weight="balanced", max_iter=3000))

    # 5-fold cross-validation: AUC and how deep the positives sit
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=20261110)
    scores = np.zeros(len(y))
    for tr, te in skf.split(X_txt, y):
        vec, clf = model()
        Xtr = vec.fit_transform([X_txt[i] for i in tr])
        clf.fit(Xtr, y[tr])
        scores[te] = clf.decision_function(vec.transform([X_txt[i] for i in te]))
    auc = roc_auc_score(y, scores)
    negs = np.sort(scores[y == 0])[::-1]
    pct = [float((negs > s).mean()) for s in scores[y == 1]]
    print(f"CV AUC {auc:.3f}; positives ranked above this share of negatives: median {1 - np.median(pct):.3f}, "
          f"in top 5% of negatives: {np.mean(np.array(pct) < 0.05):.2f}, top 10%: {np.mean(np.array(pct) < 0.10):.2f}")

    vec, clf = model()
    clf.fit(vec.fit_transform(X_txt), y)
    vocab = vec.vocabulary_
    terms = sorted(vocab, key=vocab.get)
    out = {"version": "rerank_v1", "trained": "2026-11-10", "token": TOKEN, "ngram": [1, 2], "sublinear_tf": True, "norm": "l2",
           "intercept": float(clf.intercept_[0]), "n_pos": len(pos), "n_neg": len(neg), "cv_auc": round(auc, 4),
           "holdout": sorted(HOLDOUT),
           "terms": {t: [round(float(vec.idf_[vocab[t]]), 4), round(float(clf.coef_[0][vocab[t]]), 4)] for t in terms}}
    Path("queries/rerank_model_v1.json").write_text(json.dumps(out, separators=(",", ":")))
    top = sorted(terms, key=lambda t: clf.coef_[0][vocab[t]])
    print("most positive terms:", ", ".join(top[-25:][::-1]))
    print("most negative terms:", ", ".join(top[:15]))


if __name__ == "__main__":
    main(sys.argv[1])
