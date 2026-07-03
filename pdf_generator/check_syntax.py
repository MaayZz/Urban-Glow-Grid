import re

with open('/Users/Abir/Desktop/innovation project/simulation/Urban_GlowGrid_Simulator.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Just a quick sanity check to see if the file is readable and no major parts are missing
if 'function buildEtoileAvenues()' in content:
    print("Etoile Avenues successfully injected.")
if 'geom.computeVertexNormals();' in content:
    print("UV Fix successfully injected.")
if 'color: 0x2b2b2c' in content:
    print("Asphalt successfully injected.")
