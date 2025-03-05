import requests

def fetch_google_images(query, api_key, cx, num=5):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": api_key,
        "cx": cx,
        "searchType": "image",
        "num": num
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        image_urls = [item['link'] for item in data.get('items', [])]
        return image_urls
    else:
        print(f"Error: {response.status_code}")
        return []

# Replace with your API key and Custom Search Engine ID
api_key = "YOUR_API_KEY"
cx = "YOUR_CUSTOM_SEARCH_ENGINE_ID"

# Search query
query = "cats"
image_urls = fetch_google_images(query, api_key, cx, num=5)

for i, url in enumerate(image_urls):
    print(f"Image {i+1}: {url}")

