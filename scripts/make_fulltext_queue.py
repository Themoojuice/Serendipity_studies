"""Write docs/fulltext_queue.md: every case not yet fully coded, grouped by how its full text can be reached.
Run from the repo root after a coding batch:  python3 scripts/make_fulltext_queue.py
"""
import json
from pathlib import Path

d = json.loads(Path("data/cases.json").read_text())
H = {e["case_id"] for e in json.loads(Path("data/hypotheses.json").read_text())["entries"]}
cases = [r for r in d["records"] if r["record_type"] == "case"]
todo = [r for r in cases if r["id"] not in H]

# Free copies that exist but sit behind a bot check or sign-up in the app's browser (2026-11-17); one click in a normal browser
EASY = {
    "klok-2025": "Edinburgh repository PDF (Cloudflare check in the app's browser)",
    "kalenderoglu-2011": "Türkiye Klinikleri PDF (Cloudflare check)",
    "de-filippis-2026": "Preprints.org (refused the app's browser: Access Denied)",
    "berner-2008": "Free PDF at psychiatrist.com after a free account",
    "richards-2024": "Free PDF at psychiatrist.com after a free account",
    "colli-2003": "Free in the Journal of Near-Death Studies archive at UNT Digital Library (doi.org/10.17514/jnds-2003-22-1-p33-55); it shows an 'I'm not a robot' box, which Claude leaves to you",
    "van-den-hoven-2021": "Free in the Netherlands Journal of Critical Care 2021;29(5):222-5 (njcc.nl; its security certificate failed in the app's browser)",
    "nagata-2013": "Open access (OpenAlex, 22 Nov), but International Psychogeriatrics has moved to ScienceDirect, which puts a Cloudflare check in front of Claude's browser",
    "de-santis-1997": "Free to read at Wiley (OpenAlex, 22 Nov); Wiley's bot check stops Claude's browser",
    "collyer-2020": "Open access at ScienceDirect (OpenAlex, 22 Nov); Cloudflare check in Claude's browser",
    "morena-1994": "Free to read at ScienceDirect (OpenAlex, 22 Nov); Cloudflare check in Claude's browser",
    "taira-2003": "thejns.org refused the app's browser",
}
NOTES = {
    "CKN, Ovid / Lippincott (works once signed in)": "Not all of these are in CKN's Ovid subscription (Journal of Psychiatric Practice wasn't). <a href=\"https://libkey.io/libraries/2947\">LibKey</a> (libkey.io/libraries/2947/ followed by the DOI) shows in one click whether CKN has the article.",
    "Download the PDF yourself (Elsevier: Cloudflare in the app's browser)": "Most Elsevier psychiatry journals are in ClinicalKey through CKN, which worked on 17 November (11 coded that way). These eight weren't found there, so they need ScienceDirect, which stops the app's browser at a Cloudflare check.",
    "Psychiatry Online (tick the terms box)": "The terms box only appears when you arrive through a CKN link, not when you go to psychiatryonline.org directly. Tap a CKN link below and sign in to CKN; Psychiatry Online then shows a page titled <b>SAML Login</b> with the sentence <i>I have read and agree to the Terms and Conditions and Privacy Policy</i> and <b>Yes</b> / <b>No</b> buttons. Tap <b>Yes</b>. (Claude isn't allowed to accept terms for you, so it stopped there.) Since 18 November the site also puts a Cloudflare check in front of the app's browser.",
}
ROUTES = [
    ("Psychiatry Online (tick the terms box)", ("10.1176/",)),
    ("CKN, Ovid / Lippincott (works once signed in)", ("10.1097/",)),
    ("CKN, Springer (works once signed in)", ("10.1007/",)),
    ("Download the PDF yourself (Elsevier: Cloudflare in the app's browser)", ("10.1016/",)),
    ("Download the PDF yourself (Wiley)", ("10.1002/", "10.1111/", "10.1046/")),
    ("Download the PDF yourself (SAGE / Mary Ann Liebert)", ("10.1177/", "10.1089/")),
    ("Download the PDF yourself (Taylor & Francis / Informa)", ("10.1080/", "10.3109/")),
    ("Physicians Postgraduate Press (psychiatrist.com)", ("10.4088/",)),
    ("Thieme / Karger / AMA / AAN / BMJ / JNS / other", ("10.1055/", "10.1159/", "10.1001/", "10.1212/", "10.1136/", "10.3171/", "10.1161/", "10.1053/", "10.1227/", "10.2190/", "10.1192/", "10.1017/")),
]

import json as _json
_accp = Path("queries/fulltext_access_v1.json")
ACCESS = _json.loads(_accp.read_text())["results"] if _accp.exists() else {}
def access_note(r):
    a = ACCESS.get(r["id"])
    return f"CKN check 22 Nov: {a[1]}" if a else ""

