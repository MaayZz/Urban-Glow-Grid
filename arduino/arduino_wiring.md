# 🔌 Guide de Câblage & Configuration des Pins — Arduino Mega 2560

Ce document décrit les connexions électriques réelles utilisées sur le prototype physique final de **Urban Glow Grid**. Les affectations ci-dessous correspondent exactement aux définitions du code de production final (`arduino/urban_glow_grid_mega_final/urban_glow_grid_mega_final.ino`).

---

## 🎛 Tableau de Câblage Complet

| Composant Physique | Type de Signal | Pin Arduino | Mode Pin | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Écran OLED (1.3 pouce)** | I2C (SDA) | **Broche SDA (D20)** | Entrée/Sortie | Ligne de données I2C de l'afficheur OLED |
| **Écran OLED (1.3 pouce)** | I2C (SCL) | **Broche SCL (D21)** | Sortie | Ligne d'horloge I2C de l'afficheur OLED |
| **Potentiomètre 1** | Entrée Analogue | **A0** | INPUT | Réglage de charge de la Zone 1 |
| **Potentiomètre 2** | Entrée Analogue | **A1** | INPUT | Réglage de charge de la Zone 2 |
| **Potentiomètre 3** | Entrée Analogue | **A2** | INPUT | Réglage de charge de la Zone 3 |
| **Potentiomètre 4** | Entrée Analogue | **A3** | INPUT | Réglage de charge de la Zone 4 |
| **Potentiomètre 5** | Entrée Analogue | **A4** | INPUT | Réglage de charge de la Zone 5 |
| **Potentiomètre 6** | Entrée Analogue | **A5** | INPUT | Réglage de charge de la Zone 6 |
| **Ruban LED 17cm (Zone 1)** | Sortie Digitale | **Broche 2** | OUTPUT | Indicateur LED de la Zone 1 |
| **Ruban LED 17cm (Zone 2)** | Sortie Digitale | **Broche 3** | OUTPUT | Indicateur LED de la Zone 2 |
| **Ruban LED 17cm (Zone 3)** | Sortie Digitale | **Broche 4** | OUTPUT | Indicateur LED de la Zone 3 |
| **Ruban LED 17cm (Zone 4)** | Sortie Digitale | **Broche 5** | OUTPUT | Indicateur LED de la Zone 4 |
| **Ruban LED 17cm (Zone 5)** | Sortie Digitale | **Broche 6** | OUTPUT | Indicateur LED de la Zone 5 |
| **Ruban LED 17cm (Zone 6)** | Sortie Digitale | **Broche 7** | OUTPUT | Indicateur LED de la Zone 6 |
| **Ruban LED 10cm (Mon. 1)** | Sortie Digitale | **Broche 8** | OUTPUT | Indicateur LED du Monument 1 |
| **Ruban LED 10cm (Mon. 2)** | Sortie Digitale | **Broche 9** | OUTPUT | Indicateur LED du Monument 2 |
| **Speaker 1** | Sortie PWM | **Broche 22** | OUTPUT | Haut-parleur principal (Sons système et sirènes d'alarme) |
| **Speaker 2** | Sortie PWM | **Broche 24** | OUTPUT | Haut-parleur secondaire (Bruits de clic / battement de cœur) |
| **Bouton 1 (Start)** | Entrée Digitale | **Broche 26** | INPUT_PULLUP | Bouton poussoir pour lancer la partie |
| **Bouton 2 (Reset)** | Entrée Digitale | **Broche 28** | INPUT_PULLUP | Bouton poussoir pour réinitialiser le jeu |
| **Bouton 3 (Monument 1)** | Entrée Digitale | **Broche 30** | INPUT_PULLUP | Bouton pour activer/désactiver le Monument 1 |
| **Bouton 4 (Monument 2)** | Entrée Digitale | **Broche 32** | INPUT_PULLUP | Bouton pour activer/désactiver le Monument 2 |

---

## 🛠 Détails du Câblage

### 1. Les 6 Potentiomètres
* Les broches extérieures sont connectées au **5V** et au **GND** de l'Arduino.
* La broche centrale (curseur) est reliée directement aux entrées analogiques `A0` à `A5` de l'Arduino Mega.

### 2. Les 4 Boutons
* Configurés en **active-low** (INPUT_PULLUP). Une borne est connectée à la broche Arduino (26/28/30/32) et l'autre est reliée à la masse commune (GND). 

### 3. Les Rubans LED (WS2812B)
* Les lignes de données (`DIN`) des 6 rubans de 17cm et des 2 rubans de 10cm sont connectées aux broches digitales `2` à `9`.
* Placez une **résistance de 330 ohms** en série entre chaque broche de sortie de l'Arduino et l'entrée du ruban LED.

### 4. L'Écran OLED (1.3 pouce)
* Branché sur le bus I2C matériel de la carte Arduino Mega 2560 (broches dédiées **SDA / D20** et **SCL / D21**).
* Alimenté via la broche **3.3V** (ou 5V selon le modèle) et GND.

### 5. Les 2 Speakers
* Les broches `22` et `24` sont reliées en série avec une **résistance de 100 ohms** à la borne positive de chaque haut-parleur. La borne négative est connectée au GND commun.
