import json
import random
import requests
from requests.exceptions import ProxyError
from concurrent.futures import ThreadPoolExecutor, as_completed

def test_proxy(proxy):
    try:
        print('Testing proxy: ' + proxy)
        # Remove protocol prefix if present
        if '://' in proxy:
            proxy = proxy.split('://')[-1]
            
     
        proxies = {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}'  # Use http:// even for HTTPS connections
        }
        
        proxy_check = "https://sofascore.com"
        test_response = requests.get(
            url=proxy_check,
            proxies=proxies,
            timeout=10,
            verify=False
        )
        
        if test_response.status_code == 200:
            print(f"Proxy {proxy} works")
            return proxy, True
        else:
            print(f"Proxy doesn't work")
            return proxy, False
            
    except requests.exceptions.ProxyError as e:
        print(f"Proxy error: {e}")
        return proxy, False
    except requests.exceptions.ConnectTimeout:
        print(f"Connection timeout")
        return proxy, False
    except requests.exceptions.RequestException as e:
        print(f"Error testing proxy: {e}")
        return proxy, False

def main():
    try:
        proxy_source_url = "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text"
        response = requests.get(url=proxy_source_url)
        proxies = response.content.decode('utf-8').split('\r\n')
        
        # Clean the proxy list
        proxies = [p.strip() for p in proxies if p.strip()]
        
        if not proxies:
            print("No proxies found in the response")
            return
            
        print(f"Found {len(proxies)} proxies")

        working_proxies = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            # Submit all tasks and get futures
            future_to_proxy = {executor.submit(test_proxy, proxy): proxy for proxy in proxies[:20]}
            
           
            for future in as_completed(future_to_proxy):
                proxy, is_working = future.result()
                if is_working:
                    working_proxies.append(proxy)
        
        if working_proxies:
            print(f"\nFound {len(working_proxies)} working proxies:")
            for proxy in working_proxies:
                print(f"- {proxy}")
        else:
            print("\nNo working proxies found")
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching proxy list: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()