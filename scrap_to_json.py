import requests
import json
from bs4 import BeautifulSoup

base_url = "http://quotes.toscrape.com"
quotes = []
authors = []
page_url = base_url


def get_author_info(author_url):
    author_response = requests.get(author_url)
    author_soup = BeautifulSoup(author_response.text, 'html.parser')
    fullname = author_soup.find('h3').text.strip()
    born_date = author_soup.find('span', class_='author-born-date').text.strip()
    born_location = author_soup.find('span', class_='author-born-location').text.strip()
    description = author_soup.find('div', class_='author-description').text.strip()
    return {
        "fullname": fullname,
        "born_date": born_date,
        "born_location": born_location,
        "description": description
    }


while True:
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    for quote_block in soup.find_all('div', class_='quote'):
        text = quote_block.find('span', class_='text').text.strip()
        author_url = base_url + quote_block.find('a')['href']
        author = quote_block.find('small', class_='author').text.strip()
        tags = [tag.text.strip() for tag in quote_block.find_all('a', class_='tag')]

        author_info = next((a for a in authors if a['fullname'] == author), None)
        if not author_info:
            author_info = get_author_info(author_url)
            authors.append(author_info)

        quotes.append({
            "tags": tags,
            "author": author,
            "quote": text
        })

    next_page = soup.find('li', class_='next')
    if next_page:
        page_url = base_url + next_page.find('a')['href']
    else:
        break

with open('quotes.json', 'w') as quotes_file:
    json.dump(quotes, quotes_file, indent=2)

with open('authors.json', 'w') as authors_file:
    json.dump(authors, authors_file, indent=2)

print("Scraping is complete. The quotes.json and authors.json files are saved.")