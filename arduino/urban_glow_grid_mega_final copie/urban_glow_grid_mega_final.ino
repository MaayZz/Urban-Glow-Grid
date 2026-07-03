/*
  Urban Glow Grid - Version Mega 2560 (v3 - The Hybrid Storm)
  
  Mecaniques :
  - L'Accrochage : Demarrage aleatoire. Le joueur doit tourner les 6 pots
    pour trouver et accrocher la valeur aleatoire de chaque zone.
  - La Tempete : Vague d'energie globale (Sinusoide) qui perturbe le reseau
    en temps reel. Le joueur doit compenser.
  - Monuments : 2 Boutons independants pour 2 rubans 10cm.
*/

#include <Wire.h>
#include "SSD1306Ascii.h"
#include "SSD1306AsciiWire.h"
#include <Adafruit_NeoPixel.h>

// --- Configuration OLED ---
#define I2C_ADDRESS 0x3C
SSD1306AsciiWire oled;

// --- Configuration Pins Mega ---
const int potPins[6] = {A0, A1, A2, A3, A4, A5};

const int mainStripPins[6] = {2, 3, 4, 5, 6, 7};
const int secStripPins[2] = {8, 9};

const int speaker1 = 22;
const int speaker2 = 24;

const int btnStart = 26;
const int btnReset = 28;
const int btnMonument1 = 30; // Ex btnZone1
const int btnMonument2 = 32; // Ex btnZone2

// --- Configuration Rubans LED ---
#define LEDS_MAIN 10 
#define LEDS_SEC  5  

Adafruit_NeoPixel mainStrips[6] = {
  Adafruit_NeoPixel(LEDS_MAIN, mainStripPins[0], NEO_GRB + NEO_KHZ800),
  Adafruit_NeoPixel(LEDS_MAIN, mainStripPins[1], NEO_GRB + NEO_KHZ800),
  Adafruit_NeoPixel(LEDS_MAIN, mainStripPins[2], NEO_GRB + NEO_KHZ800),
  Adafruit_NeoPixel(LEDS_MAIN, mainStripPins[3], NEO_GRB + NEO_KHZ800),
  Adafruit_NeoPixel(LEDS_MAIN, mainStripPins[4], NEO_GRB + NEO_KHZ800),
  Adafruit_NeoPixel(LEDS_MAIN, mainStripPins[5], NEO_GRB + NEO_KHZ800)
};

Adafruit_NeoPixel secStrips[2] = {
  Adafruit_NeoPixel(LEDS_SEC, secStripPins[0], NEO_GRB + NEO_KHZ800),
  Adafruit_NeoPixel(LEDS_SEC, secStripPins[1], NEO_GRB + NEO_KHZ800)
};

// --- Variables de Jeu ---
enum GameState {
  STATE_READY,
  STATE_PLAYING,
  STATE_BLACKOUT,
  STATE_TIMEOUT,
  STATE_VICTORY
};

GameState currentState = STATE_READY;

// Etat des monuments
bool monument1On = false;
bool monument2On = false;
unsigned long lastDebounceTime1 = 0;
unsigned long lastDebounceTime2 = 0;
const unsigned long debounceDelay = 250;

// Logique Hybride (Accrochage + Tempete)
bool zoneHooked[6] = {false};
int zoneBasePower[6] = {0}; // Valeur "interne" de la zone
unsigned long hookFlashTime[6] = {0}; // Pour le clignotement vert

int zonePower[6] = {0}; // Valeur finale (Base + Vague)
int lastZonePower[6] = {-1, -1, -1, -1, -1, -1};
bool zoneActive[6] = {false};

bool isOverloaded = false;
unsigned long overloadStartTime = 0;
bool isVictoryTimerRunning = false;
unsigned long victoryStartTime = 0;

// Variables du Chronometre global
const unsigned long GAME_DURATION_MS = 180000; // 3 minutes
unsigned long gameStartTime = 0;

const int MIN_POWER_TO_ACTIVATE = 15; 
const int OVERLOAD_THRESHOLD = 80;    
const int OVERLOAD_DELAY = 5000;      
const int VICTORY_DELAY = 5000;       

unsigned long lastOledUpdate = 0;
unsigned long lastSirenTime = 0;
bool sirenHigh = false;

void setup() {
  Serial.begin(9600);
  randomSeed(analogRead(A15)); // Graine pour l'aleatoire
  
  Wire.begin();
  oled.begin(&Adafruit128x64, I2C_ADDRESS);
  oled.setFont(System5x7);
  
  pinMode(btnStart, INPUT_PULLUP);
  pinMode(btnReset, INPUT_PULLUP);
  pinMode(btnMonument1, INPUT_PULLUP);
  pinMode(btnMonument2, INPUT_PULLUP);
  
  pinMode(speaker1, OUTPUT);
  pinMode(speaker2, OUTPUT);

  for(int i=0; i<6; i++) {
    mainStrips[i].begin();
    mainStrips[i].show();
  }
  for(int i=0; i<2; i++) {
    secStrips[i].begin();
    secStrips[i].show();
  }

  showReadyScreen();
}

