import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json

async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=10) as response:
                return await response.text()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return ""

def parse_html(html):
    try:
        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.string.strip() if soup.title else "No Title"
        return {"title": title}
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return {"title": "Parse Error"}

def save_data(data, filename="output.json"):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ Data saved to {filename}")
    except Exception as e:
        print(f"Error saving data: {e}")

async def main():
    with open("urls.txt", "r") as file:
        urls = [line.strip() for line in file if line.strip()]

    tasks = [fetch_url(url) for url in urls]
    html_pages = await asyncio.gather(*tasks)

    all_data = [parse_html(html) for html in html_pages]

    save_data(all_data)

if __name__ == "__main__":
    asyncio.run(main())
