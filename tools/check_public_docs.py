"""Check published portfolio documents without application dependencies."""
from pathlib import Path
import re
import sys
root=Path(__file__).resolve().parents[1]
errors=[]
for name,low in (("README.md",650),("ARCHITECTURE.md",1100),("ROADMAP.md",350)):
    f=root/name
    if not f.is_file():errors.append("Missing "+name);continue
    text=f.read_text(encoding="utf-8")
    if len(text)<low:errors.append("Too short "+name)
    for link in re.findall(r"\]\(([^)]+)\)",text):
        href=link.split("#")[0]
        if href and not href.startswith(("https://","http://","mailto:")):
            target=(root/href).resolve()
            if not target.is_relative_to(root.resolve()) or not target.is_file():errors.append("Broken "+link)
    if re.search(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----",text):
        errors.append("Private-key-looking content "+name)
if (root/"ARCHITECTURE.md").is_file() and "mermaid" not in (root/"ARCHITECTURE.md").read_text(encoding="utf-8"):
    errors.append("Missing architecture diagram")
if errors:
    for e in errors:print("FAIL:",e,file=sys.stderr)
    sys.exit(1)
print("PASS: documentation, local links and basic secret patterns")