def line(r):
    c = r["citation"]
    au = (c.get("authors") or [c.get("first_author", "")])[0] if isinstance(c.get("authors"), list) else c.get("first_author", "")
    doi = r["ids"].get("doi")
    links = []
    if r["links"].get("ckn"): links.append(f"[CKN]({r['links']['ckn']})")
    if doi: links.append(f"[DOI](https://doi.org/{doi})")
    if r["links"].get("abstract"): links.append(f"[PubMed]({r['links']['abstract']})")
    acc = access_note(r)
    return f"- **{r['id']}** · tier {r['tier']} · {c['title']} ({c.get('journal', '')} {c.get('year', '')}) · " + " · ".join(links) + (f" · *{acc}*" if acc else "")

out = ["# Full texts still needed", "",
       f"{len(todo)} of {len(cases)} cases aren't fully coded yet because their full text couldn't be reached from this session "
       "(written by `scripts/make_fulltext_queue.py`). Each needs a read and a coding batch (`protocol/SCHEMA.md` §7). "
       "Easy wins first: free copies that only a bot check stood in front of.", ""]
done = set()
easy = [r for r in todo if r["id"] in EASY]
if easy:
    out += [f"## Easy wins: free, one click in a normal browser ({len(easy)})", ""]
    out += [line(r) + f" · *{EASY[r['id']]}*" for r in sorted(easy, key=lambda r: r["tier"])] + [""]
    done |= {r["id"] for r in easy}
for title, prefixes in ROUTES:
    rs = [r for r in todo if r["id"] not in done and (r["ids"].get("doi") or "").lower().startswith(prefixes)]
    if not rs: continue
    out += [f"## {title} ({len(rs)})", ""] + [line(r) for r in sorted(rs, key=lambda r: (r["tier"], r["id"]))] + [""]
    done |= {r["id"] for r in rs}
rest = [r for r in todo if r["id"] not in done]
nodoi = [r for r in rest if not r["ids"].get("doi")]
other = [r for r in rest if r["ids"].get("doi")]
if other:
    out += [f"## Other publishers ({len(other)})", ""] + [line(r) for r in sorted(other, key=lambda r: (r["tier"], r["id"]))] + [""]
if nodoi:
    out += [f"## No DOI: older or non-indexed papers, library or interlibrary loan ({len(nodoi)})", ""] + [line(r) for r in sorted(nodoi, key=lambda r: (r["tier"], r["id"]))] + [""]
import csv as _csv
from urllib.parse import quote as _q
_rows = list(_csv.DictReader(Path("ledger/records.csv").open()))
_sup = {x["supersedes"] for x in _rows if x["supersedes"]}
UNSURE_NOTES = {  # by DOI: free copies behind bot checks (OpenAlex, 22 Nov)
    "10.3109/02699052.2016.1162060": "Free accepted manuscript in the University of Udine repository (air.uniud.it); Cloudflare check in Claude's browser",
    "10.1176/appi.neuropsych.16030053": "Free to read at Psychiatry Online; Cloudflare check in Claude's browser",
}
unsure, _seen = [], set()
for x in _rows:
    if x["record_id"] in _sup or x["decision"] != "unsure":
        continue
    key = x["doi"] or x["pmid"] or x["title"].lower()[:80]
    if key in _seen:
        continue
    _seen.add(key)
    unsure.append(x)
unsure.sort(key=lambda x: (x["year"] or "0"))
def uline(x):
    links = []
    if x["doi"]:
        links += [f"[CKN](https://go.openathens.net/redirector/ckn.qldhealth.com?url={_q('https://doi.org/' + x['doi'], safe='')})", f"[DOI](https://doi.org/{x['doi']})"]
    if x["pmid"]:
        links.append(f"[PubMed](https://pubmed.ncbi.nlm.nih.gov/{x['pmid']}/)")
    note = " · ".join(n for n in (UNSURE_NOTES.get(x["doi"], ""), (lambda a: f"CKN check 22 Nov: {a[1]}" if a else "")(ACCESS.get("doi:" + x["doi"]) or ACCESS.get("pmid:" + x["pmid"]) or ACCESS.get("rid:" + x["record_id"]))) if n)
    return f"- **{x['record_id']}** · {x['title']} ({x['journal']} {x['year']}) · " + " · ".join(links) + (f" · *{note}*" if note else "")
if unsure:
    out += [f"## Unsure screening records: full text decides whether they're cases ({len(unsure)})", ""] + [uline(x) for x in unsure] + [""]
Path("docs/fulltext_queue.md").write_text("\n".join(out) + "\n")

# --- the same list as a page on the site (queue.html), so it opens on a phone ---
import html as _h
def hl(r, extra=""):
    c = r["citation"]; doi = r["ids"].get("doi")
    links = []
    if r["links"].get("ckn"): links.append(f'<a href="{_h.escape(r["links"]["ckn"])}">CKN</a>')
    if doi: links.append(f'<a href="https://doi.org/{_h.escape(doi)}">DOI</a>')
    if r["links"].get("abstract"): links.append(f'<a href="{_h.escape(r["links"]["abstract"])}">PubMed</a>')
    extra = " · ".join(x for x in (extra, access_note(r)) if x)
    ex = f'<div class="ex">{_h.escape(extra)}</div>' if extra else ""
    return (f'<li><div class="t">{_h.escape(c["title"])}</div><div class="m">{_h.escape(c.get("journal",""))} {c.get("year","")} · tier {r["tier"]} · <code>{r["id"]}</code></div>'
            f'{ex}<div class="l">{" · ".join(links)}</div></li>')
