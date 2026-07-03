import asyncio
from playwright.async_api import async_playwright
import os
from pathlib import Path

PENROSE_SVG = """<svg viewBox="0 0 500 440" xmlns="http://www.w3.org/2000/svg" style="width: 100%; height: 100%;">
  <defs>
    <linearGradient id="face1-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#059669" />
      <stop offset="100%" stop-color="#047857" />
    </linearGradient>
    <linearGradient id="face2-grad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#064e3b" />
      <stop offset="100%" stop-color="#022c22" />
    </linearGradient>
    <linearGradient id="face3-grad" x1="100%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#34d399" />
      <stop offset="100%" stop-color="#10b981" />
    </linearGradient>
  </defs>
  <path d="M211,134 l38,66 L154,365 H496 L458,431 H40 Z" fill="url(#face1-grad)" />
  <path d="M211,2 L2,365 l38,66 L211,134 l95,165 h76 Z" fill="url(#face2-grad)" />
  <path d="M496,365 L287,2 H211 L382,299 H192 Z" fill="url(#face3-grad)" />
</svg>"""

HTML_CONTENT = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Urban Glow Grid — Mid-term Presentation</title>
  <style>
    /* ============================================================
       GUIDELINES-INSPIRED HIGH-IMPACT LIGHT THEME
       ============================================================ */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800;900&display=swap');

    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    @page {{
      size: A4 landscape;
      margin: 0;
    }}

    body {{
      margin: 0;
      padding: 0;
      background: #e2e8f0; /* Desktop backdrop */
      color: #1e293b;
      font-family: 'Plus Jakarta Sans', sans-serif;
      line-height: 1.4;
      width: 297mm;
      height: 210mm;
      overflow: hidden;
    }}

    .slide {{
      width: 297mm;
      height: 210mm;
      padding: 18mm 22mm 14mm 22mm;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      background: #f4f8f6; /* Off-white/mint background canvas */
      /* Soft emerald radial gradients simulating the guidelines PDF glow */
      background-image: 
        radial-gradient(circle at 85% 15%, rgba(16, 185, 129, 0.12) 0%, transparent 55%),
        radial-gradient(circle at 15% 85%, rgba(5, 150, 105, 0.08) 0%, transparent 55%);
      border: 1px solid rgba(16, 185, 129, 0.15);
      page-break-after: always;
      box-sizing: border-box;
      overflow: hidden;
    }}

    .slide:last-child {{
      page-break-after: avoid;
    }}

    /* Print styling to strip margins and disable shadows/filters to prevent solid gray rectangle bugs */
    @media print {{
      body {{ background: transparent; }}
      .slide {{ border: none; }}
      .card, .photo-container, .closing-card, table, .tag {{
        box-shadow: none !important;
      }}
      .cover-penrose, .penrose-bg-watermark svg {{
        filter: none !important;
      }}
    }}

    /* Subtle Penrose Background Watermark */
    .penrose-bg-watermark {{
      position: absolute;
      right: -30px;
      bottom: 25px;
      width: 240px;
      height: 240px;
      opacity: 0.05;
      pointer-events: none;
      z-index: 0;
    }}

    /* ── HEADER ── */
    .header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid rgba(16, 185, 129, 0.15);
      padding-bottom: 8px;
      margin-bottom: 12px;
      z-index: 2;
    }}

    .header h2 {{
      font-family: 'Outfit', sans-serif;
      font-size: 21pt;
      font-weight: 700;
      color: #064e3b;
      display: flex;
      align-items: center;
      gap: 10px;
      letter-spacing: -0.5px;
    }}

    .header-icon {{
      color: #10b981;
      width: 26px;
      height: 26px;
      stroke-width: 2.2;
    }}

    .header .slide-meta {{
      font-size: 9pt;
      font-weight: 700;
      color: #059669;
      text-transform: uppercase;
      letter-spacing: 1px;
    }}

    /* ── FOOTER ── */
    .footer {{
      display: flex;
      justify-content: space-between;
      border-top: 1px solid rgba(16, 185, 129, 0.15);
      padding-top: 8px;
      margin-top: 10px;
      font-size: 8.5pt;
      color: #64748b;
      font-weight: 600;
      z-index: 2;
    }}

    .footer-brand {{
      font-family: 'Outfit', sans-serif;
      font-weight: 800;
      color: #064e3b;
      text-transform: uppercase;
      letter-spacing: 1.5px;
    }}

    /* ── COVER SLIDE LAYOUT ── */
    .cover-layout {{
      display: grid;
      grid-template-columns: 1.25fr 0.75fr;
      gap: 30px;
      align-items: center;
      flex: 1;
      width: 100%;
      height: 100%;
      margin: 10px 0;
      z-index: 2;
    }}

    .cover-left {{
      display: flex;
      flex-direction: column;
      justify-content: center;
      height: 100%;
    }}

    .cover-right {{
      display: flex;
      justify-content: center;
      align-items: center;
      position: relative;
      height: 100%;
    }}

    .cover-glow {{
      position: absolute;
      width: 320px;
      height: 320px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(16, 185, 129, 0.18) 0%, rgba(244, 248, 246, 0) 70%);
      z-index: 1;
    }}

    .cover-penrose {{
      width: 290px;
      height: 290px;
      z-index: 2;
      filter: drop-shadow(0 10px 20px rgba(0, 0, 0, 0.08));
    }}

    .cover-eyebrow {{
      font-family: 'Outfit', sans-serif;
      font-size: 10.5pt;
      font-weight: 800;
      color: #10b981;
      text-transform: uppercase;
      letter-spacing: 3px;
      margin-bottom: 12px;
    }}

    .cover-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 48pt;
      font-weight: 900;
      color: #064e3b;
      line-height: 1.05;
      letter-spacing: -2px;
      margin-bottom: 14px;
    }}

    .cover-subtitle {{
      font-size: 14pt;
      color: #475569;
      font-weight: 500;
      margin-bottom: 24px;
      line-height: 1.4;
      letter-spacing: -0.2px;
    }}

    .cover-tags {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 30px;
    }}

    .tag {{
      padding: 6px 14px;
      border-radius: 99px;
      font-size: 8.5pt;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      border: 1px solid rgba(16, 185, 129, 0.2);
      background: rgba(16, 185, 129, 0.05);
      color: #065f46;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
    }}

    .tag-accent-green {{
      background: #d1fae5;
      color: #065f46;
      border-color: #a7f3d0;
    }}

    .tag-accent-cyan {{
      background: #e0f2fe;
      color: #0369a1;
      border-color: #bae6fd;
    }}

    .team-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      width: 100%;
      border-top: 1.5px solid rgba(16, 185, 129, 0.15);
      padding-top: 16px;
    }}

    .team-member {{
      display: flex;
      flex-direction: column;
    }}

    .team-name {{
      font-family: 'Outfit', sans-serif;
      font-size: 9.5pt;
      font-weight: 800;
      color: #064e3b;
    }}

    .team-role {{
      font-size: 8pt;
      color: #475569;
      margin-top: 3px;
      line-height: 1.3;
    }}

    /* ── LAYOUT SYSTEMS ── */
    .grid-2col {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
      flex: 1;
      margin: 10px 0;
      z-index: 2;
    }}

    .col {{
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      height: 100%;
    }}

    .section-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 10.5pt;
      font-weight: 700;
      color: #064e3b;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 10px;
      border-bottom: 1.5px solid rgba(16, 185, 129, 0.15);
      padding-bottom: 4px;
    }}

    /* ── CONTENT CARDS ── */
    .card {{
      background: #ffffff;
      border-radius: 20px;
      padding: 16px 20px;
      border: 1px solid rgba(16, 185, 129, 0.12);
      box-shadow: 0 6px 16px rgba(0, 0, 0, 0.03);
      margin-bottom: 12px;
    }}

    .card h4 {{
      font-family: 'Outfit', sans-serif;
      font-size: 11pt;
      font-weight: 700;
      color: #064e3b;
      margin-bottom: 6px;
      letter-spacing: -0.2px;
    }}

    .card p {{
      font-size: 9.5pt;
      color: #334155;
      line-height: 1.45;
    }}

    /* ── BULLET LISTS ── */
    .bullet-list {{
      list-style-type: square;
      padding-left: 20px;
      margin-bottom: 10px;
    }}

    .bullet-list li {{
      font-size: 10pt;
      color: #334155;
      margin-bottom: 12px;
      line-height: 1.5;
    }}

    .bullet-list li::marker {{
      color: #10b981;
      font-size: 1.1em;
    }}

    .bullet-list li b {{
      color: #064e3b;
      font-weight: 700;
    }}

    /* ── TABLES ── */
    table {{
      width: 100%;
      border-collapse: separate;
      border-spacing: 0;
      font-size: 8.5pt;
      margin-top: 4px;
      border-radius: 12px;
      overflow: hidden;
      border: 1px solid rgba(16, 185, 129, 0.15);
    }}

    th {{
      background: #e6f4ea;
      color: #064e3b;
      font-family: 'Outfit', sans-serif;
      font-weight: 700;
      padding: 6px 10px;
      text-align: left;
    }}

    td {{
      border-bottom: 1px solid rgba(16, 185, 129, 0.08);
      padding: 6px 10px;
      color: #334155;
      background: #ffffff;
    }}

    tr:last-child td {{
      border-bottom: none;
    }}

    .total-row td {{
      font-weight: 800;
      background: #d1fae5;
      color: #064e3b;
      border-top: 1.5px solid rgba(16, 185, 129, 0.25);
    }}

    /* ── REAL PHOTO CONTAINERS ── */
    .photo-container {{
      position: relative;
      flex: 1;
      width: 100%;
      height: 100%;
      min-height: 280px;
      border: 1px solid rgba(16, 185, 129, 0.15);
      border-radius: 20px;
      overflow: hidden;
      box-shadow: 0 6px 16px rgba(0, 0, 0, 0.03);
      display: flex;
      justify-content: center;
      align-items: center;
      background: #ffffff;
    }}

    .slide-photo {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}

    .photo-caption {{
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: rgba(6, 78, 59, 0.85); /* Semi-transparent forest green */
      backdrop-filter: blur(4px);
      -webkit-backdrop-filter: blur(4px);
      color: #ffffff;
      font-size: 8.5pt;
      font-weight: 600;
      padding: 8px 12px;
      text-align: center;
      border-top: 1px solid rgba(16, 185, 129, 0.25);
      font-family: 'Plus Jakarta Sans', sans-serif;
      z-index: 3;
    }}

    /* ── CONCLUSION SLIDE ── */
    .closing-content {{
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
      z-index: 2;
    }}

    .closing-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 42pt;
      font-weight: 900;
      color: #064e3b;
      margin-bottom: 6px;
      letter-spacing: -1.5px;
    }}

    .closing-subtitle {{
      font-family: 'Outfit', sans-serif;
      font-size: 12pt;
      color: #10b981;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 3px;
      margin-bottom: 30px;
    }}

    .closing-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
      width: 100%;
      max-width: 900px;
    }}

    .closing-card {{
      border: 1px solid rgba(16, 185, 129, 0.15);
      background: #ffffff;
      padding: 16px 20px;
      border-radius: 20px;
      text-align: left;
      box-shadow: 0 6px 16px rgba(0, 0, 0, 0.03);
    }}

    .closing-card h4 {{
      font-family: 'Outfit', sans-serif;
      font-size: 11pt;
      color: #064e3b;
      margin-bottom: 6px;
      font-weight: 700;
      letter-spacing: -0.2px;
    }}

    .closing-card p {{
      font-size: 9pt;
      color: #334155;
      line-height: 1.45;
    }}
  </style>
