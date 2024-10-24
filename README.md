# Adobe Portfolio Image Downloader

This project contains a Python script to crawl and download images from an Adobe Portfolio webpage using Selenium. The images are saved into folders named after the last segment of the URL path.

## Requirements

- Python 3.x
- Selenium
- Requests
- Chrome WebDriver

## Setup

1. **Install necessary packages:**

    ```sh
    pip install selenium requests
    ```

2. **Download Chrome WebDriver:**

    Ensure ChromeDriver is installed and available in your system’s PATH. You can download it from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).

## Usage

Run the script with the following command:

```sh
python image_downloader.py <URL> [-o OUTPUT]

```

python image_downloader.py https://example-portfolio.com/gallery -o my_images

- <URL>: The URL of the Adobe Portfolio webpage to crawl.
- [-o OUTPUT]: The output folder for downloaded images (optional, default is downloaded_images).


## Script Overview
Download Image Function: This function downloads an image from a URL and saves it to the specified folder with an incremented name.
Crawl and Download Function: This function uses Selenium to open the webpage, find lightbox elements, and download each image. It organizes the images into a folder named after the last segment of the URL path.

## Important Notes
Ensure you comply with the website’s terms of service and respect their robots.txt rules.
Use this script responsibly to avoid overloading the server with requests.
Issues
If you encounter any issues or have questions, feel free to reach out!
