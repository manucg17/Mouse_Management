# Import necessary libraries
import pyautogui
import time
import random
import logging
import keyboard
import threading

# Clear the log file at the start
with open('mouse_movement.log', 'w'):
    pass

# Set up logging
logging.basicConfig(filename='mouse_movement.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

# Get screen width and height
screen_width, screen_height = pyautogui.size()
# Define a buffer to avoid edges (optional)
buffer_x = 50  # Adjust as needed
buffer_y = 50  # Adjust as needed

# Define a flag to control the loop
running = False

# Initial direction of movement
direction_x = 1  # 1 means right, -1 means left
direction_y = 1  # 1 means down, -1 means up

# Define the function to move the mouse in a zigzag pattern
def move_mouse_zigzag():
  global direction_x, direction_y

  # Get the current mouse position and screen size
  current_x, current_y = pyautogui.position()

  # Generate random offsets with a slight variation
  offset_x = random.randint(20, 40) * direction_x + random.randint(-5, 5)
  offset_y = random.randint(20, 40) * direction_y + random.randint(-5, 5)

  # Calculate new position considering boundaries defined by (20, 20) and (700, 700)
  new_x = current_x + offset_x
  new_y = current_y + offset_y

  # Clamp the new position within the defined area
  new_x = max(min(new_x, 800 - buffer_x), 20 + buffer_x)  # Clamp x between 20+buffer and 700-buffer
  new_y = max(min(new_y, 800 - buffer_y), 20 + buffer_y)  # Clamp y between 20+buffer and 700-buffer

  # Update direction based on the adjusted new position
  direction_x = (new_x - current_x) / (offset_x if offset_x != 0 else 1)
  direction_y = (new_y - current_y) / (offset_y if offset_y != 0 else 1)

  # Move the mouse relatively with a smaller distance and adjusted speed
  pyautogui.moveRel(direction_x * 2, direction_y * 2, duration=0.2)

  # Log the information (optional)
  logging.info(f'Calculated new position: ({new_x}, {new_y})')


# Function to drag the mouse from point A to point B
def drag_mouse(start_x, start_y, end_x, end_y):
    pyautogui.moveTo(start_x, start_y)
    pyautogui.mouseDown()
    for i in range(1, abs(end_x - start_x) + 1):
        new_x = start_x + (i * (end_x - start_x) / abs(end_x - start_x))
        new_y = start_y + (i * (end_y - start_y) / abs(end_y - start_y))
        # Random variations for a more natural feel
        new_x += random.randint(-2, 2)
        new_y += random.randint(-2, 2)
        pyautogui.moveTo(new_x, new_y, duration=0.07)  # Adjust speed as needed
    time.sleep(random.uniform(0.05, 0.1))  # Pause after drag
    pyautogui.mouseUp()
    logging.info(f'Dragged mouse from ({start_x}, {start_y}) to ({end_x}, {end_y})')


# Function to start the movement
def start_movement():
    global running
    running = True
    logging.info('Started mouse movement')
    while running:
        if not running:  # Check if stopped while waiting
            break
        move_mouse_zigzag()
        sleep_time = random.randint(1, 60)
        # Check for user input to initiate drag during zigzag movement
        if keyboard.is_pressed('ctrl+shift+d'):
            start_x, start_y = pyautogui.position()
            end_x, end_y = get_end_point_from_user()  # Get ending point (separate function)
            drag_mouse(start_x, start_y, end_x, end_y)
        logging.info(f'Next movement in {sleep_time} seconds')
        time.sleep(sleep_time)


# Function to stop the movement
def stop_movement():
    global running
    running = False
    logging.info('Stopped mouse movement')


# Function to get ending point coordinates from user (replace with your desired implementation)
def get_end_point_from_user():
    print("Click to set the ending point for drag.")
    end_x, end_y = pyautogui.position()
    return end_x, end_y


# Function to run the movement in a separate thread
def run_movement():
    movement_thread = threading.Thread(target=start_movement)
    movement_thread.start()


# Function to log exit event
def exit_program():
    logging.info('Exited the program')
    print("Exiting the program.")
    exit()


# Set up keyboard listeners for starting, stopping, and dragging
keyboard.add_hotkey('ctrl+1', run_movement)
keyboard.add_hotkey('ctrl+0', stop_movement)
keyboard.add_hotkey('ctrl+5', exit_program)
keyboard.add_hotkey('ctrl+4', None, suppress=True)  # Listen for drag hotkey without triggering other actions

# Main loop to keep the script running
print("Press 'Ctrl+1' to start and 'Ctrl+0' to stop the mouse movement.")
print("Press 'Ctrl+4' during movement to initiate dragging. Then, click to set the ending point.")
print("Press 'Ctrl+5' to exit the program.")
logging.info("Script started. Waiting for user input.")
keyboard.wait()  # Keep the script running until a hotkey is pressed