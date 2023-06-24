import requests
url = "http://localhost:8000/tutorialTrackingApi/1/" +str(200)
data = requests.get(url)
print(data.content)