void loop() {
  if (digitalRead(btnReset) == LOW) {
    tone(speaker1, 300, 200);
    delay(200);
    resetGame();
  }

  switch(currentState) {
    case STATE_READY:
      if (digitalRead(btnStart) == LOW) {
        attemptStartGame();
      }
      playBreathingAnimation();
      break;
      
    case STATE_PLAYING:
      playGame();
      break;
      
    case STATE_BLACKOUT:
      playBlackoutAnimation();
      break;

    case STATE_TIMEOUT:
      playTimeoutAnimation();
      break;
      
    case STATE_VICTORY:
      playVictoryAnimation();
      break;
  }
}

// ==========================================
// FONCTIONS DE LOGIQUE DE JEU
// ==========================================

void attemptStartGame() {
  // Initialisation Aleatoire !
  for (int i = 0; i < 6; i++) {
    zoneHooked[i] = false;
    zoneBasePower[i] = random(15, 95); // Démarrage chaotique
    hookFlashTime[i] = 0;
  }

  tone(speaker1, 1000, 100);
  delay(150);
  tone(speaker1, 1500, 300);
  
  currentState = STATE_PLAYING;
  monument1On = false;
  monument2On = false;
  isOverloaded = false;
  isVictoryTimerRunning = false;
  gameStartTime = millis();
  
  for(int i=0; i<6; i++) lastZonePower[i] = -1;

  turnOffAllStrips();
  oled.clear(); 
  updateOledPlaying(0, false, 0, GAME_DURATION_MS, false);
}

void resetGame() {
  currentState = STATE_READY;
  turnOffAllStrips();
  showReadyScreen();
}

void playGame() {
  unsigned long currentMillis = millis();

  // 1. Gestion du Chronometre
  long timeElapsed = currentMillis - gameStartTime;
  long timeRemaining = GAME_DURATION_MS - timeElapsed;

  if (timeRemaining <= 0) {
    triggerTimeout();
    return;
  }

  // 2. Boutons des Monuments (Decoratifs)
  if (digitalRead(btnMonument1) == LOW && (currentMillis - lastDebounceTime1 > debounceDelay)) {
    monument1On = !monument1On; 
    lastDebounceTime1 = currentMillis;
    if (monument1On) {
      tone(speaker2, 1200, 100);
      setSecStripColor(0, 0, 255, 150); 
    } else {
      tone(speaker2, 600, 100);
      setSecStripColor(0, 0, 0, 0); 
    }
  }
  
  if (digitalRead(btnMonument2) == LOW && (currentMillis - lastDebounceTime2 > debounceDelay)) {
    monument2On = !monument2On; 
    lastDebounceTime2 = currentMillis;
    if (monument2On) {
      tone(speaker2, 1200, 100);
      setSecStripColor(1, 0, 255, 150); 
    } else {
      tone(speaker2, 600, 100);
      setSecStripColor(1, 0, 0, 0); 
    }
  }

  // 3. Generer la Vague d'Energie Globale (La Tempete)
  // Combine 2 sinusoides pour faire une vague imprevisible entre -25% et +25%
  int waveOffset = (sin(currentMillis / 2500.0) * 15.0) + (sin(currentMillis / 900.0) * 10.0);

  // 4. Mise a jour des zones
  int totalPower = 0;
  int activeZonesCount = 0;
  bool allHooked = true;

  for (int i = 0; i < 6; i++) {
    int potRaw = analogRead(potPins[i]);
    int potPercent = map(potRaw, 0, 1023, 0, 100);
    
    if (!zoneHooked[i]) {
      allHooked = false;
      // Le joueur doit croiser la valeur aleatoire (marge de +/- 4%)
      if (abs(potPercent - zoneBasePower[i]) <= 4) {
        zoneHooked[i] = true;
        hookFlashTime[i] = currentMillis; // Lance l'effet visuel vert
        tone(speaker2, 1000 + (i * 200), 150); // Petit bip de succes
      }
    } else {
      // Si on est accroché, le pot controle la base
      zoneBasePower[i] = potPercent;
    }

    // Puissance finale = Base (aleatoire ou controllee) + Vague (Tempete)
    int finalPower = zoneBasePower[i] + waveOffset;
    finalPower = constrain(finalPower, 0, 100); // Borne entre 0 et 100
    
    zonePower[i] = finalPower;
    
    if (finalPower > MIN_POWER_TO_ACTIVATE) {
      zoneActive[i] = true;
      activeZonesCount++;
    } else {
      zoneActive[i] = false;
    }

    totalPower += finalPower;

    // ANTI-FLICKER : MAJ uniquement si besoin ou si flash vert en cours
    bool isFlashing = (currentMillis - hookFlashTime[i] < 300) && zoneHooked[i];
    if (finalPower != lastZonePower[i] || isFlashing) {
      updateMainStrip(i, finalPower, isFlashing);
      lastZonePower[i] = finalPower;
    }
  }

  int averageLoad = totalPower / 6;

  // 5. Logique de Surcharge
  if (averageLoad > OVERLOAD_THRESHOLD) {
    if (!isOverloaded) {
      isOverloaded = true;
      overloadStartTime = currentMillis;
      isVictoryTimerRunning = false;
    }
    
    if (currentMillis - lastSirenTime > 400) {
      lastSirenTime = currentMillis;
      sirenHigh = !sirenHigh;
      if (sirenHigh) tone(speaker1, 800, 200);
      else tone(speaker1, 600, 200);
    }

    if (currentMillis - overloadStartTime > OVERLOAD_DELAY) {
      triggerBlackout();
      return;
    }
  } else {
    isOverloaded = false;
  }

  // 6. Logique de Victoire
  if (activeZonesCount == 6 && !isOverloaded && allHooked) {
    if (!isVictoryTimerRunning) {
      isVictoryTimerRunning = true;
      victoryStartTime = currentMillis;
    }
    if (currentMillis - victoryStartTime > VICTORY_DELAY) {
      triggerVictory();
      return;
    }
  } else {
    isVictoryTimerRunning = false;
  }

  // 7. Mise a jour OLED a 5 FPS (200ms)
  if (currentMillis - lastOledUpdate > 200) {
    updateOledPlaying(averageLoad, isOverloaded, currentMillis, timeRemaining, !allHooked);
    lastOledUpdate = currentMillis;
  }
}

