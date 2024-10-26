# Adobe Portfolio Image Downloader

This Python script allows you to crawl and download images from multiple URLs of Adobe Portfolio pages using Selenium and Requests. The images are saved into custom folders, or the default folder names based on the URL.

## Features

- Download images from multiple URLs.
- Save images into custom or default folders.
- Automatically open the download folder in Finder (macOS).
- Detailed error logging for easier troubleshooting.

## Requirements

- Python 3.x
- Selenium
- Requests
- Chrome WebDriver

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/adobe-portfolio-image-downloader.git
    cd adobe-portfolio-image-downloader
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```sh
    pip install selenium requests
    ```

4. **Download and setup Chrome WebDriver**:
    - Make sure `chromedriver` is installed and available in your system PATH.
    - You can download it from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).

## Usage

1. **Run the script**:
    ```sh
    python3 image_downloader.py
    ```

2. **Input the URLs and custom folder names**:
    - Enter the URLs to crawl, separated by commas.
    - Enter custom folder names separated by commas. If you do not provide a custom name, the default will be the last segment of the URL.

## Example

```sh
Enter the URLs to crawl, separated by commas: https://example1.adobe.com/portfolio, https://example2.adobe.com/gallery
Enter custom folder names separated by commas (press Enter to use URL's name after last slash): portfolio_images, gallery_images

