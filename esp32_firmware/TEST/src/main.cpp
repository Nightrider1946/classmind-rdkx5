#include <WiFi.h>
#include <WebServer.h>
#include <Adafruit_NeoPixel.h>
#include "secrets.h"
// ======================
// WiFi Credentials
// ======================
const char* ssid = WIFI_SSID;
const char* password = WIFI_PASSWORD;
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
#define BUZZER_PIN 5

#define MQ_ANALOG_PIN 4
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

void attendanceStartBeep() {

  Serial.println(
    "[BUZZER] Attendance started"
  );

  // One long beep
  digitalWrite(
    BUZZER_PIN,
    HIGH
  );

  delay(1000);

  digitalWrite(
    BUZZER_PIN,
    LOW
  );

  server.send(
    200,
    "text/plain",
    "Attendance start beep"
  );
}

void attendanceEndBeep() {

  Serial.println(
    "[BUZZER] Attendance completed"
  );

  // First short beep
  digitalWrite(
    BUZZER_PIN,
    HIGH
  );

  delay(200);

  digitalWrite(
    BUZZER_PIN,
    LOW
  );

  delay(150);

  // Second short beep
  digitalWrite(
    BUZZER_PIN,
    HIGH
  );

  delay(200);

  digitalWrite(
    BUZZER_PIN,
    LOW
  );

  server.send(
    200,
    "text/plain",
    "Attendance end beep"
  );
}

void getGasSensor() {

  const int sampleCount = 20;

  unsigned long total = 0;

  int minimumValue = 4095;
  int maximumValue = 0;


  for (
    int i = 0;
    i < sampleCount;
    i++
  ) {

    int sensorValue = analogRead(
      MQ_ANALOG_PIN
    );

    total += sensorValue;


    if (
      sensorValue < minimumValue
    ) {

      minimumValue = sensorValue;
    }


    if (
      sensorValue > maximumValue
    ) {

      maximumValue = sensorValue;
    }


    delay(10);
  }


  int averageValue = (
    total / sampleCount
  );


  unsigned long timestamp = millis();


  String json = "{";


  json += "\"sensor\":";
  json += "\"MQ-series analog prototype\"";


  json += ",\"raw_adc\":";
  json += String(
    averageValue
  );


  json += ",\"min_adc\":";
  json += String(
    minimumValue
  );


  json += ",\"max_adc\":";
  json += String(
    maximumValue
  );


  json += ",\"sample_count\":";
  json += String(
    sampleCount
  );


  json += ",\"timestamp_ms\":";
  json += String(
    timestamp
  );


  json += "}";


  Serial.print(
    "[MQ SENSOR] "
  );

  Serial.println(
    json
  );


  server.send(
    200,
    "application/json",
    json
  );
}

// ======================
// Setup
// ======================

void setup() {

  Serial.begin(115200);

  pixels.begin();
  pixels.clear();
  pixels.show();

  pinMode(
    BUZZER_PIN,
    OUTPUT
  );

  digitalWrite(
    BUZZER_PIN,
    LOW
  );

    pinMode(
    MQ_ANALOG_PIN,
    INPUT
  );


  analogReadResolution(
    12
  );


  Serial.println(
    "[MQ SENSOR] ADC initialized"
  );



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
  server.on(
    "/attendance-start",
    attendanceStartBeep
  );

  server.on(
    "/attendance-end",
    attendanceEndBeep
  );

  server.on(
    "/gas",
    getGasSensor
  );


  server.begin();

  Serial.println("HTTP Server Started");
}

void loop() {
  server.handleClient();
}