void triggerBlackout() {
  currentState = STATE_BLACKOUT;
  turnOffAllStrips();
  tone(speaker1, 100, 500);
  tone(speaker2, 80, 800);
  
  oled.clear();
  oled.set2X();
  oled.setCursor(0, 2);
  oled.print(" BLACKOUT");
  oled.set1X();
  oled.setCursor(15, 6);
  oled.print("Press RESET to retry");
}

void triggerTimeout() {
  currentState = STATE_TIMEOUT;
  turnOffAllStrips();
  
  tone(speaker1, 300, 400); delay(450);
  tone(speaker1, 250, 400); delay(450);
  tone(speaker1, 200, 800);
  
  oled.clear();
  oled.set2X();
  oled.setCursor(0, 2);
  oled.print(" TIME OUT");
  oled.set1X();
  oled.setCursor(15, 6);
  oled.print("Press RESET to retry");
}

void triggerVictory() {
  currentState = STATE_VICTORY;
  
  int melody[] = {523, 659, 784, 1046}; 
  for (int i=0; i<4; i++) {
    tone(speaker1, melody[i], 150);
    delay(200);
  }
  
  oled.clear();
  oled.set2X();
  oled.setCursor(5, 2);
  oled.print(" VICTORY !");
  oled.set1X();
  oled.setCursor(5, 6);
  oled.print("Grid is stabilized.");
}

// ==========================================
// FONCTIONS D'AFFICHAGE ET D'ANIMATION
// ==========================================

void showReadyScreen() {
  oled.clear();
  oled.set2X();
  oled.setCursor(0, 1);
  oled.println("  SYSTEM  ");
  oled.println("  READY   ");
  oled.set1X();
  oled.setCursor(0, 6);
  oled.print(">> PRESS START BUTTON <<");
}

