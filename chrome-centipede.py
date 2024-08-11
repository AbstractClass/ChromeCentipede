from websocket import create_connection, WebSocket
from typing import List
import requests
import json

class ChromeInterface:
    def __init__(self, port: int):
        self.port = port
        self.info = self._get_info()
    
    def _get_info(self) -> dict:
        response = requests.get(f'http://localhost:{self.port}/json/list')
        if response.status_code != 200:
            raise Exception(f'[!] Failed to get info from port {self.port}')
        return json.loads(response.text)
    
    @property
    def refresh(self):
        self.info = self._get_info()
    
    @property
    def ws_urls(self) -> List[str]:
        return [item['webSocketDebuggerUrl'] for item in self.info]
    
    def _pages(self, type: str = None) -> List[dict]:
        if type:
            return [item for item in self.info if item['type'] == type]
        else:
            return [item for item in self.info if item['type'] == 'page']
    
    @property
    def pages(self, type: str = None) -> List[dict]:
        return self._pages()
    
    @property
    def tabs(self) -> List[dict]:
        return self._pages('tab')
    
    @property
    def extensions(self) -> List[dict]:
        return self._pages('extension')
    
    def cookie(self, url: str) -> List[dict]:
        ws = create_connection(url)
        ws.send(json.dumps({
            "id": 1,
            "method": "Network.getAllCookies"
        })) # TODO port this to Network.getCookies
        response = ws.recv()
        ws.close()
        print(response)
        return json.loads(response)['result']['cookies']
    
    def cookies(self) -> List[List[dict]]:
        return [self.cookie(url) for url in self.ws_urls]
    
    def inject(self, url: str, script: str) -> str:
        """Doesn't work with MS Edge due to tracking prevention blocking google-analytics, which loads the script""" 
        ws = create_connection(url)
        ws.send(json.dumps({
            "id": 1,
            "method": "Security.disable"
        })) # disable tracking security state changes
        ws.recv()
        ws.send(json.dumps({
            "id": 1,
            "method": "Page.addScriptToEvaluateOnNewDocument",
            "params": {
                "source": script,
                "includeCommandLineAPI": True,
                "runImmediately": True
            }
        })) # inject script
        response = ws.recv()
        ws.close()
        return response
    
    def get_history(self, url: str) -> List[dict]:
        ws = create_connection(url)
        ws.send(json.dumps({
            "id": 1,
            "method": "Page.getNavigationHistory"
        }))
        response = ws.recv()
        ws.close()
        return json.loads(response)['result']['entries']
    
    def screenshot(self, url: str) -> str:
        """Experimental: currently freezes waiting for websocket response"""
        ws = create_connection(url)
        ws.send(json.dumps({
            "id": 1, 
            "method": "Page.captureScreenshot",
            "params": {
                "optimizeForSpeed": True,
                "captureBeyondViewport": True 
            }}))
        response = ws.recv()
        ws.close()
        return response

if __name__ == '__main__':
    # Launch the browser with the following command: $browser_exe --remote-debugging-port=9223 --user-data-dir=$user_data_dir --restore-last-session --allow-remote-origins=*
    # User data dirs: https://chromium.googlesource.com/chromium/src.git/+/HEAD/docs/user_data_dir.md#Default-Location
    chrome = ChromeInterface(9222)
    print("\n### Enumerating pages ###\n")
    for page in chrome.pages:
        print(f"Type: {page['type']}")
        print(f"URL: {page['url']}")
        print(f"Title: {page['title']}")
        print('\n')
    urls = chrome.ws_urls
    print("\n### Enumerating Cookies in 1st Page ###\n")
    for cookie in chrome.cookie(urls[0]):
        for k, v in cookie.items():
            print(f"{k}: {v}")
        print('\n')
    
    print("\n### Injecting alert Into 1st Page ###\n")
    script = 'alert("Injected!")'
    print("Finished with status: ", chrome.inject(urls[0], script))
    #print("\n### Taking a Screenshot of 1st Page ###\n")
    #print(chrome.screenshot(urls[0]))

    print("\n### Getting History of 1st Page ###\n")
    for entry in chrome.get_history(urls[0]):
        for k, v in entry.items():
            print(f"{k}: {v}")
        print('\n')
