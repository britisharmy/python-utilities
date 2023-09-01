import concurrent.futures
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
import xml.etree.ElementTree as ET
import os

# Initialize colorama for Windows support
init(autoreset=True)

# Website URL to crawl and create a sitemap for
base_url = "https://example.com/"  # Replace with the website you want to crawl
sitemap_file = "sitemap.xml"  # Output file for the sitemap

# Set to store visited links and links for the sitemap
visited_links = set()
sitemap_links = set()

# Set the user-agent to mimic a Chrome browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def get_links(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = [a['href'] for a in soup.find_all('a', href=True)]
            return links
        else:
            print(f"{Fore.RED}[404] {url}{Style.RESET_ALL}")
    except requests.RequestException as e:
        print(f"{Fore.RED}[Error] {url}: {e}{Style.RESET_ALL}")

def crawl_website(url):
    if url not in visited_links:
        visited_links.add(url)  # Mark the link as visited
        print(f"{Fore.GREEN}[Valid] {url}{Style.RESET_ALL}")
        links = get_links(url)
        if links:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(check_url, links)
        return links

def check_url(url):
    try:
        response = requests.head(url, headers=headers)
        if response.status_code == 200:
            if url not in sitemap_links:
                sitemap_links.add(url)  # Add the link to the sitemap
                print(f"{Fore.GREEN}[Valid] {url}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[404] {url}{Style.RESET_ALL}")
    except requests.RequestException as e:
        print(f"{Fore.RED}[Error] {url}: {e}{Style.RESET_ALL}")

def generate_xml_sitemap(base_url, sitemap_file):
    # Crawl the website and collect links for the sitemap
    crawl_website(base_url)

    # Create a new XML tree for the sitemap with unique links
    root = ET.Element("urlset")
    for url in sitemap_links:
        url_elem = ET.SubElement(root, "url")
        loc = ET.SubElement(url_elem, "loc")
        loc.text = url

    tree = ET.ElementTree(root)
    
    # Save the sitemap
    with open(sitemap_file, "wb") as sitemap:
        sitemap.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        tree.write(sitemap, encoding='utf-8')

if __name__ == "__main__":
    generate_xml_sitemap(base_url, sitemap_file)
