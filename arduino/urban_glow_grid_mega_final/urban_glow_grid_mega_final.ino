/*
  Urban Glow Grid - Version Mega 2560 (v7 - Fenetre de Tir)
  
  Mecaniques Finales :
  - L'Accrochage (Hack) + Pannes (System Bug)
  - Vagues d'energie
  - Jauge OLED 21 caracteres Dynamique avec O et @
  - Underload (45%) et Overload (85%)
  - Target Load (Aleatoire par partie)
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
const int btnMonument1 = 30; 
const int btnMonument2 = 32; 

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

bool monument1On = false;
bool monument2On = false;
unsigned long lastDebounceTime1 = 0;
unsigned long lastDebounceTime2 = 0;
const unsigned long debounceDelay = 250;

bool zoneHooked[6] = {false};
int zoneBasePower[6] = {0}; 
unsigned long hookFlashTime[6] = {0}; 

int zonePower[6] = {0}; 
int lastZonePower[6] = {-1, -1, -1, -1, -1, -1};
int lastVisualState[6] = {0}; 
bool zoneActive[6] = {false};

unsigned long lastBreakdownTime = 0;
unsigned long nextBreakdownDelay = 15000;

bool isOverloaded = false;
bool isUnderloaded = false;
unsigned long overloadStartTime = 0;
unsigned long underloadStartTime = 0;
unsigned long lastHeartbeat = 0;
bool isVictoryTimerRunning = false;
unsigned long victoryStartTime = 0;

const unsigned long GAME_DURATION_MS = 180000; 
unsigned long gameStartTime = 0;
long finalScore = 0;
long finalTimeRemaining = 0;

const int MIN_POWER_TO_ACTIVATE = 15; 
const int UNDERLOAD_THRESHOLD = 30;   // 30% MIN
const int OVERLOAD_THRESHOLD = 85;    // 85% MAX
const int DANGER_DELAY = 2500;        
const int VICTORY_DELAY = 5000;       

// La Cible (Fenêtre de Tir)
int targetMin = 60;
int targetMax = 65;

unsigned long lastOledUpdate = 0;
unsigned long lastSirenTime = 0;
bool sirenHigh = false;
String blackoutReason = "";

void setup() {
  Serial.begin(9600);
  randomSeed(analogRead(A15)); 
  
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
  // Generation de la Cible (Delta strict de 5%)
  targetMin = random(60, 76);
  targetMax = targetMin + 5; 
  
  for (int i = 0; i < 6; i++) {
    zoneHooked[i] = false;
    zoneBasePower[i] = random(20, 85); 
    hookFlashTime[i] = 0;
  }

  tone(speaker1, 1000, 100);
  delay(150);
  tone(speaker1, 1500, 300);
  
  currentState = STATE_PLAYING;
  monument1On = false;
  monument2On = false;
  isOverloaded = false;
  isUnderloaded = false;
  isVictoryTimerRunning = false;
  gameStartTime = millis();
  
  lastBreakdownTime = millis();
  nextBreakdownDelay = random(15000, 25000); 

  for(int i=0; i<6; i++) {
    lastZonePower[i] = -1;
    lastVisualState[i] = -1;
  }

  turnOffAllStrips();
  oled.clear(); 
  updateOledPlaying(0, false, false, 0, GAME_DURATION_MS, false);
}

void resetGame() {
  currentState = STATE_READY;
  turnOffAllStrips();
  showReadyScreen();
}

void playGame() {
  unsigned long currentMillis = millis();

  // 1. Chronometre
  long timeElapsed = currentMillis - gameStartTime;
  long timeRemaining = GAME_DURATION_MS - timeElapsed;

  if (timeRemaining <= 0) {
    triggerTimeout();
    return;
  }

  // 2. Panne Aleatoire (System Bug)
  if (currentMillis - lastBreakdownTime > nextBreakdownDelay) {
    int zoneToBreak = random(0, 6);
    zoneHooked[zoneToBreak] = false;
    zoneBasePower[zoneToBreak] = random(20, 85); 
    tone(speaker1, 200, 400); 
    
    lastBreakdownTime = currentMillis;
    nextBreakdownDelay = random(15000, 30000); 
  }

  // 3. Boutons Monuments
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

  // 4. Vague d'Energie (Tres Ralentie et Adoucie)
  int waveOffset = (sin(currentMillis / 8000.0) * 12.0) + (sin(currentMillis / 3500.0) * 8.0);

  // 5. Mise a jour des zones
  int totalPower = 0;
  int activeZonesCount = 0;
  bool allHooked = true;

  for (int i = 0; i < 6; i++) {
    int potRaw = analogRead(potPins[i]);
    int potPercent = map(potRaw, 0, 1023, 0, 100);
    
    if (!zoneHooked[i]) {
      allHooked = false;
      if (abs(potPercent - zoneBasePower[i]) <= 5) {
        zoneHooked[i] = true;
        hookFlashTime[i] = currentMillis; 
        tone(speaker2, 1000 + (i * 200), 150); 
      }
    } else {
      zoneBasePower[i] = potPercent;
    }

    int finalPower = zoneBasePower[i] + waveOffset;
    finalPower = constrain(finalPower, 0, 100); 
    
    zonePower[i] = finalPower;
    
    if (finalPower > MIN_POWER_TO_ACTIVATE) {
      zoneActive[i] = true;
      activeZonesCount++;
    } else {
      zoneActive[i] = false;
    }

    totalPower += finalPower;

    bool isFlashingGreen = (currentMillis - hookFlashTime[i] < 300) && zoneHooked[i];
    bool isBroken = !zoneHooked[i];
    
    int currentVisualState = 0;
    if (isFlashingGreen) currentVisualState = 1;
    else if (isBroken) currentVisualState = ((currentMillis / 150) % 2 == 0) ? 2 : 3;

    if (finalPower != lastZonePower[i] || currentVisualState != lastVisualState[i]) {
      updateMainStrip(i, finalPower, isFlashingGreen, isBroken, currentMillis);
      lastZonePower[i] = finalPower;
      lastVisualState[i] = currentVisualState;
    }
  }

  int averageLoad = totalPower / 6;

  // 6. HEARTBEAT Audio
  int stressLevel = 0; 
  if (averageLoad < 50) stressLevel = map(averageLoad, 50, UNDERLOAD_THRESHOLD, 0, 100);
  else if (averageLoad > 80) stressLevel = map(averageLoad, 80, OVERLOAD_THRESHOLD, 0, 100);
  
  if (timeRemaining < 30000) {
    int timeStress = map(timeRemaining, 30000, 0, 0, 100);
    stressLevel = max(stressLevel, timeStress);
  }
  
  if (stressLevel > 0 && !isOverloaded && !isUnderloaded) {
    stressLevel = constrain(stressLevel, 0, 100);
    int beatInterval = map(stressLevel, 0, 100, 1500, 250);
    if (currentMillis - lastHeartbeat > beatInterval) {
      lastHeartbeat = currentMillis;
      tone(speaker2, 80, 50); 
    }
  }

  // 7. OVERLOAD (> 85%)
  if (averageLoad > OVERLOAD_THRESHOLD) {
    if (!isOverloaded) {
      isOverloaded = true;
      overloadStartTime = currentMillis;
      isVictoryTimerRunning = false;
    }
    if (currentMillis - lastSirenTime > 300) {
      lastSirenTime = currentMillis;
      sirenHigh = !sirenHigh;
      if (sirenHigh) tone(speaker1, 800, 200);
      else tone(speaker1, 600, 200);
    }
    if (currentMillis - overloadStartTime > DANGER_DELAY) {
      triggerBlackout("OVERLOAD MAX");
      return;
    }
  } else {
    isOverloaded = false;
  }

  // 8. UNDERLOAD (< 45%)
  if (averageLoad < UNDERLOAD_THRESHOLD) {
    if (!isUnderloaded) {
      isUnderloaded = true;
      underloadStartTime = currentMillis;
      isVictoryTimerRunning = false;
    }
    if (currentMillis - lastSirenTime > 400) {
      lastSirenTime = currentMillis;
      sirenHigh = !sirenHigh;
      if (sirenHigh) tone(speaker1, 300, 300);
      else tone(speaker1, 200, 300);
    }
    if (currentMillis - underloadStartTime > DANGER_DELAY) {
      triggerBlackout("UNDERLOADED");
      return;
    }
  } else {
    isUnderloaded = false;
  }

  // 9. Victoire (Dans la Fenetre !)
  bool isTargetHit = (averageLoad >= targetMin && averageLoad <= targetMax);

  if (activeZonesCount == 6 && !isOverloaded && !isUnderloaded && allHooked && isTargetHit) {
    if (!isVictoryTimerRunning) {
      isVictoryTimerRunning = true;
      victoryStartTime = currentMillis;
    }
    if (currentMillis - victoryStartTime > VICTORY_DELAY) {
      finalTimeRemaining = timeRemaining;
      finalScore = timeRemaining / 10; 
      triggerVictory();
      return;
    }
  } else {
    isVictoryTimerRunning = false;
  }

  // 10. OLED
  if (currentMillis - lastOledUpdate > 200) {
    updateOledPlaying(averageLoad, isOverloaded, isUnderloaded, currentMillis, timeRemaining, !allHooked);
    lastOledUpdate = currentMillis;
  }
}

void triggerBlackout(String reason) {
  currentState = STATE_BLACKOUT;
  blackoutReason = reason;
  turnOffAllStrips();
  tone(speaker1, 100, 500);
  tone(speaker2, 80, 800);
  
  oled.clear();
  oled.set1X();
  oled.setCursor(0, 1);
  oled.print("   SYSTEM BLACKOUT   ");
  oled.setCursor(0, 3);
  oled.print("FATAL: "); oled.print(reason);
  oled.setCursor(0, 6);
  oled.print("  >> PRESS RESET <<  ");
}

void triggerTimeout() {
  currentState = STATE_TIMEOUT;
  turnOffAllStrips();
  
  tone(speaker1, 300, 400); delay(450);
  tone(speaker1, 250, 400); delay(450);
  tone(speaker1, 200, 800);
  
  oled.clear();
  oled.set1X();
  oled.setCursor(0, 2);
  oled.print("    TIME IS UP !     ");
  oled.setCursor(0, 5);
  oled.print("  >> PRESS RESET <<  ");
}

void triggerVictory() {
  currentState = STATE_VICTORY;
  
  int melody[] = {523, 659, 784, 1046}; 
  for (int i=0; i<4; i++) {
    tone(speaker1, melody[i], 150);
    delay(200);
  }
  
  oled.clear();
  oled.set1X();
  oled.setCursor(0, 0);
  oled.print(" *** VICTORY ! ***   ");
  oled.setCursor(0, 2);
  oled.print("SCORE: "); oled.print(finalScore); oled.print(" PTS");
  
  int s = (finalTimeRemaining / 1000) % 60;
  int m = (finalTimeRemaining / 1000) / 60;
  oled.setCursor(0, 3);
  oled.print("TIME LEFT: 0"); oled.print(m); oled.print(":");
  if (s<10) oled.print("0"); oled.print(s);
  
  oled.setCursor(0, 6);
  oled.print("  >> PRESS RESET <<  ");
}

// ==========================================
// FONCTIONS D'AFFICHAGE ET D'ANIMATION
// ==========================================

void showReadyScreen() {
  oled.clear();
  oled.set1X();
  oled.setCursor(0, 0);
  oled.println("=====================");
  oled.println("   URBAN GLOW GRID   ");
  oled.println("=====================");
  oled.println("");
  oled.println("   STATUS : ONLINE   ");
  oled.println("");
  oled.println("  >> PRESS START <<  ");
}

void updateOledPlaying(int load, bool overload, bool underload, unsigned long currentMillis, long timeRemaining, bool needsHooking) {
  int secondsRemaining = timeRemaining / 1000;
  int m = secondsRemaining / 60;
  int s = secondsRemaining % 60;

  oled.set1X();
  
  // LIGNE 0 : Temps et Load 
  oled.setCursor(0, 0);
  oled.print("T: 0"); oled.print(m); oled.print(":");
  if (s < 10) oled.print("0"); oled.print(s);
  oled.print("   LOAD: ");
  if(load < 100) oled.print(" ");
  if(load < 10) oled.print(" ");
  oled.print(load);
  oled.print("%");

  // LIGNE 2 : JAUGE VISUELLE INTELLIGENTE
  String bar = "[";
  int fillEnd = map(load, 0, 100, 1, 19);
  int underPos = map(UNDERLOAD_THRESHOLD, 0, 100, 1, 19);
  int overPos = map(OVERLOAD_THRESHOLD, 0, 100, 1, 19);
  int tMinPos = map(targetMin, 0, 100, 1, 19);
  int tMaxPos = map(targetMax, 0, 100, 1, 19);

  for (int i = 1; i <= 19; i++) {
    if (i >= tMinPos && i <= tMaxPos) {
      if (i <= fillEnd) bar += "@"; // Cible atteinte (pleine)
      else bar += "O"; // Cible vide
    } else {
      if (i <= fillEnd) bar += "=";
      else if (i == underPos || i == overPos) bar += "|";
      else bar += "-";
    }
  }
  bar += "]";
  oled.setCursor(0, 2);
  oled.print(bar);

  // LIGNE 4 : Alertes ou Cible
  oled.setCursor(0, 4);
  if (overload) {
    if ((currentMillis / 250) % 2 == 0) oled.print("! OVERLOAD CRITICAL !");
    else oled.print("                     ");
  } else if (underload) {
    if ((currentMillis / 250) % 2 == 0) oled.print("! UNDERLOAD WARNING !");
    else oled.print("                     ");
  } else if (needsHooking) {
    if ((currentMillis / 300) % 2 == 0) oled.print("  [ SYSTEM BUG ! ]   ");
    else oled.print("                     ");
  } else {
    oled.print("TARGET: "); oled.print(targetMin); oled.print("% - "); 
    oled.print(targetMax); oled.print("%    ");
  }

  // LIGNE 6 : Info Contextuelle
  oled.setCursor(0, 6);
  if (overload || underload) {
    oled.print("DANGER: FIX GRID NOW!");
  } else if (isVictoryTimerRunning) {
    oled.print("STABILIZING... HOLD! ");
  } else if (needsHooking) {
    oled.print("Fix System Bug !     ");
  } else {
    oled.print("Hit Target to Win !  ");
  }
}

void updateMainStrip(int stripIndex, int powerPercent, bool isFlashingGreen, bool isBroken, unsigned long currentMillis) {
  uint32_t color;

  if (isFlashingGreen) {
    color = mainStrips[stripIndex].Color(0, 255, 0); 
  } else if (isBroken) {
    if ((currentMillis / 150) % 2 == 0) color = mainStrips[stripIndex].Color(255, 0, 0);
    else color = mainStrips[stripIndex].Color(0, 0, 0);
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