</head>
<body>

  <!-- ==========================================
       SLIDE 1: COVER
       ========================================== -->
  <div class="slide" id="slide1">
    <div class="cover-layout">
      <div class="cover-left">
        <div class="cover-eyebrow">✦ Mid-term Showcase Checkpoint</div>
        <h1 class="cover-title">Urban Glow Grid</h1>
        <div class="cover-subtitle">An IoT-Powered Interactive City Energy Stabilization Game</div>
        
        <div class="cover-tags">
          <span class="tag tag-accent-green">⚡ SDG 7: Clean Energy</span>
          <span class="tag tag-accent-cyan">🏙️ SDG 11: Sustainable Cities</span>
          <span class="tag">⚙️ Physical Prototyping</span>
          <span class="tag">Team 22</span>
        </div>

        <div class="team-grid">
          <div class="team-member">
            <span class="team-name">Abir ISLAM</span>
            <span class="team-role">CEO / COO · Lead &amp; Operations</span>
          </div>
          <div class="team-member">
            <span class="team-name">Sofiane LACCHAB</span>
            <span class="team-role">CTO · Hardware &amp; Firmware</span>
          </div>
          <div class="team-member">
            <span class="team-name">Mohamed MELLOUK</span>
            <span class="team-role">Creative Director · Design &amp; Maquette</span>
          </div>
          <div class="team-member">
            <span class="team-name">Ismail MABROUKI</span>
            <span class="team-role">Sustainability Analyst · SDGs &amp; Impact</span>
          </div>
        </div>
      </div>
      
      <div class="cover-right">
        <div class="cover-glow"></div>
        <div class="cover-penrose">
          {PENROSE_SVG}
        </div>
      </div>
    </div>
    
    <div class="footer">
      <span class="footer-brand">Urban Glow Grid</span>
      <div>UTSEUS 2026 · Page 1 of 6</div>
    </div>
  </div>

  <!-- ==========================================
       SLIDE 2: CONCEPT & VISION
       ========================================== -->
  <div class="slide" id="slide2">
    <div class="penrose-bg-watermark">
      {PENROSE_SVG}
    </div>
    
    <div class="header">
      <h2>
        <svg class="header-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A5 5 0 0 0 8 8c0 1 .3 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/></svg>
        <span>Concept &amp; Educational Vision</span>
      </h2>
      <div class="slide-meta">Project Overview &amp; Research</div>
    </div>

    <div class="grid-2col">
      <div class="col">
        <div class="section-title">The Energy Abstraction Problem</div>
        <div class="card">
          <h4>Invisible Grid strain</h4>
          <p>
            Standard electricity billing is delayed and abstract. Citizens do not feel the immediate stress that peak-hour behaviors place on the grid.
          </p>
        </div>
        <div class="card">
          <h4>The Gamified Solution</h4>
          <p>
            A physical, interactive model of Paris. Translates complex electrical loads into intuitive physical dials and lighting feedback.
          </p>
        </div>
      </div>

      <div class="col">
        <div class="section-title">Research &amp; Evidence-Based Design</div>
        <ul class="bullet-list">
          <li>
            <b>RTE EcoWatt Grid Alerts:</b> Warning colors (green, yellow, red) are directly modeled on France's real-time national grid strain system.
          </li>
          <li>
            <b>ADEME Smart Grid Research:</b> Shift-on-demand mechanics demonstrate how shedding non-essential loads off-peak reduces grid failure risks.
          </li>
          <li>
            <b>SDG Alignment:</b> Promotes energy conservation (<b>SDG 7</b>) and resource prioritization (<b>SDG 11</b>) through active play.
          </li>
        </ul>
      </div>
    </div>

    <div class="footer">
      <span class="footer-brand">Urban Glow Grid</span>
      <div>UTSEUS 2026 · Page 2 of 6</div>
    </div>
  </div>

  <!-- ==========================================
       SLIDE 3: PHYSICAL DESIGN
       ========================================== -->
  <div class="slide" id="slide3">
    <div class="penrose-bg-watermark">
      {PENROSE_SVG}
    </div>

    <div class="header">
      <h2>
        <svg class="header-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="9" y1="3" x2="9" y2="21"/><line x1="15" y1="3" x2="15" y2="21"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="3" y1="15" x2="21" y2="15"/></svg>
        <span>Physical Design — La Maquette</span>
      </h2>
      <div class="slide-meta">Maquette Shell &amp; Layout</div>
    </div>

    <div class="grid-2col">
      <div class="col">
        <div class="section-title">Design Philosophy &amp; Strategy</div>
        <ul class="bullet-list">
          <li>
            <b>Electronics Separation:</b> Maquette is built independent of the controller board. Protects structural design from continuous circuit iterations.
          </li>
          <li>
            <b>Laser-Engraved Plywood Grid:</b> Baseboard features a vector-etched map of Paris divided into 6 distinct energy sectors.
          </li>
          <li>
            <b>Translucent Filament Landmarks:</b> Eiffel Tower, hospitals, and schools printed in translucent plastic to act as natural diffusers.
          </li>
          <li>
            <b>Dynamic Glow:</b> Internal NeoPixels scatter light through structures to represent district energy states.
          </li>
        </ul>
      </div>

      <div class="col">
        <div class="photo-container">
          <img src="IMG_7003.jpg" class="slide-photo" alt="Physical Maquette">
          <div class="photo-caption">Paris zoning layout &amp; landmark diffusers</div>
        </div>
      </div>
    </div>

    <div class="footer">
      <span class="footer-brand">Urban Glow Grid</span>
      <div>UTSEUS 2026 · Page 3 of 6</div>
    </div>
  </div>

  <!-- ==========================================
       SLIDE 4: HARDWARE & TECHNICAL CHALLENGES
       ========================================== -->
  <div class="slide" id="slide4">
    <div class="penrose-bg-watermark">
      {PENROSE_SVG}
    </div>

    <div class="header">
      <h2>
        <svg class="header-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="15" x2="23" y2="15"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="15" x2="4" y2="15"/></svg>
        <span>Hardware &amp; Technical Challenges</span>
      </h2>
      <div class="slide-meta">IoT Debugging &amp; Troubleshooting</div>
    </div>

    <div class="grid-2col">
      <div class="col">
        <div class="section-title">Hardware Architecture Iterations</div>
        <div class="card">
          <h4>Active Technical Debugging</h4>
          <p>
            <b>I2C &amp; Power drops:</b> Adding the OLED screen caused noise/circuit malfunction. Actively correcting power filtering.
            <br><b>Broken Audio:</b> Speaker damaged during assembly; currently bypassed to prevent signal shorting.
          </p>
        </div>
        <div class="card">
          <h4>Planned Technical Upgrades</h4>
          <p>
            <b>Arduino Uno to Mega Transition:</b> Uno is highly pin and memory-constrained. Switched to Mega to drive larger NeoPixel arrays and I/O smoothly.
          </p>
        </div>
      </div>

      <div class="col">
        <div class="photo-container">
          <img src="IMG_7005.jpg" class="slide-photo" alt="Electrical Assembly">
          <div class="photo-caption">Breadboard setup &amp; MCP3008 multiplexer</div>
        </div>
      </div>
    </div>

    <div class="footer">
      <span class="footer-brand">Urban Glow Grid</span>
      <div>UTSEUS 2026 · Page 4 of 6</div>
    </div>
  </div>

  <!-- ==========================================
       SLIDE 5: GAMEPLAY & BUDGET
       ========================================== -->
  <div class="slide" id="slide5">
    <div class="penrose-bg-watermark">
      {PENROSE_SVG}
    </div>

    <div class="header">
      <h2>
        <svg class="header-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="6" width="20" height="12" rx="3"/><circle cx="17" cy="12" r="1.5"/><circle cx="14" cy="12" r="1.5"/><path d="M6 12h4M8 10v4"/></svg>
        <span>Gameplay &amp; Sourcing Cost</span>
      </h2>
      <div class="slide-meta">Mid-term Demo Status</div>
    </div>

    <div class="grid-2col">
      <div class="col">
        <div class="section-title">Interactive Game Mechanics</div>
        <ul class="bullet-list">
          <li>
            <b>6 Dims / Potentiometers:</b> Adjusts light intensity directly across the 6 Paris maquette zones.
          </li>
          <li>
            <b>Building Toggles:</b> Push buttons activate/deactivate power to specific priority landmarks (e.g. Hospital).
          </li>
          <li>
            <b>Reset / Start Control:</b> Button to trigger clean restarts and initialize light grids.
          </li>
        </ul>
      </div>

      <div class="col">
        <div class="section-title">Sourcing Cost Performance (CNY)</div>
        <table>
          <thead>
            <tr>
              <th>Procured Component</th>
              <th>Qty</th>
              <th>Estimated Cost</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>LED WS2812B (1M - Orange)</td>
              <td>6</td>
              <td>46.80 CNY</td>
            </tr>
            <tr>
              <td>Button (Green)</td>
              <td>10</td>
              <td>33.00 CNY</td>
            </tr>
            <tr>
              <td>IRLZ44N MOSFET</td>
              <td>7</td>
              <td>23.80 CNY</td>
            </tr>
            <tr>
              <td>Potentiometer 10K</td>
              <td>10</td>
              <td>20.81 CNY</td>
            </tr>
            <tr>
              <td>Oled screen i2c ssd1306 (Green)</td>
              <td>2</td>
              <td>19.00 CNY</td>
            </tr>
            <tr>
              <td>MCP3008 ADC IC</td>
              <td>1</td>
              <td>12.00 CNY</td>
            </tr>
            <tr>
              <td>Alimentation Block / Delivery</td>
              <td>1</td>
              <td>22.50 CNY (7.5 + 15)</td>
            </tr>
            <tr>
              <td>Glue sticks, Speaker, Resistors</td>
              <td>-</td>
              <td>15.70 CNY (6.8 + 4 + 4.9)</td>
            </tr>
            <tr>
              <td>Arduino Uno, Dupont wires, Kits</td>
              <td>-</td>
              <td>School-Provided (0 CNY)</td>
            </tr>
            <tr class="total-row">
              <td>TOTAL DIRECT SOURCED COST</td>
              <td>-</td>
              <td>193.61 CNY</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="footer">
      <span class="footer-brand">Urban Glow Grid</span>
      <div>UTSEUS 2026 · Page 5 of 6</div>
    </div>
  </div>

  <!-- ==========================================
       SLIDE 6: CONCLUSION & NEXT STEPS
       ========================================== -->
  <div class="slide" id="slide6">
    <div class="penrose-bg-watermark">
      {PENROSE_SVG}
    </div>

    <div class="header">
      <h2>
        <svg class="header-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 16.5c-1.5 1.26-2 3.24-2 3.24s1.98-.5 3.24-2"/><path d="M12 3v12"/><path d="M12 3c3.5 0 6 3 6 8a4 4 0 0 1-4 4H8a4 4 0 0 1-4-4c0-5 2.5-8 6-8z"/><path d="M9 15v4c0 1 1 2 2 2h2c1 0 2-1 2-2v-4"/></svg>
        <span>Conclusion &amp; Roadmap</span>
      </h2>
      <div class="slide-meta">Mid-term Pitch Closing</div>
    </div>

    <div class="closing-content">
      <h3 class="closing-title">Thank You.</h3>
      <p class="closing-subtitle">Open for Q&amp;A</p>
      
      <div class="closing-grid">
        <div class="closing-card">
          <h4>1. Hardware Integration</h4>
          <p>Resolve OLED power draw, replace damaged speaker, and compile finalized wiring schematic.</p>
        </div>
        <div class="closing-card">
          <h4>2. Board Upgrades</h4>
          <p>Migrate from Uno to Mega platform to drive expanded NeoPixel grids and multiple push button inputs.</p>
        </div>
        <div class="closing-card">
          <h4>3. Gameplay Tuning</h4>
          <p>Calibrate potentiometer input mappings, define grid crash thresholds, and code environmental scenarios.</p>
        </div>
      </div>
    </div>

    <div class="footer">
      <span class="footer-brand">Urban Glow Grid</span>
      <div>UTSEUS 2026 · Page 6 of 6</div>
    </div>
  </div>

</body>
</html>
"""

async def main():
    html_file = Path("/Users/Abir/Desktop/innovation project/presentation_slide.html")
    pdf_file = Path("/Users/Abir/Desktop/innovation project/Urban_GlowGrid_Presentation_Midterm.pdf")
    
    # Write the clean HTML content
    html_file.write_text(HTML_CONTENT, encoding="utf-8")
    print(f"Written updated presentation HTML to {html_file.absolute()}")

    print("Launching browser via Playwright...")
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Load the HTML file
        filepath = os.path.abspath(str(html_file))
        await page.goto(f"file://{filepath}")
        
        # Wait for page assets and fonts
        print("Waiting for page layouts to paint...")
        await page.wait_for_timeout(2500)
        
        # Emulate print media
        await page.emulate_media(media="print")
        
        # Generate the PDF in landscape A4, with no margins for full-bleed page breaks
        print("Generating PDF...")
        await page.pdf(
            path=str(pdf_file),
            format="A4",
            landscape=True,
            print_background=True,
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"}
        )
        
        await browser.close()
        print(f"✅ Presentation PDF successfully generated at:\n  - {pdf_file.absolute()}")

if __name__ == "__main__":
    asyncio.run(main())
