import requests
from bs4 import BeautifulSoup
import sqlite3
import re
import json

# Database to connect to
db_name="quotes.db"
# Establishing database connection
conn = sqlite3.connect(db_name)
#Initializing Cursor object that will allow us to execute commands
c = conn.cursor() 

#The URL of the site I scraped the quotes from 
URL = 'https://www.awakenthegreatnesswithin.com/35-inspirational-nipsey-hussle-quotes-on-success/'


#Create table to hold the quotes
def create_table():
    try:
        c.execute("CREATE TABLE IF NOT EXISTS quotes (quote TEXT NOT NULL)")
        print("Table has been successfully created.")
    except Exception as e:
        print("There was an error creating the database table: ", (e))

# Scrape the website for the desired content
def scrape_website(website_url):
    try:
        # Make a GET request to the page
        page = requests.get(website_url)
        # Soup object that will parse the content from the page as html
        soup = BeautifulSoup(page.content, 'html.parser')
        # Results is the specific data I want to retrieve from the site (view data prehand with dev tools on Chrome, Firefox, etc.)
        results = soup.find_all('div', class_='td-post-content')

        print("Data successfully extracted!")
    except Exception as e:
        print("There was an error scraping the website: ", (e))

    return results

# Function that handles inserting the quote extracted from the site into the database.s
def insertQuote(quote):
    try:
        c.execute("INSERT INTO quotes VALUES (?)", (quote,)) # insert quote into SQLite DB
        conn.commit() # Commit the changes
        print("Successfully inserted value into DB")
    except Exception as e:
        print("Something went wrong inserting value into the DB: ", (e))

# Function that cleans up the data extracted from the page
# In this case I just wanted the p tag elements and h3 elements (where some quotes were nested inside.)
# Using a bit of regex I was able to 
def tidy_data(results):
    for element in results:
        quotes = element.find_all("p", class_="p2") # The quotes extracted from the <p> elements
        more_quotes = element.find_all("h2", class_="p3") # The nested quotes that were inside the <h3> tags
        all_quotes = quotes[1:] + more_quotes # Concatenate both lists
        for quote in all_quotes:
            raw_quote = quote.text # The quote as extracted from the <p> element
            regex = re.compile('[^a-zA-Z. ]') # Using Regex to only get the characters we want (there were some numbers in there.)
            new_quote = regex.sub('', raw_quote).replace("Nipsey Hussle", " ") # Replace our string with our Regex stripped version then replace a certain string
            insertQuote(new_quote[2:]) # Calling the insertQuote function to insert the quote into the DB.
            
            # If the quote is None then just skip it and continue.
            if None in (quote):
                continue
    print("Successfully cleaned up data and inserted all data into DB.")

# Function that queries for a all the quotes from the DB and converts that data into JSON format
def query_db(query, args=(), one=False):
    c.execute(query, args)
    r = [dict((c.description[i][0], value) for i, value in enumerate(row)) for row in c.fetchall()]
    conn.close()

    return (r[0] if r else None) if one else r

# Function that creates the JSON file and writes the JSON data to it
def create_json_file(query_data):
    try:
        with open("quotes.json", "w") as outfile:
            json.dump(query_data, outfile)
        print("File successfully created and JSON data successfully written to it")
    except Exception as e:
        print("An error occurred while creating/writing JSON data", (e))



# Create the table
create_table()
# Scrape the website
site_data = scrape_website(URL)
# Clean up the data and insert the quotes into the database
tidy_data(site_data)
# Get  all the quotes from the db
my_query = query_db("SELECT * FROM quotes")
# Create a JSON file and write the our quotes data to it
create_json_file(my_query)