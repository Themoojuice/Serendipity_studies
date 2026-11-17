"""Tag beraha-2017 'scope-one-off' (protocol v1.3.2: stuttering kept as a one-off, outside the target syndromes) so the
viewer's most-compelling order doesn't lead with it."""
import json
from pathlib import Path
p = Path("data/cases.json"); d = json.loads(p.read_text())
for r in d["records"]:
    if r["id"] == "beraha-2017" and "scope-one-off" not in r["tags"]:
        r["tags"].append("scope-one-off")
p.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
print("tagged")
