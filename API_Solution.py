#Limited with 100 only searches
from serpapi import GoogleSearch

def get_product_image(product_name):
    params = {
        "q": product_name,
        "tbm": "isch",
        "api_key": "your SerpApi key"  # Replace with your SerpApi key
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    images_results = results.get("images_results", [])

    if images_results:
        return images_results[0]["original"]  # Returns the first image URL
    else:
        return "No image found"

# Example Usage
product_name = "GE 30524EE4"
image_url = get_product_image(product_name)
print("Product Image URL:", image_url)
