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
    
    @property
    def pages(self, type: str = None) -> List[dict]:
        if type:
            return [item for item in self.info if item['type'] == type]
        else:
            return [item for item in self.info if item['type'] == 'page']
    
    @property
    def tabs(self) -> List[dict]:
        return self.get_pages('tab')
    
    @property
    def extensions(self) -> List[dict]:
        return self.get_ages('extension')
    
    def cookie(self, url: str) -> dict:
        ws = create_connection(url)
        ws.send('{"id": 1, "method": "Network.getAllCookies"}')
        response = ws.recv()
        ws.close()
        return json.loads(response)
    
    @property
    def cookies(self) -> dict:
        return [self.get_cookies(url) for url in self.get_ws_urls()]

if __name__ == '__main__':
    chrome = ChromeInterface(9223)
    print(chrome.tabs())
    urls = chrome.ws_urls()
    print(chrome.cookies(urls[0]))    
