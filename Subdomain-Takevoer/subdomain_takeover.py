import requests
from multiprocessing.dummy import Pool
import os
import argparse
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

errorTexts = [
    "The specified bucket does not exit",
    "Repository not found",
    "ERROR\: The request could not be satisfied",
    "There isn't a GitHub Pages site here.",
    "Sorry\, this shop is currently unavailable\.",
    "Sorry\, We Couldn't Find That Page",
    "Fastly error\: unknown domain\:",
    "The feed has not been found\.",
    "The thing you were looking for is no longer here\, or never was",
    "no-such-app.html|<title>no such app</title>|herokucdn.com/error-pages/no-such-app.html",
    "The gods are wise, but do not know of the site which you seek.",
    "Whatever you were looking for doesn't currently exist at this address.",
    "Do you want to register",
    "Help Center Closed",
    "Oops - We didn't find your site.",
    "We could not find what you're looking for.",
    "No settings were found for this company:",
    "The specified bucket does not exist",
    "<title>404 &mdash; File not found</title>",
    "You are being <a href=\"https://www.statuspage.io\">redirected",
    "This UserVoice subdomain is currently available!",
    "project not found",
    "This page is reserved for artistic dogs\.|Uh oh\. That page doesn't exist</h1>",
    "<p class=\"description\">The page you are looking for doesn't exist or has been moved.</p>",
    "<h1>The page you were looking for doesn't exist.</h1>",
    "You may have mistyped the address or the page may have moved.",
    "<h1>Error 404: Page Not Found</h1>",
    "<h1>https://www.wishpond.com/404?campaign=true",
    "Oops.</h2><p class=\"text-muted text-tight\">The page you're looking for doesn't exist.",
    "There is no portal here \.\.\. sending you back to Aha!",
    "to target URL: <a href=\"https://tictail.com|Start selling on Tictail.",
    "<p class=\"bc-gallery-error-code\">Error Code: 404</p>",
    "<h1>Oops! We couldn&#8217;t find that page.</h1>",
    "alt=\"LIGHTTPD - fly light.\"",
    "Double check the URL or <a href=\"mailto:help@createsend.com",
    "The site you are looking for could not be found.|If you are an Acquia Cloud customer and expect to see your site at this address",
    "If you need immediate assistance, please contact <a href=\"mailto:support@proposify.biz",
    "We can't find this <a href=\"https://simplebooklet.com",
    "With GetResponse Landing Pages, lead generation has never been easier",
    "Looks like you've traveled too far into cyberspace.",
    "is not a registered InCloud YouTrack.",
    "The requested URL / was not found on this server|The requested URL was not found on this server",
    "Domain is not configured",
    "pingdom",
    "Domain has been assigned",
    "data-html-name",
    "Unrecognized domain <strong>",
]
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
}

def findsubdomains(host):
    banner()
    day = datetime.now().day-6
    month = datetime.now().strftime("%m")
    year = datetime.now().year
    
    try:
        url = f'https://subdomainfinder.c99.nl/scans/{year}-{month}-{day}/{host}'
        print(f"Fetching subdomains from: {url}")
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        with open('subdomains.txt', 'w') as subdomains_file:
            for tr in soup.find_all('tr'):
                for aa in tr.find_all('a'):
                    if aa.get_text(strip=True).count('.') == 3 or "none" in str(aa.text):
                        continue
                    subdomains_file.write(f"{aa.get_text(strip=True)}\n")
        
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except requests.exceptions.ConnectionError:
        print("Check your internet connection.")
    except requests.exceptions.Timeout:
        print("The request timed out.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def attack_with_pool(sub):
    try:
        response = requests.get(f"http://{sub}", headers=headers)
        targetresponse = response.text
        for err in errorTexts:
            if err in targetresponse:
                print(f"Potential Vulnerability Detected: {sub}")
                break
        else:
            print(f"Not Found: {sub}")
    except requests.exceptions.RequestException as e:
        # print(f"An error occurred while checking {sub}: {e}")
        pass

def attack(mainurl):
    print("Finding subdomains, please wait...")
    findsubdomains(mainurl)
    with open('subdomains.txt', 'r') as readfile:
        subdomains = readfile.read().strip().split('\n')
    
    print(f"\n{len(subdomains)} subdomains found, saved as subdomains.txt")
    print("Now checking for vulnerabilities...")
    
    pool = Pool(40)
    pool.map(attack_with_pool, subdomains)
    pool.close()
    pool.join()

def banner():
    if os.name in ('ce', 'nt', 'dos'):
        os.system('cls')
    elif 'posix' in os.name:
        os.system('clear')
    
    print("               ####################################### ##############")
    print("               # Tool: Subdomain Takeover Vulnerability Checker    #")
    print("               # Author:  github.com/ArifulProtik                 #")
    print("               # Feel Free To Open A Issue If You Need Any Update  #")
    print("               #####################################################")
    print("\n")

def Main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "hostlink", help="Usage: python subdomain.py example.com", type=str)
    args_ = parser.parse_args()
    attack(args_.hostlink)

if __name__ == "__main__":
    Main()
