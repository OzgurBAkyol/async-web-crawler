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

def extract_headings_with_elements(html):
    soup = BeautifulSoup(html, "html.parser")
    headings = []
    for tag in ['h1', 'h2', 'h3']:
        for heading in soup.find_all(tag):
            text = heading.get_text(strip=True)
            if text:
                headings.append(heading)
    return headings

def select_items(items):
    print("Aşağıdaki başlıklar bulundu:")
    for i, item in enumerate(items, 1):
        print(f"{i}. {item.get_text(strip=True)}")
    selection = input("Seçmek istediğiniz başlıkların numaralarını virgülle ayırarak yazın: ")
    indices = [int(x.strip()) for x in selection.split(',') if x.strip().isdigit()]
    selected = [items[i-1] for i in indices if 0 < i <= len(items)]
    return selected

def get_content_of_headings(headings):
    contents = []
    for heading in headings:
        content = heading.get_text(strip=True)
        sibling = heading.find_next_sibling()
        if sibling and sibling.name == 'p':
            content += '\n' + sibling.get_text(strip=True)
        contents.append({'heading': heading.get_text(strip=True), 'content': content})
    return contents

def save_data(data, filename="output.json"):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ Data saved to {filename}")
    except Exception as e:
        print(f"Error saving data: {e}")

async def main():
    start_url = input("Lütfen taramak istediğiniz web sitesinin URL'sini yazın (örn: https://example.com): ").strip()
    html = await fetch_url(start_url)
    
    if not html:
        print("Sayfa içeriği alınamadı.")
        return

    headings = extract_headings_with_elements(html)
    if not headings:
        print("Bu sayfada hiç başlık bulunamadı.")
        return
    
    selected_headings = select_items(headings)
    if not selected_headings:
        print("Hiç başlık seçilmedi.")
        return

    contents = get_content_of_headings(selected_headings)
    save_data(contents)

if __name__ == "__main__":
    asyncio.run(main())
