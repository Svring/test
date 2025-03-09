from pyautogui import write, doubleClick
from datetime import datetime
import time
import toml
import os

class MessageSender:
    def __init__(self):
        """Initialize the MessageSender with configuration"""
        try:
            # Get the directory where this script is located
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(current_dir, "metadata.toml")
            
            self.config = toml.load(config_path)
            self.delay = self.config["configuration"]["default_delay"]
            self.position = self.config["positions"]["icon_position"]
        except Exception as e:
            print(f"Error loading configuration: {str(e)}")
            raise

    def reset_position(self):
        """Reset the stored position to default values and log the old position"""
        try:
            # Store current position before resetting
            current_dir = os.path.dirname(os.path.abspath(__file__))
            legacy_file = os.path.join(current_dir, "legacy_position.txt")
            
            # Get current timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Prepare the log entry
            log_entry = f"[{timestamp}] Position reset - x: {self.position['x']}, y: {self.position['y']}\n"
            
            # Append to legacy file
            with open(legacy_file, "a") as f:
                f.write(log_entry)
            
            # Reset position
            self.position["x"] = -1
            self.position["y"] = -1
            
            # Update the position in config
            self.config["positions"]["icon_position"] = self.position
            
            # Save updated position to config file
            config_path = os.path.join(current_dir, "metadata.toml")
            with open(config_path, "w") as f:
                toml.dump(self.config, f)
            
            print("Position has been reset and previous position logged")
            return True
        except Exception as e:
            print(f"Error during position reset: {str(e)}")
            return False

    def capture_position(self, x: int, y: int):
        """Set and store the target position for operations"""
        try:
            self.position["x"] = x
            self.position["y"] = y
            
            # Update the position in config
            self.config["positions"]["icon_position"] = self.position
            
            # Save updated position to config file using the correct path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(current_dir, "metadata.toml")
            with open(config_path, "w") as f:
                toml.dump(self.config, f)
            
            print(f"Position captured: ({x}, {y})")
            return True
        except Exception as e:
            print(f"Error during position capture: {str(e)}")
            return False

    def execute(self):
        """Execute the workflow sequence"""
        try:
            # Validate position
            if self.position["x"] == -1 or self.position["y"] == -1:
                raise ValueError("Position not set. Please capture position first.")

            # Step 1: Move to position and double click
            doubleClick(x=self.position["x"], y=self.position["y"])
            time.sleep(self.delay)
            time.sleep(2)

            # Step 2: Input '1' for random data selection
            write('1\n')
            time.sleep(self.delay)

            # Step 3: Input 's' to start execution
            write('s\n')

            return True
        except Exception as e:
            print(f"Error during execution: {str(e)}")
            return False
            