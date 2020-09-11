# Website Scraper Python Script

## A Python script that scrapes specific content off a web page, saves the content into a database, and creates a JSON file from that data.

---

I wrote this Python script to scrape a website for Nipsey Hussle quotes. After it's done scraping the site it cleans up the data and inserts the quotes into a database. After that it queries for all that data and formats it to JSON, then writes the data to a JSON file. I put it up on here in case someone has a similar use case (for other data). You are more than welcome to clone the repo and tweak the code to fit your needs. The code was done on the fly but can most definitely be optimized, feel free to optimize or format it better and commit any changes to it.

---

### Files

-   `quote_scraper.py`
    -   Script that scrapes the website, extracts the data that is needed, cleans the data, saves the data into a SQLite3 database, formats data as JSON, creates a JSON files and writes that formatted data to it.
-   `quotes.db`
    -   Database file that store the rows of data (quotes in this case)
-   `quotes.json`
    -   JSON file that contains the rows (quotes) from the database in JSON format.

---

### Packages

-   These are the packages that were used, some are already preinstalled.

```python
    import requests
    from bs4 import BeautifulSoup
    import sqlite3
    import re
    import json
```
