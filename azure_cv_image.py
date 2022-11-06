import requests
# If you are using a Jupyter Notebook, uncomment the following line.
# %matplotlib inline
import matplotlib.pyplot as plt
import json
from PIL import Image
from io import BytesIO
import os

# Add your Computer Vision subscription key and endpoint to your environment variables.
subscription_key = 'ee60559e9bda4bd3b523f09ed23b0e5d'
endpoint = 'https://cvfortest.cognitiveservices.azure.com/'
analyze_url = endpoint + "vision/v3.1/analyze"

# Set image_url to the URL of an image that you want to analyze.
#image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/" + \
#    "Broadway_and_Times_Square_by_night.jpg/450px-Broadway_and_Times_Square_by_night.jpg"

image_url = "C:\Documents\Photo\P_20191228_083744_vHDR_On.jpg"

headers = {'Ocp-Apim-Subscription-Key': subscription_key}
params = {'visualFeatures': 'Categories,Description,Color'}
data = {'url': image_url}
response = requests.post(analyze_url, headers=headers,
                         params=params, json=data)
response.raise_for_status()

# The 'analysis' object contains various fields that describe the image. The most
# relevant caption for the image is obtained from the 'description' property.
analysis = response.json()
print(json.dumps(response.json()))
image_caption = analysis["description"]["captions"][0]["text"].capitalize()

# Display the image and overlay it with the caption.
image = Image.open(BytesIO(requests.get(image_url).content))
plt.imshow(image)
plt.axis("off")
_ = plt.title(image_caption, size="x-large", y=-0.1)
plt.show()
