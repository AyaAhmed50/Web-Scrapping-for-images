from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def fetch_first_image_selenium(query):
    # Automatically install the correct ChromeDriver version
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        # Open Google Images
        driver.get("https://www.google.com/imghp")

        # Find the search box and enter the query
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        # Wait for the images to load
        wait = WebDriverWait(driver, 10)

        # Locate the container for the main image thumbnails
        image_container = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.wIjY0d.jFk0f"))
        )

        # Locate the first image thumbnail within the container
        first_image_thumbnail = image_container.find_element(By.CSS_SELECTOR, "img.YQ4gaf")
        first_image_thumbnail.click()  # Click on the thumbnail to open the preview pane

        # Wait for the preview pane to load
        time.sleep(2)

        # Locate the full-resolution image in the preview pane
        full_res_image = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "img.sFlh5c.FyHeAf.iPVvYb"))
        )

        # Get the source URL of the full-resolution image
        img_url = full_res_image.get_attribute("src")

        if img_url and img_url.startswith("http"):  # Ensure it's a valid URL
            return img_url
        else:
            return "No valid image URL found."
    except Exception as e:
        return f"An error occurred: {e}"
    finally:
        # Close the browser
        driver.quit()

# Example usage
query = "mountains"
first_image_url = fetch_first_image_selenium(query)
print("First image URL:", first_image_url)