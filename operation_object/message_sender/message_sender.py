from pyautogui import click, write, doubleClick
import time
from enum import Enum

class MessageSenderState(Enum):
    """States for the MessageSender workflow"""
    IDLE = "idle"
    POSITIONING = "positioning"
    SELECTING = "selecting"
    EXECUTING = "executing"

class MessageSender:
    def __init__(self):
        self.state = MessageSenderState.IDLE
        self.delay = 1
        self.x_position = 0
        self.y_position = 0

    def set_position(self, x: int, y: int):
        """Set the target position for operations"""
        self.state = MessageSenderState.POSITIONING
        self.x_position = x
        self.y_position = y
        return self

    def execute_workflow(self):
        """Execute the complete workflow sequence"""
        try:
            # Step 1: Move to position and double click
            click(x=self.x_position, y=self.y_position)
            doubleClick(x=self.x_position, y=self.y_position)
            time.sleep(self.delay)

            # Step 2: Input '1' for random data selection
            write('1')
            write('\n')  # '\n' simulates Enter key
            time.sleep(self.delay)

            # Step 3: Input 's' to start execution
            write('s')
            write('\n')  # '\n' simulates Enter key
            time.sleep(self.delay)

            self.state = MessageSenderState.IDLE
            return True

        except Exception as e:
            print(f"Error during workflow execution: {str(e)}")
            self.state = MessageSenderState.IDLE
            return False

    def get_state(self) -> MessageSenderState:
        """Get the current state of the MessageSender"""
        return self.state

    def set_delay(self, delay: float):
        """Set the delay between operations"""
        self.delay = delay
        return self
            