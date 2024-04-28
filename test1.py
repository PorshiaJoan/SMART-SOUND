import random
from datetime import datetime, timedelta

# Define possible volume levels
volume_levels = [-27, -18, -9, 0, -63]

# Generate 1000 entries
with open('C:\\Users\\Porshia Joan\\OneDrive\\Desktop\\yolov8peoplecounter-main\\data.csv', 'w') as f:
    f.write('Time,Day of Week,Volume\n')  # Header
    
    # Generate entries
    for _ in range(1000):
        # Generate random time within a day
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        
        # Generate random day of the week (1: Monday, 2: Tuesday, ..., 7: Sunday)
        day_of_week = random.randint(1, 7)
        
        # Choose a random volume level
        volume = random.choice(volume_levels)
        
        # Format time
        time_str = f"{hour:02d}:{minute:02d}:{second:02d}"
        
        # Get the day of the week string from the integer representation
        day_of_week_str = (datetime(2024, 1, 1) + timedelta(days=day_of_week-1)).strftime("%A")
        
        # Write to file
        f.write(f'{time_str},{day_of_week_str},{volume}\n')
