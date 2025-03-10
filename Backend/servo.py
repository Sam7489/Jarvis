import time
import threading
from pyfirmata import Arduino, SERVO

class ServoController:
    def __init__(self, port, servo_pin):
        self.board = Arduino(port)
        self.pin = servo_pin
        self.board.digital[self.pin].mode = SERVO
        self.running = False
        self.thread = None
    
    def move(self, angle):
        """Move the servo to a specific angle."""
        self.board.digital[self.pin].write(angle)
        time.sleep(0.02)  # Allow time for the servo to move

    def _oscillate(self):
        """Private method to handle to-and-fro motion."""
        while self.running:
            for angle in range(50, 60, 1):  # Move from 90 to 100 degrees
                self.move(angle)
                if not self.running:
                    return
            for angle in range(60, 50, -1):  # Move back to 90 degrees
                self.move(angle)
                if not self.running:
                    return
    
    def start(self):
        """Start oscillating the servo between 90 and 100 degrees."""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._oscillate, daemon=True)
            self.thread.start()
    
    def stop(self):
        """Stop the oscillation."""
        self.running = False
        if self.thread:
            self.thread.join()

# Example usage when imported in another script:
# from servo_control import ServoController
# servo = ServoController('COM3', 9)  # Adjust port and pin as needed
# servo.move(45)
# servo.start()
# time.sleep(5)
# servo.stop()
