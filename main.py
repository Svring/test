from pynput import mouse
from operation_object.message_sender.message_sender import MessageSender

def get_mouse_position():
    """Wait for user to click to capture position"""
    print("Move your mouse to the target position and click once...")
    
    position_captured = False
    x, y = 0, 0

    def on_click(cx, cy, button, pressed):
        nonlocal position_captured, x, y

        if button == mouse.Button.left and pressed:
            # Single click detected
            x, y = cx, cy
            position_captured = True
            return False  # Stop listener
    
    # Start mouse listener
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
    
    if position_captured:
        print(f"Position captured: ({x}, {y})")
        return x, y
    return None

def main():
    try:
        # Step 1: Initialize MessageSender
        print("Initializing MessageSender...")
        sender = MessageSender()
        
        # Step 2: Get position from user
        position = get_mouse_position()
        
        if position:
            # Step 3: Configure MessageSender with position
            sender.set_position(position[0], position[1])
            
            # Step 4: Execute workflow
            print("Starting workflow execution...")
            if sender.execute_workflow():
                print("Workflow completed successfully!")
            else:
                print("Workflow failed.")
        else:
            print("No valid position captured.")
            
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
