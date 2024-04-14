import requests

# Replace with your values
API_KEY = "AIzaSyAbrKOP9DhPUwDRcZyY1V0GRJyzspn6dHU"
SEARCH_ENGINE_ID = "86935d125cbb84559"
SEARCH_QUERY = "top 5 profile devops"

url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={SEARCH_QUERY}"

response = requests.get(url)
data = response.json()

# Extract URLs from each search result
urls = []
for item in data["items"]:
  urls.append(item["link"])
  print(item["link"])

# Print the extracted URLs
#print(urls)
