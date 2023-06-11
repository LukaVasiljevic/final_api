import requests
import json

# Specify the URL of the Flask API endpoint
url = 'http://localhost:5000/process-image'

# Prepare the image file
files = [
    ('image', ('image.jpg', open('image.jpg', 'rb'), 'image/jpg'))
]

# Prepare the style file
style = {'style': 'starry.pth',
         'mode' : 1}
style_content = json.dumps(style)
style_file = ('info', ('style.json', style_content, 'application/json'))

# Add the style file to the files list
files.append(style_file)

# Send the POST request with both image and style files
response = requests.post(url, files=files)

# Print the response from the API
print(response.json())
