#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import pandas as pd
from plyer import notification


def fetch_book_details(isbn):
    url = f"https://www.booktopia.com.au/book/{isbn}.html"
    print(url)

    session = requests.session()
    response = session.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the #__NEXT_DATA__ script tag
        script_tag = soup.find("script", id="__NEXT_DATA__")
        if script_tag:
            # Extract the JSON data from the script tag
            json_data = json.loads(script_tag.string)

            # Extract book details from the JSON data
            book_details = json_data['props']['pageProps']['product']
            title = book_details['displayName']

            # Extract author(s) from the contributors list
            contributors = book_details['contributors']
            author_names = [contributor['name'] for contributor in contributors]

            # Extract retail price and sale price
            retail_price = book_details.get('retailPrice')
            sale_price = book_details.get('salePrice')

            # Extract book type
            book_type = book_details.get('bindingFormat')

            # Extract published date, publisher, and number of pages
            published_date = book_details.get('publicationDate')
            if published_date:
                # Parse and format the published date if it's provided
                published_date = datetime.strptime(published_date, '%Y-%m-%d').strftime('%Y-%m-%d')
            else:
                published_date = "Publication date not available"

            publisher = book_details.get('publisher')
            num_pages = book_details.get('numberOfPages')

            # Extract ISBN-10
            isbn_10 = book_details.get('isbn10')

            return {
                "ISBN13": isbn,
                "Title of the Book": title,
                "Author/s": author_names,
                "Book type": book_type,
                "Original Price (RRP)": retail_price,
                "Discounted price": sale_price,
                "ISBN-10": isbn_10,
                "Published Date": published_date,
                "Publisher": publisher,
                "No. of Pages": num_pages,
            }
        else:
            print("No #__NEXT_DATA__ script tag found.")
            return None
    else:
        print(f"Failed to fetch the page for ISBN: {isbn}")
        return {
                "ISBN13": isbn,
                "Title of the Book":'failed to fetch page',
                "Author/s":'',
                "Book type":'',
                "Original Price (RRP)":'',
                "Discounted price":'',
                "ISBN-10":'',
                "Published Date":'',
                "Publisher":'',
                "No. of Pages":'',
            }
