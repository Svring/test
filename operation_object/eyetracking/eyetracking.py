from pyautogui import click, doubleClick
from datetime import datetime
import time
import toml
import os
from pynput import mouse, keyboard
from pynput.keyboard import Key, KeyCode

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

    def get_mouse_position(self):
        """Wait for backtick key press to capture current mouse position"""
        print("Move your mouse to the target position and press ` (backtick) key to capture...")
        
        position_captured = False
        x, y = 0, 0
        mouse_controller = mouse.Controller()

        def on_press(key):
            nonlocal position_captured, x, y
            try:
                if key.char == '`':
                    # Get current mouse position
                    x, y = mouse_controller.position
                    position_captured = True
                    return False  # Stop listener
            except AttributeError:
                pass  # Ignore special keys

        # Listen for backtick key press
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
        
        if position_captured:
            print(f"Position captured: ({x}, {y})")
            return x, y
        return None

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

    def position_calibration(self):
        """Stage 0: Capture all necessary positions"""
        try:
            print("\nStarting position calibration...")
            print("You will need to set positions for all interface elements.")
            
            # Iterate through all positions in the config
            for position_name in self.positions.keys():
                while True:
                    # Format position name for display (convert from snake_case to Title Case)
                    display_name = position_name.replace('_', ' ').title()
                    print(f"\nPlease set position for: {display_name}")
                    
                    # Get position from user
                    position = self.get_mouse_position()
                    if position:
                        x, y = position
                        if self.capture_position(position_name, x, y):
                            break  # Successfully captured position
                    
                    # If position capture failed or was interrupted
                    retry = input("Failed to capture position. Retry? (y/n): ").lower()
                    if retry != 'y':
                        print(f"Skipping {display_name}...")
                        break
            
            print("\nPosition calibration completed!")
            return True
            
        except Exception as e:
            print(f"Error during position calibration: {str(e)}")
            return False
        
    def open_eyetracker(self):
        """Stage 1: Open the eyetracker"""
        try:
            # Get the position
            pos = self.positions["open_eyetracker_position"]
            
            # Validate position
            if pos["x"] == -1 or pos["y"] == -1:
                raise ValueError("Eyetracker position not set. Please calibrate positions first.")

            # Double click at the position
            print("Opening eyetracker application...")
            doubleClick(x=pos["x"], y=pos["y"])
            time.sleep(self.delay)  # Wait for application to open
            time.sleep(7)

            print("Eyetracker application opened")
            return True
        except Exception as e:  
            print(f"Error during eyetracker opening stage: {str(e)}")
            return False

    def open_project(self):
        """Stage 2: Open and set up the project"""
        try:
            # Get all required positions
            project_pos = self.positions["open_project_position"]
            record_pos = self.positions["test_record_position"]
            save_pos = self.positions["save_button_position"]
            
            # Validate all positions
            for name, pos in [("Project button", project_pos), 
                            ("Test record", record_pos),
                            ("Save button", save_pos)]:
                if pos["x"] == -1 or pos["y"] == -1:
                    raise ValueError(f"{name} position not set. Please calibrate positions first.")

            # Click project button
            print("Opening project dialog...")
            click(x=project_pos["x"], y=project_pos["y"])
            time.sleep(self.delay)

            # Click test record
            print("Selecting test record...")
            click(x=record_pos["x"], y=record_pos["y"])
            time.sleep(self.delay)

            # Click save button
            print("Saving selection...")
            click(x=save_pos["x"], y=save_pos["y"])
            time.sleep(self.delay)

            print("Project setup completed")
            return True
        except Exception as e:
            print(f"Error during project opening stage: {str(e)}")
            return False

    def calibration(self):
        """Stage 3: Perform calibration"""
        try:
            # Get all required positions
            test_select_pos = self.positions["test_select_position"]
            calibrate_pos = self.positions["calibrate_position"]
            confirm_pos = self.positions["calibrate_confirm_position"]
            
            # Validate all positions
            for name, pos in [("Test select", test_select_pos), 
                            ("Calibrate", calibrate_pos),
                            ("Calibrate confirm", confirm_pos)]:
                if pos["x"] == -1 or pos["y"] == -1:
                    raise ValueError(f"{name} position not set. Please calibrate positions first.")

            # Click test select button
            print("Selecting test...")
            click(x=test_select_pos["x"], y=test_select_pos["y"])
            time.sleep(self.delay)

            # Click calibrate button
            print("Starting calibration...")
            click(x=calibrate_pos["x"], y=calibrate_pos["y"])
            time.sleep(self.delay)

            print("Calibration initiated")

            # Wait for calibration to complete
            print("Waiting for calibration process (30 seconds)...")
            time.sleep(30)

            # Click confirm button
            print("Confirming calibration...")
            click(x=confirm_pos["x"], y=confirm_pos["y"])
            time.sleep(self.delay)

            print("Calibration completed and confirmed")
            return True
        except Exception as e:
            print(f"Error during calibration stage: {str(e)}")
            return False

    def eyetracking_record(self):
        """Stage 4: Record eye tracking data"""
        try:
            # Get all required positions
            start_pos = self.positions["start_record_position"]
            confirm_pos = self.positions["record_confirm_position"]
            
            # Validate all positions
            for name, pos in [("Start record", start_pos), 
                            ("Record confirm", confirm_pos)]:
                if pos["x"] == -1 or pos["y"] == -1:
                    raise ValueError(f"{name} position not set. Please calibrate positions first.")

            # Click start record button
            print("Starting recording...")
            click(x=start_pos["x"], y=start_pos["y"])
            time.sleep(self.delay)

            # Wait for recording duration
            print("Recording in progress (20 seconds)...")
            time.sleep(20)

            # Click confirm button
            print("Confirming recording...")
            click(x=confirm_pos["x"], y=confirm_pos["y"])
            time.sleep(self.delay)

            print("Recording completed and confirmed")
            return True
        except Exception as e:
            print(f"Error during recording stage: {str(e)}")
            return False

    def data_analysis(self):
        """Stage 5: Analyze recorded data"""
        try:
            # Get all required positions
            positions = {
                "Data Analysis": self.positions["data_analysis_position"],
                "Interest Area": self.positions["interest_area_position"],
                "Stimulus Material": self.positions["stimulus_material0_position"],
                "Square Area Create": self.positions["square_area_create_position"],
                "Area Delete": self.positions["area0_delete_position"],
                "Index Area": self.positions["index_area_position"],
                "AOI Based Output Section": self.positions["aoi_based_output_section_position"],
                "AOI Based Output Export": self.positions["aoi_based_output_export_position"],
                "Export Confirm": self.positions["aoi_based_output_export_confirm_position"],
                "Data Visualization": self.positions["data_visualization_position"]
            }
            
            # Validate all positions
            for name, pos in positions.items():
                if pos["x"] == -1 or pos["y"] == -1:
                    raise ValueError(f"{name} position not set. Please calibrate positions first.")

            # Initial move to data analysis position
            print("Moving to data analysis section...")
            click(x=positions["Data Analysis"]["x"], y=positions["Data Analysis"]["y"])
            time.sleep(self.delay)

            # Interest area creation and deletion sequence
            print("Configuring interest areas...")
            click(x=positions["Interest Area"]["x"], y=positions["Interest Area"]["y"])
            time.sleep(self.delay)
            
            click(x=positions["Stimulus Material"]["x"], y=positions["Stimulus Material"]["y"])
            time.sleep(self.delay)
            
            click(x=positions["Square Area Create"]["x"], y=positions["Square Area Create"]["y"])
            time.sleep(self.delay)
            
            print("Waiting for area creation (2 seconds)...")
            time.sleep(self.delay)
            
            click(x=positions["Area Delete"]["x"], y=positions["Area Delete"]["y"])
            time.sleep(self.delay)

            # Return to data analysis and proceed with AOI based output
            print("Configuring AOI based output...")
            click(x=positions["Data Analysis"]["x"], y=positions["Data Analysis"]["y"])
            time.sleep(self.delay)
            
            click(x=positions["Index Area"]["x"], y=positions["Index Area"]["y"])
            time.sleep(self.delay)
            
            click(x=positions["AOI Based Output Section"]["x"], y=positions["AOI Based Output Section"]["y"])
            time.sleep(self.delay)
            
            click(x=positions["AOI Based Output Export"]["x"], y=positions["AOI Based Output Export"]["y"])
            time.sleep(self.delay)
            
            click(x=positions["Export Confirm"]["x"], y=positions["Export Confirm"]["y"])
            time.sleep(self.delay)

            # Final visualization sequence
            print("Opening data visualization...")
            click(x=positions["Data Analysis"]["x"], y=positions["Data Analysis"]["y"])
            time.sleep(self.delay)
            
            click(x=positions["Data Visualization"]["x"], y=positions["Data Visualization"]["y"])
            time.sleep(self.delay)

            print("Data analysis workflow completed")
            return True
        except Exception as e:
            print(f"Error during data analysis stage: {str(e)}")
            return False

    def execute(self):
        """Execute the complete eyetracking workflow sequence"""
        try:
            # Execute each stage in sequence
            stages = [
                self.open_eyetracker,
                self.open_project,
                self.calibration,
                self.eyetracking_record,
                self.data_analysis
            ]
            
            print("\nStarting eyetracking workflow execution...")
            for stage in stages:
                print(f"\nExecuting {stage.__name__} stage...")
                if not stage():
                    print(f"Workflow failed at {stage.__name__}")
                    return False
                time.sleep(self.delay)
            
            print("\nEyetracking workflow completed successfully")
            return True
        except Exception as e:
            print(f"Error during execution: {str(e)}")
            return False