void updateOledPlaying(int load, bool overload, unsigned long currentMillis, long timeRemaining, bool needsHooking) {
  int secondsRemaining = timeRemaining / 1000;
  int m = secondsRemaining / 60;
  int s = secondsRemaining % 60;

  oled.set1X();
  oled.setCursor(80, 0);
  oled.print("T: 0");
  oled.print(m);
  oled.print(":");
  if (s < 10) oled.print("0");
  oled.print(s);
  oled.print(" ");

  oled.set2X();
  oled.setCursor(0, 2);
  if (overload) {
    if ((currentMillis / 250) % 2 == 0) {
      oled.print(" OVERLOAD! ");
    } else {
      oled.print("           "); 
    }
  } else {
    oled.print("LOAD: ");
    if(load < 100) oled.print(" ");
    if(load < 10) oled.print(" ");
    oled.print(load);
    oled.print("%  "); 
  }

  oled.set1X();
  oled.setCursor(0, 5);
  if (needsHooking) {
    if ((currentMillis / 300) % 2 == 0) oled.print("FIND TARGETS !");
    else oled.print("              ");
  } else {
    oled.print("Zones: ");
    for (int i=0; i<6; i++) {
      if (zoneActive[i]) oled.print("O ");
      else oled.print("X ");
    }
  }

  oled.setCursor(0, 7);
  if (overload) {
    oled.print("CRITICAL: DANGER!   ");
  } else if (isVictoryTimerRunning) {
    oled.print("STABILIZING... HOLD!");
  } else if (needsHooking) {
    oled.print("Turn pots to sync...");
  } else {
    oled.print("Keep load < 80%     ");
  }
}

void updateMainStrip(int stripIndex, int powerPercent, bool isFlashingGreen) {
  uint32_t color;

  if (isFlashingGreen) {
    color = mainStrips[stripIndex].Color(0, 255, 0); // Flash vert vif
  } else {
    int brightness = map(powerPercent, 0, 100, 0, 255);
    if (powerPercent < 5) {
      color = mainStrips[stripIndex].Color(0, 0, 0); 
    } else if (powerPercent > 95) {
      color = mainStrips[stripIndex].Color(255, 255, 255);
    } else {
      color = mainStrips[stripIndex].Color(brightness, brightness*0.7, brightness*0.1);
    }
  }

  for (int i = 0; i < LEDS_MAIN; i++) {
    mainStrips[stripIndex].setPixelColor(i, color);
  }
  mainStrips[stripIndex].show();
}

void setSecStripColor(int stripIndex, int r, int g, int b) {
  uint32_t color = secStrips[stripIndex].Color(r, g, b);
  for (int i=0; i<LEDS_SEC; i++) {
    secStrips[stripIndex].setPixelColor(i, color);
  }
  secStrips[stripIndex].show();
}

void turnOffAllStrips() {
  for(int i=0; i<6; i++) {
    mainStrips[i].clear();
    mainStrips[i].show();
  }
  for(int i=0; i<2; i++) {
    secStrips[i].clear();
    secStrips[i].show();
  }
}

void playBreathingAnimation() {
  static unsigned long lastUpdate = 0;
  if(millis() - lastUpdate < 50) return;
  lastUpdate = millis();

  unsigned long t = millis();
  int brightness = (sin(t / 500.0) + 1.0) * 30; 
  for(int i=0; i<6; i++) {
    for (int j=0; j<LEDS_MAIN; j++) {
      mainStrips[i].setPixelColor(j, mainStrips[i].Color(brightness, brightness*0.5, 0));
    }
    mainStrips[i].show();
  }
}

void playBlackoutAnimation() {
  static unsigned long lastUpdate = 0;
  if(millis() - lastUpdate < 250) return;
  lastUpdate = millis();

  if ((millis() / 500) % 2 == 0) {
    for(int i=0; i<6; i++) {
      for (int j=0; j<LEDS_MAIN; j++) mainStrips[i].setPixelColor(j, 255, 0, 0);
      mainStrips[i].show();
    }
  } else {
    turnOffAllStrips();
  }
}

void playTimeoutAnimation() {
  static unsigned long lastUpdate = 0;
  if(millis() - lastUpdate < 250) return;
  lastUpdate = millis();

  if ((millis() / 500) % 2 == 0) {
    for(int i=0; i<6; i++) {
      for (int j=0; j<LEDS_MAIN; j++) mainStrips[i].setPixelColor(j, 0, 0, 255); 
      mainStrips[i].show();
    }
  } else {
    turnOffAllStrips();
  }
}

void playVictoryAnimation() {
  static unsigned long lastUpdate = 0;
  if(millis() - lastUpdate < 20) return;
  lastUpdate = millis();

  long firstPixelHue = millis() * 256; 
  for(int i=0; i<6; i++) {
    for(int j=0; j<LEDS_MAIN; j++) {
      int pixelHue = firstPixelHue + (j * 65536L / LEDS_MAIN);
      mainStrips[i].setPixelColor(j, mainStrips[i].gamma32(mainStrips[i].ColorHSV(pixelHue)));
    }
    mainStrips[i].show();
  }
  for(int i=0; i<2; i++) {
    for(int j=0; j<LEDS_SEC; j++) {
      int pixelHue = firstPixelHue + (j * 65536L / LEDS_SEC);
      secStrips[i].setPixelColor(j, secStrips[i].gamma32(secStrips[i].ColorHSV(pixelHue)));
    }
    secStrips[i].show();
  }
}
