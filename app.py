import json
import random
import requests
from requests.exceptions import ProxyError

def testProxy(proxy):
    try:
        print('Testing proxy: ' + proxy)
        
        # Remove protocol prefix if present
        if '://' in proxy:
            proxy = proxy.split('://')[-1]
        
        # Properly format the proxy dict
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
            return True
        else:
            print(f"Proxy doesn't work")
            return False
            
    except requests.exceptions.ProxyError as e:
        print(f"Proxy error: {e}")
        return False
    except requests.exceptions.ConnectTimeout:
        print(f"Connection timeout")
        return False
    except requests.exceptions.RequestException as e:
        print(f"Error testing proxy: {e}")
        return False

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
        
        # Test each proxy
        working_proxies = []
        for proxy in proxies[:20]:  # Test first 5 proxies
            if testProxy(proxy):
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