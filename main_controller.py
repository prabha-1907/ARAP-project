import robot

def main():
    red = 0
    green = 0
    blue = 0
    sensor_range = 0.0
    colors_seen = []  # List to track detected colors
    last_color = None  # Variable to keep track of the last detected color
    robot1 = robot.ARAP()
    robot1.init_devices()
    
    while True:
        robot1.reset_actuator_values()
        sensor_range = robot1.get_sensor_input()
        robot1.blink_leds()
        
        # Get color values from the camera image
        red, green, blue = robot1.get_camera_image(5)
        
        # Debugging: Print the RGB values to observe them
        print(f"Red: {red}, Green: {green}, Blue: {blue}")
        
        # Color detection logic
        detected_color = None  # Variable to hold the current detected color
        if red > 80 and green < 70 and blue < 70:  # Threshold for red
            detected_color = "Red"
            print("I see red!")
                             
        elif green > 80 and red < 70 and blue < 70:  # Threshold for green
            detected_color = "Green"
            print("I see green!")
                     
        # Updated threshold for blue based on observed RGB ranges
        elif (9 <= red <= 56) and (9 <= green <= 52) and (98 <= blue <= 127):
            detected_color = "Blue"
            print("I see blue!")
        
        # Only add to colors_seen if detected_color is different from last_color
        if detected_color and detected_color != last_color:
            colors_seen.append(detected_color)  # Append detected color
            last_color = detected_color  # Update last detected color
        elif detected_color:
            print(f"Already counted {detected_color}, skipping duplicate.")

        # Obstacle detection and movement logic
        if robot1.front_obstacles_detected():
            print("Obstacle detected! Moving backward and turning left.")
            robot1.move_backward()
            robot1.turn_left()
            
            # Print the summary of colors seen before hitting the block
            if colors_seen:
                print("Colors encountered before hitting an obstacle:", ', '.join(colors_seen))
            else:
                print("No colors encountered before hitting the obstacle.")
            
            # Reset last_color after hitting an obstacle to allow for new detection
            last_color = None  
        
        else:
            robot1.run_braitenberg()
        
        robot1.set_actuators()
        robot1.step()

if __name__ == "__main__":
    main()
