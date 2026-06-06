import time

from mitsubishi_rv6s_control import MitsubishiRV6S

robot = MitsubishiRV6S("/dev/ttyUSB0")

try:
    robot.connect()

    robot.set_vacuum(True)

    time.sleep(5)

    robot.set_vacuum(False)

finally:
    robot.close()