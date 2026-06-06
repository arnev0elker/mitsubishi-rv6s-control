import time
import serial

from .exceptions import RobotConnectionError, RobotTimeoutError


class SerialClient:
    def __init__(self, port="/dev/ttyUSB0", baudrate=19200, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None

    def connect(self):
        if self.is_connected():
            return

        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                parity=serial.PARITY_EVEN,
                stopbits=serial.STOPBITS_TWO,
                bytesize=serial.EIGHTBITS,
                timeout=self.timeout,
            )
        except serial.SerialException as exc:
            raise RobotConnectionError(
                f"Could not open serial port {self.port}: {exc}"
            ) from exc

    def close(self):
        if self.ser is not None and self.ser.is_open:
            self.ser.close()

    def is_connected(self):
        return self.ser is not None and self.ser.is_open

    def send(self, command):
        if not self.is_connected():
            raise RobotConnectionError("Robot is not connected.")

        telegram = f"PRN{command}\r"
        self.ser.write(telegram.encode("ascii"))

    def read(self):
        if not self.is_connected():
            raise RobotConnectionError("Robot is not connected.")

        return self.ser.read_until(b"\r").decode("ascii", errors="replace").rstrip()

    def wait_for_response(self, expected=None, timeout=10):
        end_time = time.time() + timeout

        while time.time() <= end_time:
            response = self.read()

            if expected is None:
                if response != "":
                    return response
            else:
                if response in expected:
                    return response

        raise RobotTimeoutError(
            f"No valid response received after {timeout} seconds. "
            f"Expected: {expected}"
        )

    def flush(self):
        if not self.is_connected():
            raise RobotConnectionError("Robot is not connected.")

        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()