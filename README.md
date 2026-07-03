# 🗼 Urban Glow Grid — Project Documentation

Welcome to the official repository of **Urban Glow Grid** (Team 22). This project was created to fight **"Energy Blindness"** — the invisible nature of our daily energy consumption. 

Urban Glow Grid is a **physical, interactive 1:15,000 scale model of Paris** that gamifies electrical grid management. Players act as Chief Engineers, physically manipulating dials and switches to balance grid loads, prevent blackouts, and learn key sustainable energy principles in real-time.

---

## 📸 Mockup & Hardware Overview

Below is the visual structure of the physical prototype and the challenges encountered during fabrication:

* **Paris Scale Model (Overview)**: Physical wood model split into 6 key energy zones with 3D-printed translucent landmarks (Eiffel Tower, Louvre, Arc de Triomphe) diffusing NeoPixel LED light.
  ![Paris Scale Model Overview](image/IMG_OVERVIEW.jpg)
* **Wiring Under the Hood (Challenges)**: A look at the electronics layer managing nearly 90 jumper wires, showing the physical complexity and loose connections we resolved by separating structural components from the circuitry.
  ![Wiring Infrastructure Challenges](image/IMG_CHALLENGE.jpg)

---

## 📂 Repository Directory Structure

To help future developers take over and scale this project, here is how the files are organized:

* `arduino/`
  * `urban_glow_grid_mega_final/`: The production code uploaded to the Arduino Mega managing inputs/outputs.
  * `mega_hardware_test/`: Simple test scripts to isolate issues with OLED, LEDs, dials, or buttons.
  * `arduino_wiring.md`: Detailed pinout mapping and electronic connection guide.
  * `wiring_guide.pdf`: Blueprints showing the circuit layout.
* `image/`: Clean folder containing project photos.

---

## 🛠 Hardware Architecture & Bill of Materials (BOM)

The physical maquette separates the **wooden layout structure** from the **electronics layer** to allow easy, non-destructive wiring iterations. 

### Sourcing & Cost Breakdown

| Component | Qty | Function |
| :--- | :---: | :--- |
| **Écran OLED de 1.3 pouce** | 1 | Affiche les informations de charge du réseau en temps réel |
| **Rubans LED de 17cm** | 6 | Indicateurs lumineux de charge pour les 6 zones principales |
| **Rubans LED de 10cm** | 2 | Indicateurs lumineux pour les monuments / overrides |
| **Speakers** | 2 | Alertes sonores (alarme de surcharge et bruits de clic/battement de cœur) |
| **Potentiomètres** | 6 | Contrôle manuel de la charge pour chaque zone |
| **Boutons** | 4 | Interactions de jeu (Démarrage, Réinitialisation, Overrides Monuments) |

---

## 💻 Software Setup & Installation

### Arduino Code Deployment
Open the production code (`arduino/urban_glow_grid_mega_final/urban_glow_grid_mega_final.ino`) in the Arduino IDE. 

Make sure you have installed the following libraries via the Arduino Library Manager:
* **Adafruit_NeoPixel** (to control the WS2812B LEDs)
* **SSD1306Ascii** (lightweight text-only library to control the OLED screen without overloading SRAM)

Compile and upload the project onto your Arduino Mega.

---

## 🕹 Game Rules & Playbook

The game simulates a peak winter day. The player has **3 minutes** to maintain the stability of the Paris electrical grid.

1. **Balance the Grid**: Dials (potentiometers) represent zone power. When a zone turns **red** (overloaded), you must rotate the dial to decrease non-essential load.
2. **Prioritize Buildings**: Tactile buttons allow you to route power away from residential blocks to vital sectors (like hospitals or water systems) during heavy strain.
3. **Avoid Blackout**: The OLED screen shows total system capacity. If the total load exceeds 95%, the buzzer sounds a warning. If it hits 100% for more than 5 consecutive seconds, a **Blackout** is triggered: all LEDs flash red, the game resets, and you lose.
4. **Victory Condition**: Maintain system stability until the timer expires.

---

## 🚀 Future Roadmap & Developer Notes

If you are resuming this project, here are the critical steps required to turn this prototype into a commercial product:

* **Transition to Custom PCB**: The biggest hardware challenge was **Loose Connections** (wires coming loose from the breadboards due to physical vibration). Designing a dedicated Printed Circuit Board (PCB) to replace jumper wires will reduce assembly time by 95% and make the product robust enough for shipping.
* **Scale Software Architecture**: The current C++ simulation is optimized for Paris (6 zones). The code is structured modularly so you can swap out the geographic layout files and LED indices to model other cities.
* **Transition to B2B Educational Kits**: Next phases should package the PCB, components, and a flat-packed wooden box as a "build-your-own smart city kit" for EdTech classrooms.

---

## 👥 Roles & Organization (Team 22)
* **CEO / Project Lead**
* **CTO / System Architecture**
* **Creative Director**
* **Hardware & Fabrication Support**
