import aiohttp
import asyncio
from bs4 import BeautifulSoup

url = "http://quotes.toscrape.com/"

async def fetch_page(session, page_url):
    async with session.get(page_url) as response:
        return await response.text()

async def fetch_quotes(page_url):
    async with aiohttp.ClientSession() as session:
        html = await fetch_page(session, page_url)
        soup = BeautifulSoup(html, 'html.parser')

        quotes = []
        for quote in soup.find_all('div', class_='quote'):
            text = quote.find('span', class_='text').text
            author = quote.find('small', class_='author').text
            tags = [tag.text for tag in quote.find_all('a', class_='tag')]
            quotes.append({
                'text': text,
                'author': author,
                'tags': tags
            })
        return quotes

# Main function to run the async fetch and print results
async def main():
    quotes = await fetch_quotes(url)
    for q in quotes:
        print(f"Quote: {q['text']}")
        print(f"Author: {q['author']}")
        print(f"Tags: {', '.join(q['tags'])}")
        print("\n" + "-" * 50 + "\n")  # Adds a separator line for readability

# Run the main function
asyncio.run(main())
