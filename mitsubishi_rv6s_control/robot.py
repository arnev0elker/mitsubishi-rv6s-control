import logging
from .serial_client import SerialClient
from .position import list_to_position_string
from .position import position_string_to_list


class MitsubishiRV6S:
    STOP = "1"
    MOVE_JOINT = "2"
    MOVE_LINEAR = "3"
    EMERGENCY_STOP = "4"
    GET_POS_CARTESIAN = "5"
    GET_POS_JOINT = "6"
    SET_TOOL = "8"
    VACUUM_ON = "10"
    VACUUM_OFF = "11"
    BLOWER_ON = "12"
    BLOWER_OFF = "13"

    def __init__(self, port):
        self.client = SerialClient(port=port)

    def set_tool(self, tool=None):
        """
        Set tool coordinates.
        tool format:
        [X, Y, Z, A, B, C] or [X, Y, Z, A, B, C, posture, multi]
        """

        if tool is None:
            tool = [0, 0, 0, 0, 0, 0]

        tool_str = list_to_position_string(tool)

        self.client.send(self.SET_TOOL)
        self.client.wait_for_response(["R"])

        self.client.send(tool_str)
        self.client.wait_for_response(["DONE"])

        logging.info(f"Tool coordinates set to: {tool}")
    
    def connect(self):
        self.client.connect()

    def close(self):
        self.client.close()

    def get_pos(self, joint=False):
        self.client.send(self.GET_POS_JOINT if joint else self.GET_POS_CARTESIAN)
        response = self.client.wait_for_response()
        return position_string_to_list(response)

    def _move(self, pos, speed, command, timeout):
        if speed < 1 or speed > 100:
            raise ValueError("Speed must be between 1 and 100.")

        pos_str = list_to_position_string(pos)

        self.client.send(command)
        self.client.wait_for_response(["R"])

        self.client.send(f"{speed},{pos_str}")
        self.client.wait_for_response(["MOVING"])

        response = self.client.wait_for_response(["DONE", "STOPPING"], timeout)

        logging.info(f"Movement finished: {response}")
        return response

    def moveL(self, pos, speed=30, timeout=3600):
        return self._move(pos, speed, self.MOVE_LINEAR, timeout)

    def moveJ(self, pos, speed=30, timeout=3600):
        return self._move(pos, speed, self.MOVE_JOINT, timeout)

    def _move_async(self, pos, speed, command):
        if speed < 1 or speed > 100:
            raise ValueError("Speed must be between 1 and 100.")

        pos_str = list_to_position_string(pos)

        self.client.send(command)
        self.client.wait_for_response(["R"])

        self.client.send(f"{speed},{pos_str}")
        self.client.wait_for_response(["MOVING"])

        return "MOVING"

    def moveL_async(self, pos, speed=30):
        return self._move_async(pos, speed, self.MOVE_LINEAR)

    def moveJ_async(self, pos, speed=30):
        return self._move_async(pos, speed, self.MOVE_JOINT)

    def stop(self):
        self.client.send(self.STOP)

    def emergency_stop(self):

        self.client.send(self.EMERGENCY_STOP)

    def set_vacuum(self, state):

        if state:
            self.client.send(self.VACUUM_ON)
        else:
            self.client.send(self.VACUUM_OFF)

        self.client.wait_for_response(
            ["DONE"]
        )

    def set_blower(self, state):

        if state:
            self.client.send(self.BLOWER_ON)
        else:
            self.client.send(self.BLOWER_OFF)

        self.client.wait_for_response(
            ["DONE"]
        )