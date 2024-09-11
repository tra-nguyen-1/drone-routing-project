import random
from geopy.distance import geodesic

# Define constants for drone operation
MAX_BATTERY_LIFE = 30  # in minutes
MAX_RANGE = 15  # in kilometers
RECHARGE_STATION_LOCATIONS = [(30.000, 115.000), (30.500, 115.500)] 
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
    if distance > MAX_RANGE or battery_life < required_battery:
        return False
    return True

# Find the nearest recharge station
def find_nearest_recharge_station(current_location):
    closest_station = min(RECHARGE_STATION_LOCATIONS, key=lambda x: calculate_distance(current_location, x))
    return closest_station

# Handle the delivery process
def handle_delivery(destination):
    current_location = BASE_LOCATION
    battery_life = MAX_BATTERY_LIFE
    
    # Check weather conditions before starting the journey
    weather = get_current_weather()
    if not check_weather_conditions(weather):
        return_to_base(current_location)
        return

    # Check if the drone can reach the delivery point
    if can_reach_destination(current_location, destination, battery_life):
        print(f"Delivering to {destination} from {current_location}.")
        distance = calculate_distance(current_location, destination)
        battery_life -= (distance / MAX_RANGE) * MAX_BATTERY_LIFE
        print(f"Battery life remaining: {battery_life:.2f} minutes")
    else:
        # Find nearest recharge station if needed
        recharge_station = find_nearest_recharge_station(current_location)
        print(f"Recharging at station {recharge_station}.")
        current_location = recharge_station
        battery_life = MAX_BATTERY_LIFE
        # After recharging, try to deliver again
        if can_reach_destination(current_location, destination, battery_life):
            print(f"Delivering to {destination} from {current_location}.")
            distance = calculate_distance(current_location, destination)
            battery_life -= (distance / MAX_RANGE) * MAX_BATTERY_LIFE
            print(f"Battery life remaining: {battery_life:.2f} minutes")
        else:
            print("Cannot reach destination even after recharging.")

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
