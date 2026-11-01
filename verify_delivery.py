from pathlib import Path
import hashlib, json, zipfile
r = Path(__file__).resolve().parent
m = json.loads((r / "DELIVERY-MANIFEST.json").read_text())
for n, h in m["files"].items():
    assert hashlib.sha256((r / n).read_bytes()).hexdigest() == h, n
f = json.loads((r / "manifests/development06-source-freeze.json").read_text())["files"]
s = r / "skills/himcm-modeling"
actual = {str(p.relative_to(s)): hashlib.sha256(p.read_bytes()).hexdigest() for p in s.rglob("*") if p.is_file() and "__pycache__" not in p.parts}
assert actual == f and len(f) == 93
status = json.loads((r / "STATUS.json").read_text())
for name, info in status["packages"].items():
    p = r / "packages" / name
    assert hashlib.sha256(p.read_bytes()).hexdigest() == info["sha256"]
    with zipfile.ZipFile(p) as z:
        assert z.testzip() is None and len(z.namelist()) == info["files"]
        if info["files"] == 93:
            assert {n.removeprefix("himcm-modeling/"): hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist()} == f
print(f"PASS: {len(m['files'])} delivery files; 93 exact source files; both original ZIPs verified")
