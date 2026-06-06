Python library for controlling a Mitsubishi RV-6S industrial robot via serial communication.

## Features

* Connect to Mitsubishi RV-6S vi controller
* Read Cartesian robot position
* Read joint positions
* Linear motion (`MOVL`)
* Joint motion (`MOVJ`)
* Set tool coordinates
* Control vacuum gripper
* Control blower
* Stop robot motion
* Emergency stop

## Project Structure

```text
mitsubishi_rv6s_control/

├── __init__.py
├── robot.py
├── serial_client.py
├── position.py
└── exceptions.py
```

## Installation

Clone the repository:

```bash
git clone https://github.com/<username>/mitsubishi-rv6s-control.git
cd mitsubishi-rv6s-control
```

Install dependencies:

```bash
pip install pyserial
```

## Quick Start

```python
from mitsubishi_rv6s_control import MitsubishiRV6S

robot = MitsubishiRV6S("/dev/ttyUSB0")

try:
    robot.connect()

    position = robot.get_pos()

    print(position)

finally:
    robot.close()
```

## Moving the Robot

### Joint Motion

```python
target = [
    42.3,
    -526.45,
    491.19,
    98.76,
    -48.97,
    84.72,
    7,
    0
]

robot.moveJ(target, speed=30)
```

### Linear Motion

```python
target = [
    42.3,
    -526.45,
    491.19,
    98.76,
    -48.97,
    84.72,
    7,
    0
]

robot.moveL(target, speed=30)
```

## Vacuum Control

```python
robot.set_vacuum(True)
robot.set_vacuum(False)
```

## Blower Control

```python
robot.set_blower(True)
robot.set_blower(False)
```

## Tool Definition

```python
robot.set_tool(
    [0, 0, 100, 0, 0, 0]
)
```

## Examples

Example scripts can be found in:

```text
examples/
```

including:

* connect.py
* get_position.py
* move_joint.py
* move_linear.py
* vacuum.py
* set_tool.py

## Supported Hardware

* Mitsubishi RV-6S
* Mitsubishi CRn-500 series robot controller with a custom Formhand robot program for serial command interpretation.
* Serial communication via RS232
