import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, urljoin
import os
import threading
import concurrent.futures

# Initialize colorama for Windows support
init(autoreset=True)

# Website URL to crawl and create a sitemap for
base_url = "https://example.com/"  # Replace with the website you want to crawl
sitemap_file = "sitemap.xml"  # Output file for the sitemap

# Set to store visited links and links for the sitemap
visited_links = set()
sitemap_links = set()
unique_links = set()  # Maintain a set for unique links

# Create locks for synchronization
visited_links_lock = threading.Lock()
sitemap_links_lock = threading.Lock()

# Condition variable for signaling when the sitemap is ready to be written
sitemap_ready_condition = threading.Condition()

# Counter to keep track of processed links
processed_links_count = 0

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
    except requests.RequestException as e:
        pass  # Handle the exception as needed

def crawl_website(url, max_depth):
    global processed_links_count  # Use the global counter
    if url not in visited_links and urlparse(url).netloc == urlparse(base_url).netloc:
        with visited_links_lock:
            visited_links.add(url)  # Mark the link as visited
        print(f"{Fore.GREEN}[Valid] {url}{Style.RESET_ALL}")
        links = get_links(url)
        if links and max_depth > 0:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(crawl_website, urljoin(base_url, link), max_depth - 1) for link in links]
                for future in concurrent.futures.as_completed(futures):
                    pass  # Wait for all threads to finish
        with sitemap_links_lock:
            if url not in unique_links:
                sitemap_links.add(url)  # Add the link to the sitemap
                unique_links.add(url)  # Add the link to the unique_links set
            processed_links_count += 1  # Increment the counter
            if processed_links_count == len(visited_links):  # Check if all links are processed
                with sitemap_ready_condition:  # Acquire the condition here
                    sitemap_ready_condition.notify()  # Notify that the sitemap is ready

def write_sitemap(sitemap_file):  # Accept sitemap_file as an argument
    with sitemap_ready_condition:
        sitemap_ready_condition.wait()  # Wait until the sitemap is ready
    # Create a new XML tree for the sitemap with unique links
    root = ET.Element("urlset")
    for url in sitemap_links:
        url_elem = ET.SubElement(root, "url")
        loc = ET.SubElement(url_elem, "loc")
        loc.text = url

    # Convert the XML tree to a string
    xml_string = ET.tostring(root, encoding="utf-8").decode("utf-8")

    # Save the sitemap using a single thread to write to the file
    with open(sitemap_file, "w", encoding="utf-8") as sitemap_file:
        sitemap_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        sitemap_file.write(xml_string)

if __name__ == "__main__":
    # Start the sitemap writing thread and pass sitemap_file as an argument
    sitemap_writer_thread = threading.Thread(target=write_sitemap, args=(sitemap_file,))
    sitemap_writer_thread.start()

    # Crawl the website and collect links for the sitemap (max_depth=3 in this example)
    crawl_website(base_url, max_depth=3)

    # Wait for the sitemap writer thread to finish
    sitemap_writer_thread.join()
