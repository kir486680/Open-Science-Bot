#include <ArduinoJson.h>
#include <Servo.h>

Servo myservo1;  
Servo myservo2;  
const int ledPin = 13;
// Motor A connections
int enA = 9;
int in1 = 8;
int in2 = 7;
// Motor B connections
int enB = 4;
int in3 = 5;
int in4 = 6;

// Define a struct to map actions to functions
struct ActionHandler {
  const char* action;
  void (*handler)(JsonObject parameters);
};

// Forward declare the function prototypes first
void grip(JsonObject parameters);
void ungrip(JsonObject parameters);
void pumpA(JsonObject parameters);
void pumpB(JsonObject parameters);
void executeAction(const char* action, ActionHandler* actions, size_t actionCount, JsonObject parameters);

// Now we can define the action handlers
ActionHandler gripperActions[] = {
  {"grip", grip},
  {"ungrip", ungrip}
};

ActionHandler pumpAActions[] = {
  {"run", pumpA}
};

ActionHandler pumpBActions[] = {
  {"run", pumpB}
};

// Create a device handler struct
struct DeviceHandler {
  const char* device;
  ActionHandler* actions;
  size_t actionCount;
};

// Define all available devices
DeviceHandler deviceHandlers[] = {
  {"gripper", gripperActions, sizeof(gripperActions) / sizeof(ActionHandler)},
  {"pumpA", pumpAActions, sizeof(pumpAActions) / sizeof(ActionHandler)},
  {"pumpB", pumpBActions, sizeof(pumpBActions) / sizeof(ActionHandler)}
};

// Implementation of the functions
void grip(JsonObject parameters) {
  int gripper_number = parameters["gripper_number"];
  
  if (gripper_number == 1) {
    myservo1.write(5);
  } else if (gripper_number == 2) {
    myservo2.write(105);
  }

}

void ungrip(JsonObject parameters) {
  int gripper_number = parameters["gripper_number"];
  
  if (gripper_number == 1) {
    myservo1.write(90);
  } else if (gripper_number == 2) {
    myservo2.write(0);
  }
  delay(1000);
}

void pumpA(JsonObject parameters) {
  int duration = parameters["duration"];
  const char* direction = parameters["direction"] | "forward";
  
  analogWrite(enA, 255);
  if (strcmp(direction, "forward") == 0) {
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
  } else {
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
  }
  delay(duration*1000);
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
}

void pumpB(JsonObject parameters) {
  int duration = parameters["duration"];
  const char* direction = parameters["direction"] | "forward";
  
  analogWrite(enB, 255);
  if (strcmp(direction, "forward") == 0) {
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
  } else {
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
  }
  delay(duration*1000);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}

// Find the right device for the command
void executeCommand(const char* device, const char* action, JsonObject parameters) {
  for (size_t i = 0; i < sizeof(deviceHandlers) / sizeof(DeviceHandler); i++) {
    if (strcmp(device, deviceHandlers[i].device) == 0) {
      executeAction(action, deviceHandlers[i].actions, deviceHandlers[i].actionCount, parameters);
      return;
    }
  }
  Serial.println("Unknown device");
}

// Execute Action on device
void executeAction(const char* action, ActionHandler* actions, size_t actionCount, JsonObject parameters) {
  for (size_t i = 0; i < actionCount; ++i) {
    if (strcmp(action, actions[i].action) == 0) {
      actions[i].handler(parameters);
      return;
    }
  }
  Serial.println("Unknown action");
}

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);  // Set the LED pin as an output

  // Set all the motor control pins to outputs
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  
  // Turn off motors - Initial state
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);


  myservo1.attach(4);  // Assigns data pin to your servo object, must be digital port
  myservo2.attach(3);
  
  myservo1.write(90);  // ungripped position for servo1
  myservo2.write(0);
  delay(1000);

}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    StaticJsonDocument<200> doc;
    DeserializationError error = deserializeJson(doc, input);
    
    if (!error) {
      const char* device = doc["device"];
      const char* action = doc["action"];
      JsonObject parameters = doc["parameters"];
      
      // Handle the command based on device
      executeCommand(device, action, parameters);
    }
    
    // Send a response
    StaticJsonDocument<200> response;
    response["status"] = "ok";
    response["device"] = doc["device"];
    response["action"] = doc["action"];
    serializeJson(response, Serial);
    Serial.println();
    digitalWrite(ledPin, HIGH);  // Turn the LED on
    delay(100);                  // Wait for 100 milliseconds
    digitalWrite(ledPin, LOW);   // Turn the LED off
    delay(100);                  // Wait for 100 milliseconds
  }
}