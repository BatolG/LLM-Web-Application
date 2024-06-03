import requests
from bs4 import BeautifulSoup
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('scraped_data.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Create a table in the database
cursor.execute('''
    CREATE TABLE IF NOT EXISTS scraped_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT,
        title TEXT,
        content TEXT
    )
''')

# List of URLs to scrape
urls = [
    'https://u.ae/en/information-and-services/visa-and-emirates-id/residence-visas/golden-visa',
    'https://u.ae/en/information-and-services/visa-and-emirates-id/residence-visas/residence-visa-for-working-in-the-uae',
    'https://u.ae/en/information-and-services/visa-and-emirates-id',
    'https://u.ae/en/information-and-services#/'
]

# Iterate over the URLs
for url in urls:
    # Send a GET request to the website
    response = requests.get(url)

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find specific elements on the webpage
    title = soup.title.text.strip() if soup.title else ''  # Extract the title of the webpage
    paragraphs = soup.find_all('p')  # Extract all <p> tags

    # Print the extracted information
    print('Title:', title)
    print('Paragraphs:')
    for paragraph in paragraphs:
        print(paragraph.text.strip())

    # Extract the relevant information from the soup object
    content = soup.find('div', class_='content').text.strip() if soup.find('div', class_='content') else ''

    # Insert the scraped data into the database
    cursor.execute('''
        INSERT INTO scraped_data (url, title, content)
        VALUES (?, ?, ?)''', (url, title, content))

# Commit the changes to the database
conn.commit()

# Close the database connection
conn.close()