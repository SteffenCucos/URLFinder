import re
import argparse
import requests
from bs4 import BeautifulSoup

def find_urls(input_string):
    # Define the regex pattern
    pattern = r"(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])"
    
    # Find all matches in the input string
    urls = re.findall(pattern, input_string)
    
    # Construct the full URLs from the matches
    full_urls = ["".join(url) for url in urls]
    
    # Sort the URLs alphabetically
    sorted_urls = sorted(full_urls)
    
    return sorted_urls

def fetch_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return ""

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Fetch a webpage and find all URLs in its content.")
    parser.add_argument("url", type=str, help="The URL of the webpage to fetch and search for URLs")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Fetch the page content
    page_content = fetch_page_content(args.url)
    
    if page_content:
        # Create a BeautifulSoup object to parse the HTML
        soup = BeautifulSoup(page_content, "html.parser")
        
        # Extract all text content from the page
        text_content = soup.get_text()
        
        # Find and sort the URLs
        sorted_urls = find_urls(text_content)
        
        # Print the sorted URLs
        for url in sorted_urls:
            print(url)

if __name__ == "__main__":
    main()
