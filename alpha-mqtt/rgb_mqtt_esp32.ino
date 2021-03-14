/*********
DOIT ESP32 DEVKIT V1
*********/

#include <WiFi.h>
#include <PubSubClient.h>

//watchdog timer configure
#include "esp_system.h"
const int loopTimeCtl = 0;
hw_timer_t *timer = NULL;
void IRAM_ATTR resetModule(){
    ets_printf("reboot\n");
    esp_restart();
}


// Replace the next variables with your SSID/Password combination
const char* ssid = "Sallyport";
const char* password = "B@l@dAB20!5";

// Add your MQTT Broker IP address, example:
//const char* mqtt_server = "192.168.1.144";
const char* mqtt_server = "seapod.technoid.info";

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
//char msg[50];
int value = 0;
int toggle = 0;

char copy[15];

// LED Pin
const int blue = 32;
const int green = 25;
const int red = 33;
const int gnd = 26;

String redStatus = "red_off";
String greenStatus = "green_off";
String blueStatus = "blue_off";

void setup() {
  Serial.begin(115200);

 
  
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  //watchdog timer set up
  pinMode(loopTimeCtl, INPUT_PULLUP);
  timer = timerBegin(0, 80, true); //timer 0, div 80
  timerAttachInterrupt(timer, &resetModule, true);
  timerAlarmWrite(timer, 3000000, false); //set time in us
  timerAlarmEnable(timer); //enable interrupt

  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(gnd, OUTPUT);
  pinMode(red, OUTPUT);
  pinMode(green, OUTPUT);
  pinMode(blue, OUTPUT);
  digitalWrite(gnd, LOW);
  digitalWrite(red, HIGH);
  delay(500);
  digitalWrite(red, LOW);
  digitalWrite(green, HIGH);
  delay(500);
  digitalWrite(green, LOW);
  digitalWrite(blue, HIGH);
  delay(500);
  digitalWrite(blue, LOW);
}

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();

  // Feel free to add more if statements to control more GPIOs with MQTT

  // If a message is received on the topic esp32/output, you check if the message is either "on" or "off". 
  // Changes the output state according to the message
  if (String(topic) == "test/leds") {
    Serial.println("Changing output to ");
    Serial.println(messageTemp);
    
    
    if(messageTemp == "red_on"){
      digitalWrite(red, HIGH);
      redStatus = messageTemp;
      Serial.println("Red On");
    }
    else if(messageTemp == "red_off"){
      digitalWrite(red, LOW);
      redStatus = messageTemp;
      Serial.println("Red Off");
    }
    else if(messageTemp == "green_on"){
      digitalWrite(green, HIGH);
      greenStatus = messageTemp;
      Serial.println("Green On");
    }
    else if(messageTemp == "green_off"){
      digitalWrite(green, LOW);
      greenStatus = messageTemp;
      Serial.println("Green Off");
    }
    else if(messageTemp == "blue_on"){
      digitalWrite(blue, HIGH);
      blueStatus = messageTemp;
      Serial.println("Blue On");
    }
    else if(messageTemp == "blue_off"){
      digitalWrite(blue, LOW);
      blueStatus = messageTemp;
      Serial.println("Blue Off");
    }
    else if(messageTemp == "request_status"){
      Serial.println(redStatus);
      redStatus.toCharArray(copy, 15);
      client.publish("test/leds/status", copy);
      Serial.println(greenStatus);
      greenStatus.toCharArray(copy, 15);
      client.publish("test/leds/status", copy);
      Serial.println(blueStatus);
      blueStatus.toCharArray(copy, 15);
      client.publish("test/leds/status", copy);
      
    }
    
    messageTemp.toCharArray(copy, 15);
    client.publish("test/leds/status", copy);
    Serial.println(messageTemp);
  }
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");
      // Subscribe
      client.subscribe("test/leds");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}
void loop() {

  timerWrite(timer, 0); //reset timer (feed watchdog)

  
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

 
  long now = millis();
  if (now - lastMsg > 5000) {
    lastMsg = now;
    client.publish("test/leds/heartbeat", "heartbeat");
    if (toggle == 1){
      digitalWrite(LED_BUILTIN, HIGH);
      toggle = 0;
    } else {
      digitalWrite(LED_BUILTIN, LOW);
      toggle = 1;
    }
   }

   
}
