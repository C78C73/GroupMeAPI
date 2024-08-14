import requests  # Import the requests library to make HTTP requests
import re        # Import the re library to work with regular expressions (for phone number formatting)
import os        # Import the os library to interact with the operating system (e.g., for environment variables)

# Your GroupMe access token (ideally stored as an environment variable for security)
# The access token is used to authenticate your API requests to GroupMe. 
# Here, we're trying to get it from an environment variable named 'GROUPME_ACCESS_TOKEN'.
# If the environment variable is not set, it will use the fallback token provided in the second argument.
ACCESS_TOKEN = os.getenv('GROUPME_ACCESS_TOKEN', 'your access token in here within the quotes')

# The GroupMe group ID where you want to add members
# The GROUP_ID is the unique identifier for the GroupMe group you're managing.
GROUP_ID = 'your group id here inside these quotes'

# Path to the text file containing phone numbers
# This is the file where you have saved all the phone numbers that you want to add to the group.
PHONE_NUMBERS_FILE = 'your txt file with phone numbers inside these quotes'

# Function to normalize phone numbers
# This function takes a phone number as input and formats it into a standard format.
def normalize_phone_number(phone_number):
    # Remove all non-numeric characters except the leading '+'
    # For example, it removes spaces, dashes, and parentheses.
    normalized = re.sub(r'[^\d+]', '', phone_number.strip())
    
    # Add the country code if missing (assuming country code is +1 for US)
    # If the phone number doesn't start with a '+', we assume it's a US number and add the country code '+1'.
    if not normalized.startswith('+'):
        normalized = '+1' + normalized
    
    return normalized

# Function to read phone numbers from a file
# This function reads all the phone numbers from the specified text file and returns them as a list.
def read_phone_numbers_from_file(file_path):
    # Open the file in read mode ('r') and store it in the variable 'file'
    with open(file_path, 'r') as file:
        # Read all lines from the file, strip whitespace, and store them in the 'phone_numbers' list
        phone_numbers = [line.strip() for line in file.readlines()]
    # Return the list of phone numbers
    return phone_numbers

# API endpoint for adding members to a group
# This is the URL where we send the request to add members to the GroupMe group.
# We include the group ID and the access token in the URL.
url = f'https://api.groupme.com/v3/groups/{GROUP_ID}/members/add?token={ACCESS_TOKEN}'

# Function to add members to the group
# This function takes a list of phone numbers and adds them to the GroupMe group.
def add_members_to_group(phone_numbers):
    members = []  # Initialize an empty list to store the members we want to add
    
    for phone_number in phone_numbers:
        # Normalize each phone number using the 'normalize_phone_number' function
        normalized_number = normalize_phone_number(phone_number)
        
        # Create a dictionary for each member with their nickname and phone number
        # The nickname is set to "User <phone_number>" for simplicity.
        member = {
            "nickname": f"User {normalized_number}",
            "phone_number": normalized_number
        }
        
        # Add the member dictionary to the 'members' list
        members.append(member)
    
    # Create the payload (data) for the API request, which contains the list of members
    payload = {
        "members": members
    }

    # Making the API request
    try:
        # Send a POST request to the GroupMe API with the payload (members) as JSON data
        response = requests.post(url, json=payload)
        
        # Check if the request was successful
        # response.raise_for_status() will raise an error if the status code is not 2xx (indicating success)
        response.raise_for_status()

        # If the request was successful, print a success message
        if response.status_code == 202:
            print("Members added successfully!")
        else:
            # If the request was not successful, print the status code and error message
            print(f"Failed to add members: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        # If there was a network error or an error with the request, print the error message
        print(f"An error occurred: {e}")

# Read phone numbers from the file
# This line calls the 'read_phone_numbers_from_file' function to get the list of phone numbers from the file.
phone_numbers = read_phone_numbers_from_file(PHONE_NUMBERS_FILE)

# Add the phone numbers to the group
# This line calls the 'add_members_to_group' function to add the phone numbers to the GroupMe group.
add_members_to_group(phone_numbers)