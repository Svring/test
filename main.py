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
            x, y = cx, cy
            position_captured = True
            return False  # Stop listener
    
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

    if position_captured:
        print(f"Position captured: ({x}, {y})")
        return x, y
    return None

def get_procedure_choice():
    """Get user's choice for which automation procedure to run"""
    print("\nChoose automation procedure:")
    print("1. Message Sender")
    print("2. Eye Tracking")
    while True:
        choice = input("Enter your choice (1 or 2): ").strip()
        if choice in ['1', '2']:
            return choice
        print("Invalid choice. Please enter 1 or 2.")

def get_message_sender_action():
    """Get user's choice for message sender actions"""
    print("\nMessage Sender Options:")
    print("1. Start execution")
    print("2. Reset position")
    while True:
        choice = input("Enter your choice (1 or 2): ").strip()
        if choice in ['1', '2']:
            return choice
        print("Invalid choice. Please enter 1 or 2.")

def run_message_sender():
    """Execute the message sender procedure"""
    try:
        print("Initializing MessageSender...")
        sender = MessageSender()

        # Get user's choice for message sender
        choice = get_message_sender_action()
        
        if choice == '2':
            # Reset position
            if sender.reset_position():
                print("Position has been reset. Please set new position.")
            else:
                print("Failed to reset position")
                return

        # Check if position is already set
        if sender.position["x"] == -1 or sender.position["y"] == -1:
            print("No position set. Please click on the target position...")
            position = get_mouse_position()
            if position:
                if not sender.capture_position(position[0], position[1]):
                    print("Failed to capture position")
                    return
            else:
                print("No valid position captured")
                return
        else:
            print(f"Using existing position: ({sender.position['x']}, {sender.position['y']})")

        # Execute the workflow
        print("Starting workflow execution...")
        if sender.execute():
            print("Workflow completed successfully!")
        else:
            print("Workflow failed.")
    except Exception as e:
        print(f"Error in message sender procedure: {str(e)}")

def run_eye_tracking():
    """Execute the eye tracking procedure"""
    try:
        print("Eye tracking automation is not implemented yet.")
        # TODO: Implement eye tracking automation
    except Exception as e:
        print(f"Error in eye tracking procedure: {str(e)}")

def main():
    try:
        while True:
            # Get user's choice for procedure
            procedure = get_procedure_choice()
            
            # Execute chosen procedure
            if procedure == '1':
                run_message_sender()
            else:
                run_eye_tracking()
            
            # Ask if user wants to continue
            if input("\nDo you want to run another procedure? (y/n): ").lower() != 'y':
                break
            
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
