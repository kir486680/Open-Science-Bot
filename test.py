import serial
import time

# Replace '/dev/tty.usbmodem5CF0515B37301' with your printer's port
port = '/dev/tty.usbmodem5CF0515B37301'
baud_rate = 115200  # Common baud rate for Ender 3

# Open serial connection
with serial.Serial(port, baud_rate, timeout=2) as ser:
    # Give the printer time to initialize
    time.sleep(2)

    # Example: Send a few commands
    def send_gcode(command):
        ser.write((command + '\n').encode())
        print(f"Sent: {command}")
        wait_for_ok()  # Wait for the printer to confirm completion

    def wait_for_ok():
        while True:
            response = ser.readline().decode().strip()
            if response == "ok":
                print("Move Done")  # Confirmation message
                break
            elif response:
                print("Printer response:", response)

    # Initialize communication
    #send_gcode("M115")  # Firmware info
    #send_gcode("G28")   # Home all axes
    #send_gcode("G1 X50 Y700 Z300 F4000")  # Move to a position
    send_gcode("G1 Z120 F4000")
    send_gcode("G1 X101 F4000")
    send_gcode("G1 Y140 F4000")
    send_gcode("G1 Z48 F4000")

    time.sleep(15)

    #after pick up the part
    send_gcode("G1 Z120 F4000")
    send_gcode("G1 X100 F4000")
    send_gcode("G1 Y83 F4000")
    send_gcode("G1 Z48 F4000")

    #retract the nozzle
    send_gcode("G1 Z120 F4000")

