import requests
import json
import pandas as pd

# API endpoint URL
api_url = "https://data.lacity.org/resource/2nrs-mtv8.json"

# Define parameters for filtering the data (adjust as needed)
params = {
    "$limit": 10000,  # Number of records per request (adjust as needed)
    "$offset": 0,     # Initial offset
    "$order": ":id",  # Order by a unique identifier to ensure consistent ordering
}

# Initialize an empty list to store data
all_data = []

while True:
    # Make a request to the API
    response = requests.get(api_url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse JSON data from the response
        data = response.json()

        # Append the data to the list
        all_data.extend(data)

        # Increment the offset for the next request
        params["$offset"] += len(data)

        # Print progress
        print(f"Downloaded {len(all_data)} records so far.")

        # Check if there is more data to download
        if len(data) < params["$limit"]:
            break
    else:
        # Print an error message and break the loop
        print(f"Error: {response.status_code}")
        break

# Convert the list of dictionaries to a Pandas DataFrame
df = pd.DataFrame(all_data)

# Save the DataFrame to a CSV file
df.to_csv("crime_data_2020_present.csv", index=False)

print("Download complete.")
