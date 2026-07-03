#include <Wire.h>
#include "SSD1306Ascii.h"
#include "SSD1306AsciiWire.h"
#include <Adafruit_NeoPixel.h>

// --- Configuration OLED ---
#define I2C_ADDRESS 0x3C
SSD1306AsciiWire oled;

// --- Configuration LED ---
// On met 10 LEDs par défaut pour le test (modifiable)
#define LEDS_PER_STRIP 10 
const int stripPins[6] = {2, 3, 4, 5, 6, 7};
Adafruit_NeoPixel strip1(LEDS_PER_STRIP, stripPins[0], NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel strip2(LEDS_PER_STRIP, stripPins[1], NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel strip3(LEDS_PER_STRIP, stripPins[2], NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel strip4(LEDS_PER_STRIP, stripPins[3], NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel strip5(LEDS_PER_STRIP, stripPins[4], NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel strip6(LEDS_PER_STRIP, stripPins[5], NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel* strips[6] = {&strip1, &strip2, &strip3, &strip4, &strip5, &strip6};

// --- Configuration Potentiomètres ---
const int potPins[6] = {A0, A1, A2, A3, A4, A5};

// --- Configuration Boutons ---
const int btnStart = 26;
const int btnReset = 28;

// --- Configuration Speakers ---
const int speaker1 = 22;
const int speaker2 = 24;

void setup() {
  Serial.begin(9600);
  
  // Initialisation I2C et OLED
  Wire.begin();
  oled.begin(&Adafruit128x64, I2C_ADDRESS);
  oled.setFont(System5x7);
  oled.clear();
  oled.println("=== TEST HARDWARE ===");
  oled.println("Test Audio...");

  // Initialisation Boutons
  pinMode(btnStart, INPUT_PULLUP);
  pinMode(btnReset, INPUT_PULLUP);

  // Initialisation Speakers
  pinMode(speaker1, OUTPUT);
  pinMode(speaker2, OUTPUT);

  // Initialisation des 6 rubans LED
  for (int i = 0; i < 6; i++) {
    strips[i]->begin();
    strips[i]->show(); // Tout éteindre au démarrage
  }

  // Petit test audio au démarrage
  tone(speaker1, 1000, 200);
  delay(300);
  tone(speaker2, 1500, 200);
  delay(300);
  
  oled.clear();
  oled.println("=== TEST HARDWARE ===");
  oled.println("Tourne les pots !");
}

void loop() {
  bool needsUpdate = false;
  static unsigned long lastOledUpdate = 0;
  
  // 1. Tester les boutons
  if (digitalRead(btnStart) == LOW) {
    tone(speaker1, 800, 100);
    oled.setCursor(0, 3);
    oled.print("Bouton: START presse ");
    delay(200); // Anti-rebond basique
  }
  
  if (digitalRead(btnReset) == LOW) {
    tone(speaker2, 400, 100);
    oled.setCursor(0, 3);
    oled.print("Bouton: RESET presse ");
    delay(200);
  }

  // 2. Lire les potentiomètres et allumer les LEDs
  for (int i = 0; i < 6; i++) {
    int potValue = analogRead(potPins[i]); // Valeur de 0 à 1023
    
    // On convertit la valeur du potentiomètre (0-1023) en luminosité (0-255)
    int brightness = map(potValue, 0, 1023, 0, 255);
    
    // Si la valeur est très faible, on éteint
    if (brightness < 10) brightness = 0;

    // Allumer tout le ruban avec cette luminosité (en blanc chaud/jaune pour tester)
    for (int j = 0; j < LEDS_PER_STRIP; j++) {
      strips[i]->setPixelColor(j, strips[i]->Color(brightness, brightness * 0.7, brightness * 0.2));
    }
    strips[i]->show();
  }

  // Mettre à jour l'OLED toutes les 500ms avec les valeurs des 2 premiers potentiomètres pour vérifier
  if (millis() - lastOledUpdate > 500) {
    oled.setCursor(0, 5);
    oled.print("Pot 1: "); oled.print(analogRead(potPins[0])); oled.print("   ");
    oled.setCursor(0, 6);
    oled.print("Pot 6: "); oled.print(analogRead(potPins[5])); oled.print("   ");
    lastOledUpdate = millis();
  }
}
