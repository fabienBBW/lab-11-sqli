# lab-11-sqli

 ![password cracking](https://i.postimg.cc/FskzFNmN/Screenshot-2026-05-20-111624.jpg)

## What is this?

Asynchronous password cracker for Lab 11 from the PortSwigger Web Academy SQL Injection module.
(https://portswigger.net/web-security/learning-paths/sql-injection/sql-injection-exploiting-blind-sql-injection-by-triggering-conditional-responses/sql-injection/blind/lab-conditional-responses)  
The vulnerability is a blind SQL Injection with a conditional response.

## How to use?
-- NOTICE: config.json implemented. how to use coming soon. --
1. In the code, change the values for the cookies to your cookie values for your running lab.  
(In the function "getChar")
2. Install required modules:
```shell
python -m pip install -r requirements.txt
```
3. Call the program with python:
```shell
python sqli-lab-11.py <url_of_your_lab_11>
```
