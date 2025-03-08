from pyautogui import click
from datetime import datetime
import time
import toml
import os

class EyeTracking:
    def __init__(self):
        """Initialize the EyeTracking with configuration"""
        try:
            # Get the directory where this script is located
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(current_dir, "metadata.toml")
            
            self.config = toml.load(config_path)
            self.delay = self.config["configuration"]["default_delay"]
            self.positions = self.config["positions"]
        except Exception as e:
            print(f"Error loading configuration: {str(e)}")
            raise

    def reset_positions(self):
        """Reset all stored positions to default values and log the old positions"""
        try:
            # Store current positions before resetting
            current_dir = os.path.dirname(os.path.abspath(__file__))
            legacy_file = os.path.join(current_dir, "legacy_positions.txt")
            
            # Get current timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Prepare the log entry for all positions
            log_entry = f"[{timestamp}] Positions reset:\n"
            for pos_name, pos_value in self.positions.items():
                log_entry += f"  {pos_name}: x={pos_value['x']}, y={pos_value['y']}\n"
            
            # Append to legacy file
            with open(legacy_file, "a") as f:
                f.write(log_entry)
            
            # Reset all positions
            for position in self.positions:
                self.positions[position]["x"] = -1
                self.positions[position]["y"] = -1
            
            # Update the positions in config
            self.config["positions"] = self.positions
            
            # Save updated positions to config file
            config_path = os.path.join(current_dir, "metadata.toml")
            with open(config_path, "w") as f:
                toml.dump(self.config, f)
            
            print("All positions have been reset and previous positions logged")
            return True
        except Exception as e:
            print(f"Error during positions reset: {str(e)}")
            return False

    def capture_position(self, position_name: str, x: int, y: int):
        """Set and store a specific position"""
        try:
            if position_name not in self.positions:
                raise ValueError(f"Invalid position name: {position_name}")
                
            self.positions[position_name]["x"] = x
            self.positions[position_name]["y"] = y
            
            # Update the position in config
            self.config["positions"] = self.positions
            
            # Save updated position to config file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(current_dir, "metadata.toml")
            with open(config_path, "w") as f:
                toml.dump(self.config, f)
            
            print(f"Position '{position_name}' captured: ({x}, {y})")
            return True
        except Exception as e:
            print(f"Error during position capture: {str(e)}")
            return False

    def position_capture(self):
        """Stage 1: Capture all necessary positions"""
        try:
            # TODO: Implement position capture workflow
            print("Position capture stage - Not implemented")
            return True
        except Exception as e:
            print(f"Error during position capture stage: {str(e)}")
            return False

    def open_project(self):
        """Stage 2: Open and set up the project"""
        try:
            # TODO: Implement project opening workflow
            print("Open project stage - Not implemented")
            return True
        except Exception as e:
            print(f"Error during project opening stage: {str(e)}")
            return False

    def calibration(self):
        """Stage 3: Perform calibration"""
        try:
            # TODO: Implement calibration workflow
            print("Calibration stage - Not implemented")
            return True
        except Exception as e:
            print(f"Error during calibration stage: {str(e)}")
            return False

    def eyetracking_record(self):
        """Stage 4: Record eye tracking data"""
        try:
            # TODO: Implement recording workflow
            print("Recording stage - Not implemented")
            return True
        except Exception as e:
            print(f"Error during recording stage: {str(e)}")
            return False

    def data_analysis(self):
        """Stage 5: Analyze recorded data"""
        try:
            # TODO: Implement data analysis workflow
            print("Data analysis stage - Not implemented")
            return True
        except Exception as e:
            print(f"Error during data analysis stage: {str(e)}")
            return False

    def execute(self):
        """Execute the complete eyetracking workflow sequence"""
        try:
            # Execute each stage in sequence
            stages = [
                self.position_capture,
                self.open_project,
                self.calibration,
                self.eyetracking_record,
                self.data_analysis
            ]
            
            for stage in stages:
                if not stage():
                    print(f"Workflow failed at {stage.__name__}")
                    return False
                time.sleep(self.delay)
            
            print("Eyetracking workflow completed successfully")
            return True
        except Exception as e:
            print(f"Error during execution: {str(e)}")
            return False
