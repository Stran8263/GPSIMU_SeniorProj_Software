import pandas as pd
from math import radians, sin, cos, sqrt, atan2

# Define the lat and long of the markers here

#Marker 1
#given_latitude = 35.293816
#given_longitude = -120.645682
#Marker 2
#given_latitude = 35.367953
#given_longitude = -120.865730
#Marker 3
given_latitude = 35.362912
given_longitude = -120.869822

# Function to read the CSV file from a specific row and select specific columns
def read_csv_selective(file_path):
    # Read the CSV file from row 3 onwards and only columns 9 (I), 10 (J), and 12 (L)
    df = pd.read_csv(file_path, skiprows=2, usecols=[8, 9, 11], header=None, names=['Latitude', 'Longitude', 'SIV'])
    return df

# Function to calculate average differences for each unique value of SIV
def calculate_average_differences(df, given_latitude, given_longitude):
    avg_diffs = {}
    for siv_value, siv_group in df.groupby('SIV'):
        # Drop rows where 'Latitude' or 'Longitude' have missing values
        siv_group = siv_group.dropna(subset=['Latitude', 'Longitude'])
        if not siv_group.empty:
            # Convert latitude and longitude back (divide by 10^7)
            siv_group['Latitude'] /= 1e7
            siv_group['Longitude'] /= 1e7

            # Calculate differences
            latitude_diff = siv_group['Latitude'] - given_latitude
            longitude_diff = siv_group['Longitude'] - given_longitude
            # Calculate average differences
            avg_latitude_diff = latitude_diff.mean()
            avg_longitude_diff = longitude_diff.mean()
            avg_diffs[siv_value] = (avg_latitude_diff, avg_longitude_diff)
    return avg_diffs

# Function to calculate the distance between two latitude and longitude pairs
def calculate_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1_rad, lon1_rad, lat2_rad, lon2_rad = map(radians, [lat1, lon1, lat2, lon2])
    # Earth radius in kilometers
    R = 6371.0
    # Calculate differences in latitude and longitude
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    # Calculate distance using Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c * 1000  # Convert distance to meters
    return distance

# Read the CSV file. Change to file name
df = read_csv_selective('data4.csv')

# Select every third row starting from the first row (which corresponds to row 3 in the original file)
df = df.iloc[::3, :]

# Calculate average differences for each unique value of SIV
average_diffs = calculate_average_differences(df, given_latitude, given_longitude)

# Print the results
for siv_value, (avg_latitude_diff, avg_longitude_diff) in average_diffs.items():
    print(f'SIV: {siv_value}, Average Latitude Difference: {avg_latitude_diff}, Average Longitude Difference: {avg_longitude_diff}')


# Calculate distance for each average latitude and longitude difference
average_distances = {}
for siv_value, (avg_latitude_diff, avg_longitude_diff) in average_diffs.items():
    # Convert average latitude and longitude differences to latitude and longitude
    lat = given_latitude + avg_latitude_diff
    lon = given_longitude + avg_longitude_diff
    # Calculate distance
    distance = calculate_distance(given_latitude, given_longitude, lat, lon)
    average_distances[siv_value] = distance

# Find the SIV value with the smallest average distance
min_distance_siv = min(average_distances, key=average_distances.get)
min_distance = average_distances[min_distance_siv]

print(f'Best Data -> SIV: {min_distance_siv}, Minimum Distance: {min_distance} meters')