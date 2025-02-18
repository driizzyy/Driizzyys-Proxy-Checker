import os
import requests
from threading import Thread
from queue import Queue
import sys
from datetime import datetime
from urllib.parse import urlparse
import time
import sys
import logging

gray = '\033[90m'
pink = '\033[38;2;255;105;180m'
reset = '\033[0m'

pink_gradient = [
    '\033[38;2;255;182;193m',  
    '\033[38;2;255;105;180m',  
    '\033[38;2;255;20;147m',  
    '\033[38;2;219;112;147m', 
]

def display_ascii_art():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.write(fr'''
{pink_gradient[0]}  ____  ____  _  _  ____  ____ ___  ____  _   ____  ____  ____  ____  _____  ____ 
{pink_gradient[1]} /  _ \/  __\/ \/ \/_   \/_   \\  \//\  \//  /  __\/  _ \/  _ \/ ___\/__ __\/ ___\ 
{pink_gradient[2]} | | \||  \/|| || | /   / /   / \  /  \  /   | | //| / \|| / \||    \  / \  |    \
{pink_gradient[3]} | |_/||    /| || |/   /_/   /_ / /   / /    | |_\\| \_/|| \_/|\___ |  | |  \___ | .-'--`-._
{pink_gradient[0]} \____/\_/\_\\_/\_/\____/\____//_/   /_/     \____/\____/\____/\____/  \_/  \____/ '-O---O--'
{reset}
    ''')

def check_proxy(proxy, valid_proxies, invalid_proxies):
    test_url = "http://httpbin.org/ip"
    proxies = {}

    if proxy.startswith("socks5://"):
        proxies = {"http": proxy, "https": proxy}
    elif proxy.startswith("socks4://"):
        proxies = {"http": proxy, "https": proxy}
    elif proxy.startswith("http://") or proxy.startswith("https://"):
        proxies = {"http": proxy, "https": proxy}
    else:
        proxies = {"http": f"http://{proxy}", "https": f"https://{proxy}"}

    try:
        response = requests.get(test_url, proxies=proxies, timeout=3)  
        if response.status_code == 200:
            valid_proxies.append(proxy)
            print(f"{pink}[>]{reset} {gray}Proxy Valid: {proxy}{reset}")
            sys.stdout.flush()  
        else:
            invalid_proxies.append(proxy)
            sys.stdout.flush()  
    except:
        invalid_proxies.append(proxy)
        print(f"{pink}[>]{reset} {gray}Proxy Invalid: {proxy}{reset}")
        sys.stdout.flush()

def main():
    os.system("cls" if os.name == "nt" else "clear") 
    display_ascii_art()

    print(f"\n{pink}[N]{reset} {gray}Checking proxies from data/proxies.txt...{reset}")

    data_folder = "data"
    results_folder_base = "results"

    os.makedirs(data_folder, exist_ok=True)

    input_file = os.path.join(data_folder, "proxies.txt")
    if not os.path.exists(input_file):
        print(f"{pink}[>]{reset}{gray} No input file found in {data_folder}. Please add your proxies to {input_file}.{reset}")
        return

    with open(input_file, 'r') as file:
        proxies = [line.strip() for line in file if line.strip()]

    valid_proxies = []
    invalid_proxies = []

    proxy_queue = Queue()
    for proxy in proxies:
        proxy_queue.put(proxy)

    def worker():
        while not proxy_queue.empty():
            proxy = proxy_queue.get()
            check_proxy(proxy, valid_proxies, invalid_proxies)

    threads = []
    for _ in range(50):  
        thread = Thread(target=worker)
        thread.daemon = True
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    results_folder = os.path.join(results_folder_base, current_datetime)

    os.makedirs(results_folder, exist_ok=True)

    valid_file = os.path.join(results_folder, "valid.txt")
    invalid_file = os.path.join(results_folder, "invalid.txt")

    with open(valid_file, 'w') as file:
        file.writelines([f"{proxy}\n" for proxy in valid_proxies])
    with open(invalid_file, 'w') as file:
        file.writelines([f"{proxy}\n" for proxy in invalid_proxies])

    print(f"{pink}[>]{reset}{gray} Valid proxies saved to {valid_file}.{reset}")
    print(f"{pink}[>]{reset}{gray} Invalid proxies saved to {invalid_file}.{reset}")

    input(f"{pink}[N]{reset} {gray}Press Enter to exit...{reset}")

    os._exit(0)
    os.system("exit")

if __name__ == "__main__":
    main()
