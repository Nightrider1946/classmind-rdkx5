#include <WiFi.h>
#include <WebServer.h>
#include <Adafruit_NeoPixel.h>

// ======================
// WiFi Credentials
// ======================
const char* ssid = "Block A";
const char* password = "123456789";

// ======================
// RGB LED Configuration
// ======================
#define LED_PIN 48      // Built-in RGB LED pin for ESP32-S3 N16R8
#define NUMPIXELS 1

Adafruit_NeoPixel pixels(NUMPIXELS, LED_PIN, NEO_GRB + NEO_KHZ800);

// ======================
// Web Server
// ======================
WebServer server(80);

// ======================
// LED Functions
// ======================

void setGreen() {
  pixels.setPixelColor(0, pixels.Color(0, 255, 0));
  pixels.show();
  server.send(200, "text/plain", "GREEN");
}

void setRed() {
  pixels.setPixelColor(0, pixels.Color(255, 0, 0));
  pixels.show();
  server.send(200, "text/plain", "RED");
}

void setBlue() {
  pixels.setPixelColor(0, pixels.Color(0, 0, 255));
  pixels.show();
  server.send(200, "text/plain", "BLUE");
}

void setYellow() {
  pixels.setPixelColor(0, pixels.Color(255, 255, 0));
  pixels.show();
  server.send(200, "text/plain", "YELLOW");
}

void turnOff() {
  pixels.clear();
  pixels.show();
  server.send(200, "text/plain", "OFF");
}

// ======================
// Setup
// ======================

void setup() {

  Serial.begin(115200);

  pixels.begin();
  pixels.clear();
  pixels.show();

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\n");
  Serial.println("=================================");
  Serial.println("WiFi Connected!");
  Serial.print("ESP32 IP Address: ");
  Serial.println(WiFi.localIP());
  Serial.println("=================================");

  server.on("/green", setGreen);
  server.on("/red", setRed);
  server.on("/blue", setBlue);
  server.on("/yellow", setYellow);
  server.on("/off", turnOff);

  server.begin();

  Serial.println("HTTP Server Started");
}

void loop() {
  server.handleClient();
}