import paho.mqtt.client as mqtt
import time

# MQTT broker configuration
broker_address = "localhost"
broker_port = 1883
keepalive = 60

# Topics for communication
gantry_topic = "gantry"
gripper_topic = "gripper"

# Gantry class
class Gantry:
    def __init__(self):
        # Initialize MQTT client
        self.client = mqtt.Client("gantry")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # Connect to MQTT broker
        self.client.connect(broker_address, broker_port, keepalive)
        self.client.loop_start()

        # Gantry state variables
        self.x_pos = 0
        self.y_pos = 0
        self.z_pos = 0

    def on_connect(self, client, userdata, flags, rc):
        # Subscribe to gripper topic
        self.client.subscribe(gripper_topic)
        print("Gantry connected to MQTT broker")

    def on_message(self, client, userdata, msg):
        # Handle messages received on the gripper topic
        if msg.topic == gripper_topic:
            # Process gripper messages
            message = msg.payload.decode("utf-8")
            print("Gantry received message:", message)
            # Handle gripper commands here

    def move_x(self, distance):
        # Code to move the gantry in the X-axis
        # ...
        print("Gantry moving in X-axis by", distance)
        # Publish the new X position
        self.x_pos += distance
        self.client.publish(gantry_topic, f"X:{self.x_pos}")

    def move_y(self, distance):
        # Code to move the gantry in the Y-axis
        # ...
        print("Gantry moving in Y-axis by", distance)
        # Publish the new Y position
        self.y_pos += distance
        self.client.publish(gantry_topic, f"Y:{self.y_pos}")

    def move_z(self, distance):
        # Code to move the gantry in the Z-axis
        # ...
        print("Gantry moving in Z-axis by", distance)
        # Publish the new Z position
        self.z_pos += distance
        self.client.publish(gantry_topic, f"Z:{self.z_pos}")

# Gripper class
class Gripper:
    def __init__(self):
        # Initialize MQTT client
        self.client = mqtt.Client("gripper")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # Connect to MQTT broker
        self.client.connect(broker_address, broker_port, keepalive)
        self.client.loop_start()

        # Gripper state variables
        self.is_gripped = False

    def on_connect(self, client, userdata, flags, rc):
        # Subscribe to gantry topic
        self.client.subscribe(gantry_topic)
        print("Gripper connected to MQTT broker")

    def on_message(self, client, userdata, msg):
        # Handle messages received on the gantry topic
        if msg.topic == gantry_topic:
            # Process gantry messages
            message = msg.payload.decode("utf-8")
            print("Gripper received message:", message)
            # Handle gantry commands here

    def grip(self):
        # Code to activate the gripper
        # ...
        print("Gripper activated")
        # Publish gripper state
        self.client.publish(gripper_topic, "GRIPPED")

    def release(self):
        # Code to release the gripper
        # ...
        print("Gripper released")
        # Publish gripper state
        self.client.publish(gripper_topic, "RELEASED")

# Main code
if __name__ == "__main__":

    
    # Initialize gantry and gripper objects
    gantry = Gantry()
    gripper = Gripper()
    time.sleep(3)
    # Example usage
    gantry.move_x(100)  # Move gantry 100 units in the X-axis
    gripper.grip()  # Activate the gripper
    gantry.move_z(50)  # Move gantry 50 units in the Z-axis
    gripper.release()  # Release the gripper

    # Loop to keep the program running
    while True:
        pass
