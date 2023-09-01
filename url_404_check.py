import concurrent.futures
import requests
from colorama import Fore, Style, init

# Initialize colorama for Windows support
init(autoreset=True)

# List of URLs to check
urls = [
    "https://example.com/indonesia/selling-tips/",
    "https://example.com/indonesia/buy-and-sell-quickly/",
    "https://example.com/indonesia/membership/",
    "https://example.com/indonesia/banner-advertising/",
    "https://example.com/indonesia/promote-your-ad/",
    "https://example.com/indonesia/company-contact-info/",
    "https://example.com/indonesia/terms-of-service/",
    "https://example.com/indonesia/privacy-policy/",
    "https://example.com/indonesia/faqs/",
    "https://example.com/indonesia/how-to-stay-safe/",
    "https://example.com/indonesia/terms-conditions/",
]

def check_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"{Fore.GREEN}[Valid] {url}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[404] {url}{Style.RESET_ALL}")
    except requests.RequestException as e:
        print(f"{Fore.RED}[Error] {url}: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    # Use concurrent.futures to check URLs concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(check_url, urls)
