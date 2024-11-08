import random
from geopy.distance import geodesic

# Define constants for drone operation
MAX_BATTERY_LIFE = 30  # in minutes
MAX_RANGE = 15  # in kilometers
RECHARGE_STATION_LOCATIONS = [
    (40.000, 115.000), 
    (40.500, 115.500), 
    (39.800, 114.800),  # New recharge station
    (41.000, 115.200)   # New recharge station
]
BASE_LOCATION = (30.000, 115.000)  # Base coordinates
WEATHER_CONDITIONS = ["Clear", "Windy", "Rainy", "Stormy"]

# Simulate getting the current weather condition 
def get_current_weather():
    return random.choice(WEATHER_CONDITIONS)

# Check if the drone can proceed under the current weather condition
def check_weather_conditions(weather):
    if weather in ["Windy", "Stormy"]:
        print(f"Adverse weather detected: {weather}. Drone will return to base.")
        return False  # Not safe to fly
    return True

# Calculate distance between two coordinates
def calculate_distance(point1, point2):
    return geodesic(point1, point2).km

# Determine if the drone can reach the destination based on battery life
def can_reach_destination(current_location, destination, battery_life):
    distance = calculate_distance(current_location, destination)
    required_battery = (distance / MAX_RANGE) * MAX_BATTERY_LIFE
    
    if battery_life < required_battery:
        print(f"Not enough battery to reach destination. Battery required: {required_battery:.2f} minutes, Battery remaining: {battery_life:.2f} minutes.")
        return False
    return True

# Find the nearest recharge station using a greedy approach
def find_nearest_recharge_station(current_location):
    closest_station = min(RECHARGE_STATION_LOCATIONS, key=lambda x: calculate_distance(current_location, x))
    print(f"Nearest recharge station is at {closest_station}.")
    return closest_station

# Simulate checking signal strength
def check_signal():
    return random.randint(0, 100)  # Signal strength as a percentage (0-100)

# Handle signal coverage issues
def handle_signal_coverage(signal_strength, current_location):
    if signal_strength < 20:  # If signal is weak, drone needs to return to the last known point
        print(f"Low signal detected: {signal_strength}%. Returning to last known point.")
        return_to_base(current_location)
        return False  # Stop the journey due to signal loss
    return True

# Avoid obstacle logic
def avoid_obstacle(current_location, obstacle_location, obstacle_size):
    # Simple avoidance logic: move east by the size of the obstacle (in km)
    adjusted_location = (current_location[0], current_location[1] + obstacle_size)
    print(f"Obstacle detected at {obstacle_location} with size {obstacle_size} km. Adjusting route to {adjusted_location}.")
    return adjusted_location

# Handle the delivery process
def handle_delivery(destination):
    current_location = BASE_LOCATION
    battery_life = MAX_BATTERY_LIFE
    max_recharge_attempts = 2  # Allow up to 2 recharges to reach the destination
    recharge_attempts = 0
    
    # Check weather conditions before starting the journey
    weather = get_current_weather()
    if not check_weather_conditions(weather):
        return_to_base(current_location)
        return

    # Check signal strength before starting the journey
    signal_strength = check_signal()
    if not handle_signal_coverage(signal_strength, current_location):
        return

    # Get obstacle input from user
    obstacle_input = input("Is there an obstacle? (yes/no): ").strip().lower()
    obstacle_location = None
    obstacle_size = 0

    if obstacle_input == 'yes':
        obstacle_lat = float(input("Enter the latitude of the obstacle: "))
        obstacle_lon = float(input("Enter the longitude of the obstacle: "))
        obstacle_size = float(input("Enter the size of the obstacle (in km): "))
        obstacle_location = (obstacle_lat, obstacle_lon)

    # Loop to allow multiple recharges if necessary
    while True:
        if can_reach_destination(current_location, destination, battery_life):
            if obstacle_location:
                current_location = avoid_obstacle(current_location, obstacle_location, obstacle_size)

            print(f"Delivering to {destination} from {current_location}.")
            distance = calculate_distance(current_location, destination)
            battery_life -= (distance / MAX_RANGE) * MAX_BATTERY_LIFE
            print(f"Battery life remaining: {battery_life:.2f} minutes")
            break  # Successfully delivered, exit loop
        else:
            if recharge_attempts < max_recharge_attempts:
                # Find nearest recharge station using greedy choice
                recharge_station = find_nearest_recharge_station(current_location)
                print(f"Recharging at station {recharge_station}.")
                current_location = recharge_station
                battery_life = MAX_BATTERY_LIFE
                recharge_attempts += 1

                # After recharging, check signal strength again
                signal_strength = check_signal()
                if not handle_signal_coverage(signal_strength, current_location):
                    return
            else:
                print("Maximum recharge attempts reached. Cannot reach destination.")
                break

    # Return to base after delivery
    return_to_base(current_location)

def return_to_base(current_location):
    # Navigate back to base
    print(f"Returning to base from {current_location}.")
    distance = calculate_distance(current_location, BASE_LOCATION)
    if distance <= MAX_RANGE:
        print(f"Successfully returned to base at {BASE_LOCATION}.")
    else:
        print("Warning: Insufficient battery to return to base. Emergency landing required.")

# Execute the route planning
def main():
    print("Starting drone delivery route planning...")
    
    # Get delivery location from user
    try:
        lat = float(input("Enter the latitude of the delivery location: "))
        lon = float(input("Enter the longitude of the delivery location: "))
        delivery_location = (lat, lon)
        
        # Handle the delivery
        handle_delivery(delivery_location)
    except ValueError:
        print("Invalid input. Please enter valid numerical values for latitude and longitude.")

if __name__ == "__main__":
    main()
