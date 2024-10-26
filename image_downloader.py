import argparse
import os
import traceback
import subprocess
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

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

def setup_webdriver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver

def open_folder_in_finder(folder):
    subprocess.call(["open", folder])

def get_lightbox_elements(driver, url):
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "js-lightbox")))
    return driver.find_elements(By.CLASS_NAME, "js-lightbox")

def process_image(driver, lightbox, folder, url, index):
    try:
        close_button_xpath = '//*[@id="lightbox-img-wrap"]/div[3]'
        next_button_xpath = '//*[@id="lightbox-img-wrap"]/div[2]'
        
        print(f"Processing image {index}")
        lightbox.click()
        print("Clicked to open lightbox")

        img_locator = (By.CSS_SELECTOR, "#lightbox-img-wrap img")
        lightbox_img = WebDriverWait(driver, 30).until(EC.presence_of_element_located(img_locator))
        print("Lightbox image loaded")

        img_url = lightbox_img.get_attribute("src")
        print(f"Found image URL for image {index}: {img_url}")

        name = url.split('/')[-1]
        if download_image(img_url, folder, name, index):
            print(f"Downloaded image with name: {name}_{index:03d}")

        actions = ActionChains(driver)
        actions.move_to_element(lightbox_img).perform()

        close_button = driver.find_element(By.XPATH, close_button_xpath)
        driver.execute_script("arguments[0].scrollIntoView();", close_button)
        driver.execute_script("arguments[0].click();", close_button)
        print(f"Closed lightbox for image {index}")

        driver.execute_script("window.scrollBy(0, 100);")

        next_button = driver.find_element(By.XPATH, next_button_xpath)
        actions.move_to_element(next_button).perform()
        driver.execute_script("arguments[0].scrollIntoView();", next_button)
        actions.move_to_element(next_button).perform()
        driver.execute_script("arguments[0].click();", next_button)
        print(f"Clicked next button for image {index}")
    except Exception as e:
        print(f"Error processing image {index}: {str(e)}")
        print("Current URL:", driver.current_url)
        print("Element attempted:", close_button_xpath)
        print("Stack Trace:", traceback.format_exc())

def crawl_and_download(url, folder):
    print(f"Starting: Crawling {url}")
    driver = setup_webdriver()
    lightbox_elements = get_lightbox_elements(driver, url)
    print(f"Found {len(lightbox_elements)} lightbox elements")

    if not os.path.exists(folder):
        print(f"Creating folder: {folder}")
        os.makedirs(folder, exist_ok=True)
    
    open_folder_in_finder(folder)
    print(f"Downloading images from {len(lightbox_elements)} lightbox elements")

    for index, lightbox in enumerate(lightbox_elements, 1):
        process_image(driver, lightbox, folder, url, index)

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

