import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import requests
import os
import traceback

def download_image(url, folder, name, index):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            filename = f"{name}_{index:03d}.jpg"
            filepath = os.path.join(folder, filename)
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(8192):
                    f.write(chunk)
            print(f"Success: Downloaded image - {filename}")
            return True
        else:
            print(f"Error: Failed to download image from {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error: An exception occurred while downloading image from {url}: {str(e)}")
    return False

def crawl_and_download(url, folder):
    print(f"Starting: Crawling {url}")
    driver = webdriver.Chrome()
    
    # Maximize the window
    driver.maximize_window()

    # Navigate to the URL
    driver.get(url)

    # Wait for the page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "js-lightbox")))
    lightbox_elements = driver.find_elements(By.CLASS_NAME, "js-lightbox")
    print(f"Found {len(lightbox_elements)} lightbox elements")

    os.makedirs(folder, exist_ok=True)

    for index, lightbox in enumerate(lightbox_elements, 1):
        try:
            print(f"Processing image {index}")

            # Click to open the lightbox
            lightbox.click()
            print("Clicked to open lightbox")

            # Wait for the full-resolution image to load in the lightbox
            img_locator = (By.CSS_SELECTOR, "#lightbox-img-wrap img")
            lightbox_img = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(img_locator)
            )
            print("Lightbox image loaded")

            # Get the full-resolution image URL
            img_url = lightbox_img.get_attribute("src")
            print(f"Found image URL for image {index}: {img_url}")

            # Extract name from URL
            name = url.split('/')[-1]

            if download_image(img_url, folder, name, index):
                print(f"Downloaded image with name: {name}_{index:03d}")

            # Hover over the photo before clicking the close button
            actions = ActionChains(driver)
            actions.move_to_element(lightbox_img).perform()  # Hover over the photo

            # Close button interaction
            close_button_xpath = '//*[@id="lightbox-img-wrap"]/div[3]'

            # Click using JavaScript without waiting for visibility
            close_button = driver.find_element(By.XPATH, close_button_xpath)
            driver.execute_script("arguments[0].click();", close_button)
            print(f"Closed lightbox for image {index}")

            # Scroll down
            driver.execute_script("window.scrollBy(0, 100);")  # Scroll down slightly
           
            # Next button interaction without waiting for visibility
            next_button_xpath = '//*[@id="lightbox-img-wrap"]/div[2]'
            
            # Find the next button
            next_button = driver.find_element(By.XPATH, next_button_xpath)
            
            # Scroll into view
            actions.move_to_element(next_button).perform()
            driver.execute_script("arguments[0].scrollIntoView();", next_button)
            
            # Hover over the next button
            actions.move_to_element(next_button).perform()  # Hover over the next button

            # Click using JavaScript if necessary
            driver.execute_script("arguments[0].click();", next_button)
            print(f"Clicked next button for image {index}")

        except Exception as e:
            # Detailed error logging
            print(f"Error processing image {index}: {str(e)}")
            print("Current URL:", driver.current_url)
            print("Element attempted:", close_button_xpath)
            print("Stack Trace:", traceback.format_exc())

    print(f"Completed: Downloaded images from {len(lightbox_elements)} lightbox elements")
    driver.quit()

def main():
    parser = argparse.ArgumentParser(description="Download images from a specified URL.")
    parser.add_argument("url", help="The URL of the webpage to crawl")
    parser.add_argument("-o", "--output", default="downloaded_images", help="Output folder for downloaded images")
    args = parser.parse_args()
    crawl_and_download(args.url, args.output)

if __name__ == "__main__":
    main()

