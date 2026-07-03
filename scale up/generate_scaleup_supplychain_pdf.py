import asyncio
from playwright.async_api import async_playwright
import os
from pathlib import Path

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Urban Glow Grid — Day 2 Scale-Up Presentation</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800;900&display=swap');

    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    @page {
      size: A4 landscape;
      margin: 0;
    }

    b, strong {
      font-weight: 800 !important;
    }

    body {
      margin: 0;
      padding: 0;
      background: #e2e8f0;
      color: #1e293b;
      font-family: 'Plus Jakarta Sans', sans-serif;
      line-height: 1.4;
      width: 297mm;
      height: 210mm;
      overflow: hidden;
    }

    .slide {
      width: 297mm;
      height: 210mm;
      padding: 16mm 20mm 12mm 20mm;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      background: #f4f8f6; /* Premium light mint background */
      background-image: 
        radial-gradient(circle at 85% 15%, rgba(16, 185, 129, 0.12) 0%, transparent 55%),
        radial-gradient(circle at 15% 85%, rgba(5, 150, 105, 0.08) 0%, transparent 55%);
      border: 1px solid rgba(16, 185, 129, 0.15);
      page-break-after: always;
      box-sizing: border-box;
      overflow: hidden;
    }

    .slide:last-child {
      page-break-after: avoid;
    }

    /* Print styling */
    @media print {
      body { background: transparent; }
      .slide { border: none; }
      .card, .photo-container, table, .badge {
        box-shadow: none !important;
      }
    }

    /* ── HEADER ── */
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid rgba(16, 185, 129, 0.15);
      padding-bottom: 6px;
      margin-bottom: 10px;
      z-index: 2;
    }

    .header h2 {
      font-family: 'Outfit', sans-serif;
      font-size: 20pt;
      font-weight: 700;
      color: #064e3b;
      display: flex;
      align-items: center;
      gap: 10px;
      letter-spacing: -0.5px;
    }

    .header-icon {
      color: #10b981;
      width: 24px;
      height: 24px;
      stroke-width: 2.2;
    }

    .header .slide-meta {
      font-size: 9pt;
      font-weight: 700;
      color: #059669;
      text-transform: uppercase;
      letter-spacing: 1px;
    }

    /* ── FOOTER ── */
    .footer {
      display: flex;
      justify-content: space-between;
      border-top: 1px solid rgba(16, 185, 129, 0.15);
      padding-top: 6px;
      margin-top: 8px;
      font-size: 8pt;
      color: #64748b;
      font-weight: 600;
      z-index: 2;
    }

    .footer-brand {
      font-family: 'Outfit', sans-serif;
      font-weight: 800;
      color: #064e3b;
      text-transform: uppercase;
      letter-spacing: 1.5px;
    }

    /* ── GRID SYSTEMS ── */
    .grid-2col {
      display: grid;
      grid-template-columns: 1.15fr 0.85fr;
      gap: 20px;
      flex: 1;
      height: 150mm;
      margin: 5px 0;
      z-index: 2;
    }

    .grid-equal-col {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      flex: 1;
      height: 150mm;
      margin: 5px 0;
      z-index: 2;
    }

    /* ── PHOTO CONTAINERS ── */
    .photos-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      height: 100%;
    }

    .photo-container {
      background: #ffffff;
      border: 1px solid rgba(16, 185, 129, 0.15);
      border-radius: 12px;
      padding: 8px;
      box-shadow: 0 4px 15px -5px rgba(6, 78, 59, 0.05);
      display: flex;
      flex-direction: column;
      height: 100%;
    }

    .photo-container img {
      width: 100%;
      height: 110mm;
      object-fit: cover;
      border-radius: 8px;
      margin-bottom: 6px;
    }

    .photo-caption {
      font-size: 8.5pt;
      font-weight: 700;
      color: #064e3b;
      text-align: center;
    }

    /* ── CARDS ── */
    .card {
      background: #ffffff;
      border: 1px solid rgba(16, 185, 129, 0.12);
      border-radius: 12px;
      padding: 12px 14px;
      box-shadow: 0 4px 15px -5px rgba(6, 78, 59, 0.04);
      margin-bottom: 10px;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }

    .card h4 {
      font-family: 'Outfit', sans-serif;
      font-size: 10.5pt;
      font-weight: 800;
      color: #064e3b;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 4px;
      border-bottom: 1px solid rgba(16, 185, 129, 0.08);
      padding-bottom: 2px;
    }

    .card p {
      font-size: 8.5pt;
      color: #334155;
      line-height: 1.4;
    }

    .card b {
      color: #059669;
    }

    .section-title {
      font-family: 'Outfit', sans-serif;
      font-size: 11.5pt;
      font-weight: 800;
      color: #064e3b;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 8px;
      border-left: 3.5px solid #10b981;
      padding-left: 8px;
    }

    /* ── BOM TABLE STYLES ── */
    .bom-table-container {
      background: #ffffff;
      border: 1px solid rgba(16, 185, 129, 0.15);
      border-radius: 12px;
      padding: 8px 12px;
      box-shadow: 0 4px 20px -5px rgba(6, 78, 59, 0.04);
      overflow: hidden;
      height: 142mm;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 7pt;
    }

    th {
      border-bottom: 2px solid #064e3b;
      color: #064e3b;
      font-weight: 800;
      padding: 4px 5px;
      text-align: left;
      font-family: 'Outfit', sans-serif;
      text-transform: uppercase;
      font-size: 6.8pt;
      letter-spacing: 0.3px;
    }

    td {
      border-bottom: 1px solid rgba(16, 185, 129, 0.08);
      padding: 3.5px 5px;
      color: #334155;
      vertical-align: middle;
      line-height: 1.15;
    }

    tr:last-child td {
      border-bottom: none;
    }

    .total-row {
      font-weight: 800;
      background: #e6f4ea;
      border-top: 2px solid #064e3b;
      color: #064e3b;
    }

    /* Kraljic Badges */
    .badge {
      display: inline-block;
      padding: 1px 4px;
      border-radius: 4px;
      font-size: 6pt;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.2px;
    }

    .badge-strategic { background: #fee2e2; border: 1px solid #fca5a5; color: #b91c1c; }
    .badge-bottleneck { background: #fef3c7; border: 1px solid #fcd34d; color: #b45309; }
    .badge-leverage { background: #d1fae5; border: 1px solid #6ee7b7; color: #047857; }
    .badge-noncritical { background: #f1f5f9; border: 1px solid #cbd5e1; color: #475569; }

    .justifications {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .justification-title {
      font-family: 'Outfit', sans-serif;
      font-size: 10pt;
      font-weight: 800;
      color: #064e3b;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      border-bottom: 2px solid rgba(16, 185, 129, 0.15);
      padding-bottom: 3px;
      margin-bottom: 2px;
    }

    .item-card {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }

    .item-header {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
    }

    .item-name {
      font-size: 8.5pt;
      font-weight: 800;
      color: #064e3b;
    }

    .item-desc {
      font-size: 7.8pt;
      color: #475569;
      text-align: justify;
      line-height: 1.3;
    }

    /* ── FINANCIAL GRID STYLES ── */
    .financial-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin-top: 4px;
    }

    .financial-stat {
      background: #fafdfc;
      border: 1px solid rgba(16, 185, 129, 0.15);
      border-radius: 8px;
      padding: 6px 8px;
      text-align: center;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }

    .financial-stat span {
      display: block;
      font-size: 7pt;
      color: #475569;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.3px;
      margin-bottom: 2px;
    }

    .financial-stat strong {
      font-family: 'Outfit', sans-serif;
      font-size: 11pt;
      color: #064e3b;
      font-weight: 900;
    }

    .financial-stat.highlight {
      background: #e6f4ea;
      border: 1px solid #10b981;
    }

    .financial-stat.highlight strong {
      color: #047857;
      font-size: 12pt;
    }
  </style>
</head>
<body>

  <!-- ==========================================
       SLIDE 1: INTRO COVER
       ========================================== -->
  <div class="slide" id="slide1" style="justify-content: center; align-items: center; text-align: center; background-image: radial-gradient(circle at 50% 50%, rgba(16, 185, 129, 0.15) 0%, transparent 60%);">
    <div style="z-index: 2; display: flex; flex-direction: column; align-items: center; gap: 10px;">
      <span style="font-family: 'Outfit', sans-serif; font-size: 14pt; font-weight: 800; color: #10b981; text-transform: uppercase; letter-spacing: 4px; margin-bottom: 5px;">UTSEUS 2026</span>
      <h1 style="font-family: 'Outfit', sans-serif; font-size: 44pt; font-weight: 900; color: #064e3b; letter-spacing: -1.5px; line-height: 1.1; margin-bottom: 5px;">Urban Glow Grid</h1>
      <p style="font-size: 16pt; font-weight: 500; color: #059669; margin-bottom: 25px; font-family: 'Plus Jakarta Sans', sans-serif;">IoT Smart Grid Simulator — Scale-Up &amp; Sourcing Strategy</p>
      
      <div style="border-top: 2px solid rgba(16, 185, 129, 0.2); padding-top: 15px; width: 140mm; display: flex; justify-content: space-between; font-size: 9.5pt; color: #64748b; font-weight: 600;">
        <div>Presenter Group: <strong>Team 22</strong></div>
        <div>Members: <strong>Abir, Ismail, Sofiane, Mohamed, Nouh</strong></div>
      </div>
    </div>
  </div>

  <!-- ==========================================
       SLIDE 2: THE PRODUCT CONCEPT
       ========================================== -->
  <div class="slide" id="slide2">
    <div class="header">
      <h2>
        <svg class="header-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
        <span>Product Overview &amp; Industrial Vision</span>
      </h2>
      <div class="slide-meta">Concept &amp; Target Scale</div>
    </div>

    <div class="grid-2col" style="grid-template-columns: 1fr 1fr; gap: 25px;">
      <div class="photo-container" style="padding: 6px; height: 100%;">
        <img src="file:///Users/Abir/Desktop/innovation project/Gemini_Generated_Image_s66owns66owns66o.png" alt="Finished Product Concept" style="height: 122mm; border-radius: 8px; object-fit: cover;">
        <div class="photo-caption" style="margin-top: 4px;">Target Industrial Design Concept (30,000 Units)</div>
      </div>

      <div class="col" style="display: flex; flex-direction: column; justify-content: center; gap: 10px;">
        <div class="card" style="margin-bottom: 0; padding: 16px;">
          <h4 style="font-size: 11.5pt;">What is Urban Glow Grid?</h4>
          <p style="font-size: 9.2pt; line-height: 1.5; color: #334155; margin-top: 5px;">
            An <b>IoT-enabled sustainable smart grid simulator</b> designed as an interactive educational console for science museums and schools. It simulates electrical grid management in real-time, helping users understand renewable energy distribution and grid stability challenges.
          </p>
        </div>

        <div class="card" style="margin-bottom: 0; padding: 16px;">
          <h4 style="font-size: 11.5pt;">Problem &amp; SDG Alignment</h4>
          <p style="font-size: 9.2pt; line-height: 1.5; color: #334155; margin-top: 5px;">
            Educating the public on complex grid mechanisms (solar/wind variability, load balancing) is crucial for the green transition. The product directly addresses **UN SDGs 7 (Affordable and Clean Energy)** and **11 (Sustainable Cities &amp; Communities)**.
          </p>
        </div>
        
        <div class="card" style="margin-bottom: 0; padding: 12px 16px; background: #e6f4ea; border: 1px solid #10b981;">
          <p style="font-size: 9.5pt; font-weight: 700; color: #064e3b; text-align: center;">
            ✦ Target Scale-Up Production: <strong>30,000 Units</strong>
          </p>
        </div>
      </div>
    </div>

    <div class="footer">
      <span class="footer-brand">Urban Glow Grid</span>
      <div>Day 2 Scale-Up · Slide 2 of 7</div>
    </div>
  </div>

  <!-- ==========================================
       SLIDE 3: CURRENT PHYSICAL MVP PROTOTYPE
       ========================================== -->
  <div class="slide" id="slide3">
    <div class="header">
      <h2>
        <svg class="header-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>
        <span>Physical MVP Prototype Architecture</span>
      </h2>
      <div class="slide-meta">Real Prototype &amp; Internal Wiring</div>
    </div>

    <div class="grid-2col" style="grid-template-columns: 1.35fr 0.65fr; gap: 20px;">
      <div class="photos-row">
        <div class="photo-container">
          <img src="file:///Users/Abir/Desktop/innovation project/IMG_7003.jpg" alt="MVP Top View" style="height: 124mm; object-fit: contain; background: #fafdfc; border: 1px solid rgba(16, 185, 129, 0.1);">
          <div class="photo-caption">Top Interface: Wood Grid &amp; Dials</div>
        </div>
        <div class="photo-container">
          <img src="file:///Users/Abir/Desktop/innovation project/IMG_7005.jpg" alt="MVP Bottom View" style="height: 124mm; object-fit: contain; background: #fafdfc; border: 1px solid rgba(16, 185, 129, 0.1);">
          <div class="photo-caption">Bottom Circuitry: Microcontroller &amp; Wiring</div>
        </div>
      </div>

      <div class="col" style="display: flex; flex-direction: column; justify-content: center; gap: 6px;">
        <div class="card" style="padding: 10px 12px; margin-bottom: 0;">
          <h4>1. Wooden Top Contour Chassis</h4>
          <p>Laser-cut from <b>7 Birch plywood panels</b>, structured by <b>8 pillars</b>. Holds <b>21 translucent building diffusers</b>.</p>
        </div>

        <div class="card" style="padding: 10px 12px; margin-bottom: 0;">
          <h4>2. Control &amp; Display Console</h4>
          <p><b>6 rotary potentiometers</b> and <b>3 arcade action buttons</b> input signals. <b>0.96-inch OLED screen</b> and <b>3 classic LEDs</b> show network status.</p>
        </div>

        <div class="card" style="padding: 10px 12px; margin-bottom: 0;">
          <h4>3. Embedded Controller &amp; Multiplexer</h4>
          <p>Driven by an <b>Arduino Uno</b> and <b>6 addressable WS2812B LED stripes</b>. Uses an <b>MCP3008 ADC chip</b> on a <b>170-tie breadboard</b> to read all knobs over SPI.</p>
        </div>

        <div class="card" style="padding: 10px 12px; margin-bottom: 0;">
          <h4>4. Power &amp; Sound Alerts</h4>
          <p>Clean power via <b>5V 4A adapter</b> and physical <b>Rocker Power Switch</b>. <b>Dual 8-ohm speakers</b> trigger overload audio alarms.</p>
        </div>
      </div>
    </div>

    <div class="footer">
      <span class="footer-brand">Urban Glow Grid</span>
      <div>Day 2 Scale-Up · Slide 3 of 7</div>
    </div>
  </div>

  <!-- ==========================================
       SLIDE 4: DETAILED BILL OF MATERIALS (BOM)
       ========================================== -->
  <div class="slide" id="slide4">
    <div class="header">
      <h2>
        <svg class="header-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>
        <span>Prototype BOM vs. Scale-Up Wholesale Estimates</span>
      </h2>
      <div class="slide-meta">Prototype Retail vs. Bulk Volume Estimations</div>
    </div>

    <div class="grid-2col" style="grid-template-columns: 1.15fr 0.85fr; gap: 20px;">
      <div class="bom-table-container" style="height: 142mm;">
        <table>
          <thead>
            <tr>
              <th style="width: 34%;">Component / Material</th>
              <th style="width: 6%; text-align: center;">Qty</th>
              <th style="width: 15%; text-align: right;">Proto Unit (CNY)</th>
              <th style="width: 15%; text-align: right;">Proto Total (CNY)</th>
              <th style="width: 15%; text-align: right;">Bulk Unit (CNY)</th>
              <th style="width: 15%; text-align: right;">Bulk Total (CNY)</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>3D Printed Buildings (diffusers)</td>
              <td style="text-align: center;">21</td>
              <td style="text-align: right;">2.00</td>
              <td style="text-align: right;">42.00</td>
              <td style="text-align: right;">0.20</td>
              <td style="text-align: right;">4.20</td>
            </tr>
            <tr>
              <td>Laser-Cut Base Wood Panels</td>
              <td style="text-align: center;">7</td>
              <td style="text-align: right;">3.00</td>
              <td style="text-align: right;">21.00</td>
              <td style="text-align: right;">0.80</td>
              <td style="text-align: right;">5.60</td>
            </tr>
            <tr>
              <td>3D Printed Landscape Details</td>
              <td style="text-align: center;">20</td>
              <td style="text-align: right;">0.50</td>
              <td style="text-align: right;">10.00</td>
              <td style="text-align: right;">0.05</td>
              <td style="text-align: right;">1.00</td>
            </tr>
            <tr>
              <td>Addressable WS2812B LED Stripes</td>
              <td style="text-align: center;">6</td>
              <td style="text-align: right;">2.00</td>
              <td style="text-align: right;">12.00</td>
              <td style="text-align: right;">0.60</td>
              <td style="text-align: right;">3.60</td>
            </tr>
            <tr>
              <td>Arduino Uno Board (Microcontroller)</td>
              <td style="text-align: center;">1</td>
              <td style="text-align: right;">15.00</td>
              <td style="text-align: right;">15.00</td>
              <td style="text-align: right;">2.00</td>
              <td style="text-align: right;">2.00</td>
            </tr>
            <tr>
              <td>Push Buttons (Arcade Action)</td>
              <td style="text-align: center;">3</td>
              <td style="text-align: right;">1.00</td>
              <td style="text-align: right;">3.00</td>
              <td style="text-align: right;">0.30</td>
              <td style="text-align: right;">0.90</td>
            </tr>
            <tr>
              <td>Wood Pillars (Support Dowels)</td>
              <td style="text-align: center;">8</td>
              <td style="text-align: right;">0.50</td>
              <td style="text-align: right;">4.00</td>
              <td style="text-align: right;">0.10</td>
              <td style="text-align: right;">0.80</td>
            </tr>
            <tr>
              <td>Power Switch (On/Off Rocker)</td>
              <td style="text-align: center;">1</td>
              <td style="text-align: right;">1.00</td>
              <td style="text-align: right;">1.00</td>
              <td style="text-align: right;">0.20</td>
              <td style="text-align: right;">0.20</td>
            </tr>
            <tr>
              <td>Power Supply Adapter (5V 4A)</td>
              <td style="text-align: center;">1</td>
              <td style="text-align: right;">12.00</td>
              <td style="text-align: right;">12.00</td>
              <td style="text-align: right;">4.00</td>
              <td style="text-align: right;">4.00</td>
            </tr>
            <tr>
              <td>Potentiometers (B10K Rotary Dials)</td>
              <td style="text-align: center;">6</td>
              <td style="text-align: right;">0.50</td>
              <td style="text-align: right;">3.00</td>
              <td style="text-align: right;">0.20</td>
              <td style="text-align: right;">1.20</td>
            </tr>
            <tr>
              <td>Connecting Wires (Jumper Cables)</td>
              <td style="text-align: center;">54</td>
              <td style="text-align: right;">0.05</td>
              <td style="text-align: right;">2.70</td>
              <td style="text-align: right;">0.01</td>
              <td style="text-align: right;">0.54</td>
            </tr>
            <tr>
              <td>Breadboard (Prototype Matrix)</td>
              <td style="text-align: center;">1</td>
              <td style="text-align: right;">5.00</td>
              <td style="text-align: right;">5.00</td>
              <td style="text-align: right;">0.00</td>
              <td style="text-align: right;">0.00</td>
            </tr>
            <tr>
              <td>Analog Multiplexer (MCP3008 ADC)</td>
              <td style="text-align: center;">1</td>
              <td style="text-align: right;">4.00</td>
              <td style="text-align: right;">4.00</td>
              <td style="text-align: right;">1.00</td>
              <td style="text-align: right;">1.00</td>
            </tr>
            <tr>
              <td>Scotch Adhesive Mounting Tape</td>
              <td style="text-align: center;">21</td>
              <td style="text-align: right;">0.10</td>
              <td style="text-align: right;">2.10</td>
              <td style="text-align: right;">0.02</td>
              <td style="text-align: right;">0.42</td>
            </tr>
            <tr>
              <td>OLED Display (128x64 I2C Screen)</td>
              <td style="text-align: center;">1</td>
              <td style="text-align: right;">6.00</td>
              <td style="text-align: right;">6.00</td>
              <td style="text-align: right;">2.50</td>
              <td style="text-align: right;">2.50</td>
            </tr>
            <tr>
              <td>Sticks of Glue (Hot Melt Adhesive)</td>
              <td style="text-align: center;">3</td>
              <td style="text-align: right;">1.00</td>
              <td style="text-align: right;">3.00</td>
              <td style="text-align: right;">0.20</td>
              <td style="text-align: right;">0.60</td>
            </tr>
            <tr>
              <td>Resistors (10k Ohm Signal Damping)</td>
              <td style="text-align: center;">2</td>
              <td style="text-align: right;">0.10</td>
              <td style="text-align: right;">0.20</td>
              <td style="text-align: right;">0.02</td>
              <td style="text-align: right;">0.04</td>
            </tr>
            <tr>
              <td>Speakers (8-Ohm Audio Alerts)</td>
              <td style="text-align: center;">2</td>
              <td style="text-align: right;">1.50</td>
              <td style="text-align: right;">3.00</td>
              <td style="text-align: right;">0.50</td>
              <td style="text-align: right;">1.00</td>
            </tr>
            <tr>
              <td>Classic LEDs (Status Indicators)</td>
              <td style="text-align: center;">3</td>
              <td style="text-align: right;">0.33</td>
              <td style="text-align: right;">1.00</td>
              <td style="text-align: right;">0.10</td>
              <td style="text-align: right;">0.30</td>
            </tr>
            <tr class="total-row">
              <td colspan="3">TOTAL RAW HARDWARE BOM COST</td>
              <td style="text-align: right;">150.00 CNY</td>
              <td colspan="1"></td>
              <td style="text-align: right;">30.00 CNY</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="justifications" style="display: flex; flex-direction: column; justify-content: center;">
        <div class="justification-title">Wholesale Estimation Rationale</div>
        <p style="font-size: 8.2pt; line-height: 1.4; color: #475569; margin-bottom: 10px; text-align: justify;">
          * <b>Estimation Note:</b> Wholesale unit rates are estimated approximations based on quotes from upstream manufacturers for a <b>30,000-unit contract</b>.
        </p>

        <div class="card" style="margin-bottom: 0; padding: 10px 12px; gap: 2px;">
          <h4>Integrated Custom PCBA</h4>
          <p style="font-size: 8pt; line-height: 1.3;">
            Bulk hardware eliminates the breadboard and jumper cables. An integrated PCB layout directly mounts the microcontroller chip (2.00 CNY) and multiplexer chip, reducing raw hardware cost.
          </p>
        </div>

        <div class="card" style="margin-bottom: 0; padding: 10px 12px; gap: 2px;">
          <h4>Plastic Injection Molding</h4>
          <p style="font-size: 8pt; line-height: 1.3;">
            Slow, expensive 3D printing is replaced by rapid B2B plastic injection molding, slashing individual building diffuser cost from 2.00 CNY to just 0.20 CNY.
          </p>
        </div>
      </div>
    </div>

    <div class="footer">
      <span class="footer-brand">Urban Glow Grid</span>
      <div>Day 2 Scale-Up · Slide 4 of 7</div>
    </div>
  </div>

  <!-- ==========================================
       SLIDE 5: MANUFACTURING & ASSEMBLY PROCESS
       ========================================== -->
  <div class="slide" id="slide5">
    <div class="header">
      <h2>
        <svg class="header-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>
        <span>Manufacturing &amp; Assembly Process Strategy</span>
      </h2>
      <div class="slide-meta">Industrial Scale-Up Timeline</div>
    </div>

    <div class="grid-equal-col">
      <div class="col" style="justify-content: center;">
        <div class="section-title">Phase 1: In-House Manual Pilot (Months 1-4)</div>
        
        <div class="card" style="padding: 12px 14px; margin-bottom: 10px;">
          <h4>Manual Assembly &amp; Calibration Jigs</h4>
          <p>
            • Assemble initial batches manually with a small team of <b>4 to 5 workers</b> to strictly monitor quality.
            <br>• Focus on manual sensor calibration, firmware flashing, and hardware debugging.
          </p>
        </div>

        <div class="card" style="padding: 12px 14px; margin-bottom: 0;">
          <h4>Design for Manufacturing (DFM) Prep</h4>
          <p>
            • Redesign the prototype circuit into a single custom <b>PCBA board</b>, eliminating breadboards and jumper wires.
            <br>• Sourcing pre-certified sub-modules (power adapters) to accelerate certifications.
          </p>
        </div>
      </div>

      <div class="col" style="justify-content: center;">
        <div class="section-title">Phase 2: Automated Supplier Delegation (Months 5+)</div>
        
        <div class="card" style="padding: 12px 14px; margin-bottom: 10px;">
          <h4>Contract Manufacturing (EMS)</h4>
          <p>
            • Delegate raw fabrication and PCBA assembly to specialized YRD factory contract suppliers.
            <br>• Automate production lines using custom jigs designed and tested during our Phase 1 manual pilot.
          </p>
        </div>

        <div class="card" style="padding: 12px 14px; margin-bottom: 0;">
          <h4>Core Startup Team Pivot</h4>
          <p>
            • Fully transition the core startup team away from manual assembly line labor.
            <br>• Focus 100% of internal startup resources on <b>global B2B sales expansion, marketing, and software updates</b>.
          </p>
        </div>
      </div>
    </div>

    <div class="footer">
      <span class="footer-brand">Urban Glow Grid</span>
      <div>Day 2 Scale-Up · Slide 5 of 7</div>
    </div>
  </div>

  <!-- ==========================================
       SLIDE 6: CUSTOMERS STRATEGY & FINANCIAL BUSINESS MODEL
       ========================================== -->
  <div class="slide" id="slide6">
    <div class="header">
      <h2>
        <svg class="header-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        <span>Customers Strategy &amp; Financial Business Model</span>
      </h2>
      <div class="slide-meta">Market Expansion &amp; Projections</div>
    </div>

    <div class="grid-equal-col">
      <div class="col" style="justify-content: center;">
        <div class="section-title">Logistics, Channels &amp; Compliance</div>
        
        <div class="card" style="padding: 10px 12px; margin-bottom: 8px;">
          <h4>Central Sourcing &amp; Sales Channels</h4>
          <p>
            • Ningbo warehouse is central to YRD suppliers; ships by sea/air.
            <br>• Scale school sales via STEM distributors; sell directly to museums.
          </p>
        </div>

        <div class="card" style="padding: 10px 12px; margin-bottom: 8px;">
          <h4>CE, FCC, &amp; RoHS Compliance Roadmap</h4>
          <p>
            • Pre-compliance: PCBA design utilizes pre-certified RF modules.
            <br>• Lab testing: Budget 10k EUR in Phase 1 for CEM testing.
          </p>
        </div>

        <div class="card" style="padding: 10px 12px; margin-bottom: 0;">
          <h4>Flat-Pack &amp; Assembly Strategy</h4>
          <p>
            • Schools: Flat-pack kits (freight cuts to 10 CNY) for maker classes.
            <br>• Museums: Delivered 100% pre-assembled for instant display.
            <br>• B2C Expansion: Launch flat-pack retail kits for hobbyists in Year 2.
          </p>
        </div>
      </div>

      <div class="col" style="justify-content: center;">
        <div class="section-title">Scale-Up Financial Model (30k Units Target)</div>
        
        <div class="card" style="padding: 10px 12px; margin-bottom: 8px;">
          <h4>Unit Economics &amp; Cost Price</h4>
          <p style="font-size: 7.5pt; line-height: 1.25; margin-bottom: 6px; color:#475569;">
            <b>All-Inclusive Cost Breakdown:</b> Raw BOM: <b>30 CNY</b> | Assembly: <b>15 CNY</b> | QC/Packaging: <b>10 CNY</b> | Shipping/Customs: <b>25 CNY</b> | 3PL Warehousing/Delivery: <b>40 CNY</b> | Warranty Swap: <b>10 CNY</b>.
          </p>
          <div class="financial-grid">
            <div class="financial-stat">
              <span>Unit Cost Price</span>
              <strong>120.00 CNY <small style="font-size:6.5pt;color:#64748b;">(≈$17.00)</small></strong>
            </div>
            <div class="financial-stat">
              <span>Selling Price (B2B/B2G)</span>
              <strong>299.00 CNY <small style="font-size:6.5pt;color:#64748b;">(≈$42.00)</small></strong>
            </div>
            <div class="financial-stat highlight" style="grid-column: span 2;">
              <span>Unit Gross Profit</span>
              <strong>179.00 CNY <small style="font-size:8pt;color:#047857;">(60.0% Gross Margin)</small></strong>
            </div>
          </div>
        </div>

        <div class="card" style="padding: 10px 12px; margin-bottom: 0;">
          <h4>Monthly &amp; Annual Projections (3,000 Sales/Mo)</h4>
          <div class="financial-grid">
            <div class="financial-stat">
              <span>Monthly Revenue</span>
              <strong>897,000 CNY <small style="font-size:6.5pt;color:#64748b;">(≈$126,000)</small></strong>
            </div>
            <div class="financial-stat highlight">
              <span>Monthly Gross Profit</span>
              <strong>537,000 CNY <small style="font-size:6.5pt;color:#047857;">(≈$75,600)</small></strong>
            </div>
            <div class="financial-stat" style="grid-column: span 2;">
              <span>Annual Revenue Projection (Run Rate)</span>
              <strong>10,764,000 CNY <small style="font-size:7.5pt;color:#64748b;">(≈$1.51M USD / Year)</small></strong>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="footer">
      <span class="footer-brand">Urban Glow Grid</span>
      <div>Day 2 Scale-Up · Slide 6 of 7</div>
    </div>
  </div>

  <!-- ==========================================
       SLIDE 7: CLOSING & Q&A
       ========================================== -->
  <div class="slide" id="slide7" style="justify-content: center; align-items: center; text-align: center; background-image: radial-gradient(circle at 50% 50%, rgba(16, 185, 129, 0.15) 0%, transparent 60%); border-bottom: none;">
    <div style="z-index: 2; display: flex; flex-direction: column; align-items: center; gap: 10px;">
      <span style="font-family: 'Outfit', sans-serif; font-size: 14pt; font-weight: 800; color: #10b981; text-transform: uppercase; letter-spacing: 4px; margin-bottom: 5px;">Urban Glow Grid</span>
      <h1 style="font-family: 'Outfit', sans-serif; font-size: 38pt; font-weight: 900; color: #064e3b; letter-spacing: -1.5px; line-height: 1.1; margin-bottom: 20px;">Thank You!</h1>
      <p style="font-size: 14pt; font-weight: 500; color: #059669; margin-bottom: 30px; font-family: 'Plus Jakarta Sans', sans-serif;">Questions &amp; Answers Session</p>
      
      <div style="border-top: 1px solid rgba(16, 185, 129, 0.2); padding-top: 15px; width: 100mm; display: flex; flex-direction: column; gap: 5px; font-size: 9pt; color: #64748b; font-weight: 600;">
        <div>Team 22 · Scale-Up &amp; Sourcing Pitch</div>
      </div>
    </div>
  </div>

</body>
</html>
"""

async def main():
    scale_up_dir = Path("/Users/Abir/Desktop/innovation project/scale up")
    scale_up_dir.mkdir(parents=True, exist_ok=True)
    
    html_file = scale_up_dir / "scaleup_slide.html"
    pdf_file = scale_up_dir / "team22_urbanglowgrid_scaleup_supplychain.pdf"
    
    # Write the HTML slide deck
    html_file.write_text(HTML_CONTENT, encoding="utf-8")
    print(f"Written scale-up slides HTML to {html_file.absolute()}")

    print("Launching browser via Playwright...")
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Load the HTML file
        filepath = os.path.abspath(str(html_file))
        await page.goto(f"file://{filepath}", wait_until="domcontentloaded")
        
        # Wait for page painting & fonts loading
        print("Waiting for page layouts to paint...")
        await page.wait_for_timeout(2000)
        
        # Emulate print media
        await page.emulate_media(media="print")
        
        # Generate the landscape PDF
        print("Generating PDF...")
        await page.pdf(
            path=str(pdf_file),
            format="A4",
            landscape=True,
            print_background=True,
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"}
        )
        
        await browser.close()
        print(f"✅ Slide Deck PDF successfully generated at:\n  - {pdf_file.absolute()}")

if __name__ == "__main__":
    asyncio.run(main())
