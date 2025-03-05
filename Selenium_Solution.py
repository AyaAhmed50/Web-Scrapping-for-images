import requests
from bs4 import BeautifulSoup


def get_first_google_image_url(product_name):
    search_url = f"https://www.google.com/search?tbm=isch&q={product_name.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }

    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch search results.")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Find all images and filter those that are from encrypted-tbn0.gstatic.com
    images = soup.find_all("img")
    for img in images:
        img_url = img.get("src")
        if img_url and "https://encrypted-tbn0.gstatic.com/" in img_url:
            print("First Image URL:", img_url)
            return img_url

    print("No relevant image found!")
    return None


# Example usage
get_first_google_image_url("Nike Air Max Shoes")
