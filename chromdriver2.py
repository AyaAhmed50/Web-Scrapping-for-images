from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def fetch_images_selenium(driver, query, num_images=1):
    try:
        # Open Google Images
        driver.get("https://www.google.com/imghp")

        # Find the search box and enter the query
        search_box = driver.find_element(By.NAME, "q")
        search_box.clear()  # Clear the search box in case of previous query
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        # Wait for the images to load
        wait = WebDriverWait(driver, 10)

        # Locate the container for the main image thumbnails
        image_container = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.wIjY0d"))  # Updated selector
        )

        # Find all image thumbnails within the container
        image_thumbnails = image_container.find_elements(By.CSS_SELECTOR, "img.YQ4gaf")  # Updated selector

        # Fetch the first `num_images` images
        image_urls = []
        for i in range(min(num_images, len(image_thumbnails))):  # Ensure we don't exceed available thumbnails
            # Scroll the thumbnail into view (optional, but helps with visibility)
            driver.execute_script("arguments[0].scrollIntoView();", image_thumbnails[i])

            # Click on the thumbnail to open the preview pane
            image_thumbnails[i].click()

            # Wait for the preview pane to load
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.A8mJGd.NDuZHe")))  # Updated selector

            # Locate the full-resolution image in the preview pane
            full_res_image = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "img.sFlh5c.FyHeAf.iPVvYb"))  # Updated selector
            )

            # Get the source URL of the full-resolution image
            img_url = full_res_image.get_attribute("src")

            if img_url and img_url.startswith("http"):  # Ensure it's a valid URL
                image_urls.append(img_url)

            # Close the preview pane (optional, but helps avoid clutter)
            close_button = driver.find_element(By.CSS_SELECTOR, "div.ioQ39e.wv9iH.MjJqGe.cd29Sd")  # Updated selector
            close_button.click()
            time.sleep(1)  # Wait for the preview pane to close

        return image_urls
    except Exception as e:
        # Print the page source for debugging
        print(driver.page_source)
        return f"An error occurred: {e}"

# Main script
if __name__ == "__main__":
    # Set up Chrome options for headless mode
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Disable headless mode for debugging
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    chrome_options.add_argument("--window-size=1920,1080")  # Set window size

    # Install ChromeDriver only once
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # List of queries to process
        queries = ["mountains", "flowers", "beaches"]

        # Fetch 2 images for each query
        for query in queries:
            print(f"Fetching images for query: '{query}'")
            image_urls = fetch_images_selenium(driver, query, num_images=2)
            if isinstance(image_urls, list):  # Check if the result is a list of URLs
                for idx, img_url in enumerate(image_urls, start=1):
                    print(f"Image {idx} URL: {img_url}")
            else:
                print(image_urls)  # Print error message if any
            print("-" * 50)  # Separator for readability
    finally:
        # Close the browser after all queries are processed
        driver.quit()