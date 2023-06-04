import requests

# Specify the URL of the Flask API endpoint
url = 'http://localhost:5000/process-image'

# Open the image file in binary mode
with open('image.jpg', 'rb') as file:
    # Create a dictionary with the file as the 'image' key
    files = {'image': file}

    # Send a POST request to the API endpoint with the image file
    response = requests.post(url, files=files)

# Print the response from the API
print(response.json())
