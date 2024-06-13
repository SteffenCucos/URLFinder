import os
import re
import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse


def find_urls(input_string):
    # Define the regex pattern
    pattern = r"(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])"
    
    # Find all matches in the input string
    urls = re.findall(pattern, input_string)
    # print(urls)
    
    # Construct the full URLs from the matches
    full_urls = [url[0] +"://" + "".join(url[1:]) for url in urls]
    
    # Sort the URLs alphabetically
    sorted_urls = sorted(full_urls)
    
    return sorted_urls

def fetch_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return response.text
    except requests.exceptions.RequestException as e:
        # print(f"Error fetching the URL: {e}")
        return ""

def is_file(url):
    # Define a list of common file extensions
    file_extensions = [
        '.pdf', '.zip', '.rar', '.tar', '.7z', '.doc', '.docx', '.xls', 
        '.xlsx', '.jpg', '.jpeg', '.png', '.gif', '.txt', '.csv', '.mp3', 
        '.mp4', '.avi', '.mkv', '.ppt', '.pptx', '.js'
    ]

    full_url = "".join(url)
    parsed_url = urlparse(full_url)
    cleaned_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', '', ''))
    
    # Extract the file extension from the URL
    _, ext = os.path.splitext(cleaned_url)
    
    # Check if the extracted extension is in the list of file extensions
    return ext.lower() in file_extensions


def find_urls_from_link(url):
    pass


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Fetch a webpage and find all URLs in its content.")
    parser.add_argument("url", type=str, help="The URL of the webpage to fetch and search for URLs")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Fetch the page content
    page_content = fetch_page_content(args.url)

    urls = set()

    file_urls = []
    other_urls = []
    
    if page_content:
        # Create a BeautifulSoup object to parse the HTML
        soup = BeautifulSoup(page_content, "html.parser")
        script_tags = soup.find_all('script', src=True)
        for script in script_tags:
            js_url = script['src']
            script_content = fetch_page_content(js_url)
            page_content += script_content

        # Find and sort the URLs
        sorted_urls = find_urls(page_content)
        
        # Print the sorted URLs
        for url in sorted_urls:
            urls.add(url)

    sorted_urls = sorted(urls)
    for url in sorted_urls:
        if is_file(url):
            file_urls.append(url)
        else:
            other_urls.append(url)

    print("FILE URLS #--------------------------------------#")
    for url in file_urls:
        print("| >", url)
    print("OTHER URLS #--------------------------------------#")
    for url in other_urls:
        print("| >", url)
    print("#--------------------------------------#")
    



if __name__ == "__main__":
    main()
