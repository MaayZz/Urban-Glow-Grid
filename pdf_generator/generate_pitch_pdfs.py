import subprocess, sys, os

files = [
    ("Pitch_Recruit_Slides.html",  "Pitch_Recruit_Slides.pdf"),
    ("Pitch_Recruit_Script.html",  "Pitch_Recruit_Script.pdf"),
]

base = "/Users/Abir/Desktop/innovation project"

for html, pdf in files:
    inp = os.path.join(base, html)
    out = os.path.join(base, pdf)
    result = subprocess.run(
        ["python3", "-c", f"""
import sys
try:
    from weasyprint import HTML
    HTML(filename=r'{inp}').write_pdf(r'{out}')
    print("OK:", r'{out}')
except Exception as e:
    print("FAIL weasyprint:", e)
    sys.exit(1)
"""],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
