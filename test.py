from mindstorms import Motor, Hub
import time
import asyncio

hub = Hub()
time.sleep(1)

motor = hub.port.E.motor
motor.run_for_degrees(1110)
#Hello world will be =executed before the motor is done. To prevent this, we can define async functions and await them.

async def move_motor():
    await motor.run_for_degrees(1110)

asyncio.run(move_motor())

print("Hello World")