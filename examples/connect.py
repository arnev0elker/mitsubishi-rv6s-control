from mitsubishi_rv6s_control import MitsubishiRV6S

robot = MitsubishiRV6S("/dev/ttyUSB0")

try:
    robot.connect()
    print("Connected")
finally:
    robot.close()