# 🔌 Guide de Câblage & Configuration des Pins — Arduino Mega 2560

Ce document décrit les connexions électriques réelles utilisées sur le prototype physique final de **Urban Glow Grid**. Les affectations ci-dessous correspondent exactement aux définitions du code de production final (`arduino/urban_glow_grid_mega_final/urban_glow_grid_mega_final.ino`).

---

## 🎛 Tableau de Câblage Complet (Arduino Mega)

| Composant Physique | Type de Signal | Pin Arduino | Mode Pin | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Écran OLED (0.96" SSD1306)** | I2C (SDA) | **Broche SDA (D20)** | Entrée/Sortie | Ligne de données I2C de l'afficheur OLED |
| **Écran OLED (0.96" SSD1306)** | I2C (SCL) | **Broche SCL (D21)** | Sortie | Ligne d'horloge I2C de l'afficheur OLED |
| **Potentiomètre 1 (Zone 1)** | Entrée Analogue | **A0** | INPUT | Molette de réglage de charge pour la zone Haussmann |
| **Potentiomètre 2 (Zone 2)** | Entrée Analogue | **A1** | INPUT | Molette de réglage de charge pour la zone Défense |
| **Potentiomètre 3 (Zone 3)** | Entrée Analogue | **A2** | INPUT | Molette de réglage de charge pour la zone Monuments |
| **Potentiomètre 4 (Zone 4)** | Entrée Analogue | **A3** | INPUT | Molette de réglage de charge pour la zone 4 |
| **Potentiomètre 5 (Zone 5)** | Entrée Analogue | **A4** | INPUT | Molette de réglage de charge pour la zone 5 |
| **Potentiomètre 6 (Zone 6)** | Entrée Analogue | **A5** | INPUT | Molette de réglage de charge pour la zone 6 |
| **Ruban LED Zone 1 (Main)** | Sortie Digitale | **Broche 2** | OUTPUT | 10x LEDs WS2812B sous la zone 1 (Haussmann) |
| **Ruban LED Zone 2 (Main)** | Sortie Digitale | **Broche 3** | OUTPUT | 10x LEDs WS2812B sous la zone 2 (Défense) |
| **Ruban LED Zone 3 (Main)** | Sortie Digitale | **Broche 4** | OUTPUT | 10x LEDs WS2812B sous la zone 3 (Monuments) |
| **Ruban LED Zone 4 (Main)** | Sortie Digitale | **Broche 5** | OUTPUT | 10x LEDs WS2812B sous la zone 4 |
| **Ruban LED Zone 5 (Main)** | Sortie Digitale | **Broche 6** | OUTPUT | 10x LEDs WS2812B sous la zone 5 |
| **Ruban LED Zone 6 (Main)** | Sortie Digitale | **Broche 7** | OUTPUT | 10x LEDs WS2812B sous la zone 6 |
| **Ruban LED Monument 1 (Sec)**| Sortie Digitale | **Broche 8** | OUTPUT | 5x LEDs WS2812B pour l'indicateur du Monument 1 |
| **Ruban LED Monument 2 (Sec)**| Sortie Digitale | **Broche 9** | OUTPUT | 5x LEDs WS2812B pour l'indicateur du Monument 2 |
| **Haut-parleur / Buzzer 1** | Sortie PWM | **Broche 22** | OUTPUT | Haut-parleur principal (Sons système et sirènes d'alarme) |
| **Haut-parleur / Buzzer 2** | Sortie PWM | **Broche 24** | OUTPUT | Haut-parleur secondaire (Bruits de clic / battement de cœur) |
| **Bouton Arcade Lumineux (Start)** | Entrée Digitale | **Broche 26** | INPUT_PULLUP | Initialise la partie de 3 minutes (Bouton poussoir 60mm) |
| **Bouton Arcade (Reset)** | Entrée Digitale | **Broche 28** | INPUT_PULLUP | Interrompt le jeu et réinitialise l'état (Bouton poussoir 24mm) |
| **Interrupteur à Bascule (Mon. 1)**| Entrée Digitale | **Broche 30** | INPUT_PULLUP | SPDT Toggle Switch : Active/Désactive la priorité du Monument 1 |
| **Interrupteur à Bascule (Mon. 2)**| Entrée Digitale | **Broche 32** | INPUT_PULLUP | SPDT Toggle Switch : Active/Désactive la priorité du Monument 2 |
| **Broche de Seed Aléatoire** | Entrée Analogue | **A15** | INPUT (Floating) | Laissée vide / flottante pour initialiser `randomSeed()` |

---

## 🛠 Détails du Matériel & Schéma Électronique

### 1. Dials (Potentiomètres 10k Ohms)
* Les broches extérieures de chaque potentiomètre sont connectées au **5V** et au **GND** de l'Arduino.
* La broche centrale (curseur) est reliée directement aux entrées analogiques `A0` à `A5` de l'Arduino Mega.

### 2. Contrôles de Jeu (Boutons d'Arcade et Commutateurs)
* **Start & Reset** : Boutons poussoirs d'arcade connectés en **active-low** (INPUT_PULLUP). Une borne est connectée à la broche Arduino (26/28) et l'autre est reliée à la masse commune (GND). Aucun besoin de résistance de pull-up externe.
* **Monuments Overrides** : Deux interrupteurs à bascule métalliques (SPDT). La broche centrale est connectée à la broche Arduino (30/32), et l'une des broches latérales est connectée à la masse commune (GND). 

### 3. Rubans LED (NeoPixels WS2812B)
* Les lignes de données (`DIN`) des 6 rubans principaux et des 2 rubans secondaires sont connectées aux broches digitales `2` à `9`.
* **Important** : Placez une **résistance de 330 ohms** en série entre chaque broche de sortie de l'Arduino et l'entrée `DIN` du ruban LED pour protéger les circuits intégrés des pixels.
* **Alimentation Électrique** : Les 70 LEDs (60 principales + 10 secondaires) peuvent consommer jusqu'à 4.2A sous 5V en pleine luminosité. Elles sont alimentées par un **bloc externe 5V 3A dédié** (masse commune partagée avec l'Arduino Mega) pour éviter de griller le régulateur interne de l'Arduino.

### 4. Écran OLED SSD1306 (I2C)
* Branché sur le bus I2C matériel de la carte Arduino Mega 2560 (broches dédiées **SDA / D20** et **SCL / D21**).
* **Alimentation** : Relié à la broche **3.3V** de la carte Mega (ou 5V selon le module d'affichage utilisé) et au GND.
* Pour éviter les plantages de l'I2C (courants avec des fils longs), il est recommandé de mettre des résistances pull-up de **4.7k ohms** entre les lignes SDA/SCL et le VCC.

### 5. Audio (Haut-parleurs 8 Ohms 2W)
* Les broches `22` et `24` sont reliées en série avec une **résistance de 100 ohms** (pour limiter le courant de sortie de la broche Arduino Mega) à la borne positive de chaque haut-parleur. La borne négative est connectée au GND commun.
