# lab-11-sqli

 ![password cracking](https://i.postimg.cc/FskzFNmN/Screenshot-2026-05-20-111624.jpg)

## What is this?

Asynchronous password cracker for Lab 11 from the PortSwigger Web Academy SQL Injection module.
(https://portswigger.net/web-security/learning-paths/sql-injection/sql-injection-exploiting-blind-sql-injection-by-triggering-conditional-responses/sql-injection/blind/lab-conditional-responses)  
The vulnerability is a blind SQL Injection with a conditional response.

## How to use?
1. Install required modules:
```shell
python -m pip install -r requirements.txt
```
2. Add the required values to the config.json at the root level:
- "url": "<url_of_the_lab>",
- "session": "<value_of_session_cookie>",
- "TrackingId": "<value_of_tracking_cookie>",
- "http_proxy": "<address_http_proxy>",
- "https_proxy": "<address_https_proxy>"

For example:  
```json
{
    "url": "https://0aee008b04257a5c80e3ee06002c005a.web-security-academy.net/",
    "session": "fIryKzVpfd4xgBT2ra1c1nUk6pNNG4Ed",
    "TrackingId": "ZzohJeiL3E2qocNS",
    "http_proxy": "http://127.0.0.1:8080",
    "https_proxy": "https://127.0.0.1:8080"
}
```
3. Call the program with python:
```shell
python sqli-lab-11.py
```

## Explanation?
The cookie "TrackingId" will be exploited. We will exploit a blind SQL Injection vulnerability. We can see whether 
we have a hit (character of the password) if the page contains the text "Welcome" (since the SQL query returned "true" then).  
We add our SQL payload at the end of the "TrackingId" cookie. We know from the introduction text to Lab 11 that the password 
is 21 characters long exactly and only contains alphanumeric characters. We brute-force each character using the SQL payload.  
We can only brute-force since we only get a response that either the query worked or did not work; we cannot get text output
from the query. That is why this vulnerability is called a "blind" SQL Injection.
