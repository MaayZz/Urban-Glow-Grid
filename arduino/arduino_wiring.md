# 🔌 Wiring Guide & Pin Configuration — Arduino Mega 2560

This document describes the exact electrical connections used for the **Urban Glow Grid** physical mockup. The connections listed below are defined in the production C++ code (`arduino/urban_glow_grid_mega_final/urban_glow_grid_mega_final.ino`).

---

## 🎛 Complete Pin Mapping Table

| Component | Pin Type | Pin Number | Pin Mode | Description |
| :--- | :--- | :--- | :--- | :--- |
| **I2C OLED Screen** | I2C (SDA) | **Pin 20** | Output / Input | Data line for the SSD1306 OLED visualizer |
| **I2C OLED Screen** | I2C (SCL) | **Pin 21** | Output | Clock line for the SSD1306 OLED visualizer |
| **Potentiometer 1** | Analog Input | **A0** | INPUT | Zone 1 (Haussmann) Load balancing dial |
| **Potentiometer 2** | Analog Input | **A1** | INPUT | Zone 2 (Défense) Load balancing dial |
| **Potentiometer 3** | Analog Input | **A2** | INPUT | Zone 3 (Monuments) Load balancing dial |
| **Potentiometer 4** | Analog Input | **A3** | INPUT | Zone 4 Load balancing dial |
| **Potentiometer 5** | Analog Input | **A4** | INPUT | Zone 5 Load balancing dial |
| **Potentiometer 6** | Analog Input | **A5** | INPUT | Zone 6 Load balancing dial |
| **NeoPixel Strip 1** | Digital Output | **Pin 2** | OUTPUT | 10x WS2812B LEDs under Zone 1 |
| **NeoPixel Strip 2** | Digital Output | **Pin 3** | OUTPUT | 10x WS2812B LEDs under Zone 2 |
| **NeoPixel Strip 3** | Digital Output | **Pin 4** | OUTPUT | 10x WS2812B LEDs under Zone 3 |
| **NeoPixel Strip 4** | Digital Output | **Pin 5** | OUTPUT | 10x WS2812B LEDs under Zone 4 |
| **NeoPixel Strip 5** | Digital Output | **Pin 6** | OUTPUT | 10x WS2812B LEDs under Zone 5 |
| **NeoPixel Strip 6** | Digital Output | **Pin 7** | OUTPUT | 10x WS2812B LEDs under Zone 6 |
| **Secondary strip 1** | Digital Output | **Pin 8** | OUTPUT | 5x WS2812B LEDs for Monument override 1 |
| **Secondary strip 2** | Digital Output | **Pin 9** | OUTPUT | 5x WS2812B LEDs for Monument override 2 |
| **Speaker / Buzzer 1** | Digital (PWM) | **Pin 22** | OUTPUT | Primary audio output (Game start/alarm tones) |
| **Speaker / Buzzer 2** | Digital (PWM) | **Pin 24** | OUTPUT | Secondary audio output (Monument override clicks) |
| **Start Button** | Digital Input | **Pin 26** | INPUT_PULLUP | Tactile switch to initialize the 3-minute game |
| **Reset Button** | Digital Input | **Pin 28** | INPUT_PULLUP | Tactile switch to interrupt/reset the game status |
| **Monument Button 1**| Digital Input | **Pin 30** | INPUT_PULLUP | Toggles priority power distribution (Monument 1) |
| **Monument Button 2**| Digital Input | **Pin 32** | INPUT_PULLUP | Toggles priority power distribution (Monument 2) |
| **Random Seed Pin** | Analog Input | **A15** | INPUT (Floating) | Left floating to initialize `randomSeed()` |

---

## 💡 Wiring Details & Electronic Principles

### 1. Dials (Potentiometers)
* Each of the 6 dials is connected to **5V** on one side, **GND** on the other side, and the middle pin (wiper) connects to the respective Analog input pins (`A0` to `A5`).
* These convert the player's physical movements into raw values from `0` to `1023` in the code, which are mapped to percentage values representing local power flow.

### 2. Status LEDs (WS2812B NeoPixels)
* The NeoPixel data lines (`DIN`) connect to Digital Pins `2` to `9`.
* **Important**: To protect the NeoPixel data pins, place a **330-ohm resistor** in series between the Arduino output pin and the NeoPixel `DIN` pin.
* Power is managed externally or via high-capacity pins. NeoPixels draw up to 60mA each at full white brightness. For 70 LEDs total, the maximum draw is ~4.2A. Power is drawn from the external 5V grid to prevent overloading the Arduino's on-board linear regulator.

### 3. Push Buttons (Tac Switches)
* The buttons are configured using the internal pull-up resistors of the Mega (`INPUT_PULLUP`). 
* This means they are **active-low**: one terminal of the switch is connected to the Arduino input pin, and the other terminal is connected directly to **GND**.
* When pressed, the input reads `LOW`. When released, it reads `HIGH`. Debouncing is handled in the software (debounce delay: 250ms).

### 4. OLED Display (I2C)
* The SSD1306 screen connects to the I2C bus of the Mega (Pins `20` and `21`). 
* If using long cables, add **4.7k-ohm pull-up resistors** from `SDA` to `5V` and `SCL` to `5V` to stabilize signal integrity and prevent screen freezes (common I2C bus failure).

### 5. Speakers / Buzzers
* Connect Pin `22` and Pin `24` in series with a **100-ohm resistor** to the speaker positive terminal (to limit current output from the Arduino pin to standard safety levels of ~20-40mA), and the other terminal to **GND**.
* Software uses `tone(speakerX, frequency, duration)` to generate alarms and cues.