secs = []
def sec(title, rs, note="", extras=None):
    if not rs: return
    items = "".join(hl(r, (extras or {}).get(r["id"], "")) for r in rs)
    secs.append(f'<section><h2>{_h.escape(title)} <span>{len(rs)}</span></h2>' + (f'<p class="note">{note}</p>' if note else "") + f'<ol>{items}</ol></section>')
sec("Easy wins: free, one click in a normal browser", sorted(easy, key=lambda r: r["tier"]), "Free copies that only a bot check or a free sign-up stood in front of.", EASY)
seen = {r["id"] for r in easy}
for title, prefixes in ROUTES:
    rs = [r for r in todo if r["id"] not in seen and (r["ids"].get("doi") or "").lower().startswith(prefixes)]
    sec(title, sorted(rs, key=lambda r: (r["tier"], r["id"])), NOTES.get(title, ""))
    seen |= {r["id"] for r in rs}
sec("Other publishers", sorted([r for r in todo if r["id"] not in seen and r["ids"].get("doi")], key=lambda r: (r["tier"], r["id"])))
sec("No DOI: older or non-indexed papers (library or interlibrary loan)", sorted([r for r in todo if r["id"] not in seen and not r["ids"].get("doi")], key=lambda r: (r["tier"], r["id"])))
def uhl(x):
    links = []
    if x["doi"]:
        links += [f'<a href="https://go.openathens.net/redirector/ckn.qldhealth.com?url={_q("https://doi.org/" + x["doi"], safe="")}">CKN</a>', f'<a href="https://doi.org/{_h.escape(x["doi"])}">DOI</a>']
    if x["pmid"]:
        links.append(f'<a href="https://pubmed.ncbi.nlm.nih.gov/{x["pmid"]}/">PubMed</a>')
    note = " · ".join(n for n in (UNSURE_NOTES.get(x["doi"], ""), (lambda a: f"CKN check 22 Nov: {a[1]}" if a else "")(ACCESS.get("doi:" + x["doi"]) or ACCESS.get("pmid:" + x["pmid"]) or ACCESS.get("rid:" + x["record_id"]))) if n)
    ex = f'<div class="ex">{_h.escape(note)}</div>' if note else ""
    return (f'<li><div class="t">{_h.escape(x["title"])}</div><div class="m">{_h.escape(x["journal"])} {x["year"]} · <code>{x["record_id"]}</code></div>'
            f'{ex}<div class="l">{" · ".join(links) or "no link: library or interlibrary loan"}</div></li>')
if unsure:
    secs.append(f'<section><h2>Unsure screening records <span>{len(unsure)}</span></h2><p class="note">Not cases yet: the full text decides whether each one is a case or an exclusion.</p><ol>' + "".join(uhl(x) for x in unsure) + "</ol></section>")
page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Full texts still needed · Serendipity library</title>
<style>
:root {{ --bg:#faf9f5; --ink:#1f1e1d; --muted:#6b6862; --line:#e6e2d8; --accent:#c96442; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#1f1e1d; --ink:#f0eee6; --muted:#a8a49b; --line:#3a3835; --accent:#e08a6a; }} }}
body {{ margin:0; background:var(--bg); color:var(--ink); font:16px/1.5 -apple-system, "Segoe UI", Roboto, sans-serif; }}
main {{ max-width:760px; margin:0 auto; padding:20px 16px 60px; }}
h1 {{ font-size:24px; margin:8px 0 4px; }} h2 {{ font-size:18px; margin:28px 0 6px; border-top:1px solid var(--line); padding-top:16px; }}
h2 span {{ color:var(--muted); font-weight:400; }} .lede, .note, .m, .ex {{ color:var(--muted); }} .note {{ font-size:14px; }}
ol {{ padding-left:22px; }} li {{ margin:0 0 14px; }} .t {{ font-weight:600; }} .m, .ex {{ font-size:13px; }} .l {{ font-size:14px; }}
a {{ color:var(--accent); }} code {{ font-size:12px; }}
</style></head><body><main>
<p><a href="./">← Back to the library</a></p>
<h1>Full texts still needed</h1>
<p class="lede">{len(todo)} of {len(cases)} cases aren't fully coded yet, because Claude couldn't reach their full text. Grouped by how to get each one, easiest first. Send a PDF (or sign in to CKN and say so) and Claude codes it. Regenerated by <code>scripts/make_fulltext_queue.py</code> with every coding batch.</p>
{''.join(secs)}
</main></body></html>
"""
Path("queue.html").write_text(page)
print(f"{len(todo)} cases listed (docs/fulltext_queue.md and queue.html)")
