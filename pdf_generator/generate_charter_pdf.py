import subprocess
import os
import sys
import shutil

HTML_FILE = "22_Urban_Glow_Grid.html"
PDF_FILE  = "22 Urban Glow Grid.pdf"

def find_chromium():
    """Find Chromium or Chrome executable on macOS / Linux."""
    candidates = [
        "chromium",
        "chromium-browser",
        "google-chrome",
        "google-chrome-stable",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ]
    for c in candidates:
        path = shutil.which(c) or (c if os.path.isfile(c) else None)
        if path:
            return path
    return None

def main():
    chromium = find_chromium()
    if not chromium:
        print("❌  Chromium / Chrome not found. Install it or add it to PATH.")
        sys.exit(1)

    html_abs  = os.path.abspath(HTML_FILE)
    pdf_abs   = os.path.abspath(PDF_FILE)
    file_url  = f"file://{html_abs}"

    print(f"🌐  Using browser : {chromium}")
    print(f"📄  Source HTML   : {html_abs}")
    print(f"📑  Output PDF    : {pdf_abs}")

    cmd = [
        chromium,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-software-rasterizer",
        f"--print-to-pdf={pdf_abs}",
        "--print-to-pdf-no-header",
        file_url,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0 and os.path.isfile(pdf_abs):
        size_kb = os.path.getsize(pdf_abs) / 1024
        print(f"✅  PDF generated successfully ({size_kb:.1f} KB)")
    else:
        print("❌  PDF generation failed.")
        if result.stderr:
            print("STDERR:", result.stderr[:1000])
        sys.exit(1)

if __name__ == "__main__":
    main()
