import asyncio
import aiohttp
from bs4 import BeautifulSoup, Tag
import json
from crawler.deep_parser import list_elements_with_types

async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=10) as response:
                return await response.text()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return ""

def print_elements(elements, max_len=40):
    for el in elements:
        text = el['text']
        if len(text) > max_len:
            text = text[:max_len] + "..."
        print(f"{el['index']}: [{el['type']}] {text} (path: {el['path']})")

def find_children(elements, parent_path):
    children = [el for el in elements
                if el['path'].startswith(parent_path + '.') and
                el['path'].count('.') == parent_path.count('.') + 1]
    return children

def find_all_descendants(elements, parent_path):
    descendants = [el for el in elements if el['path'].startswith(parent_path + '.')]
    return descendants

def select_element(elements):
    current_elements = elements
    while True:
        print("\nMevcut seçenekler:")
        print_elements(current_elements)
        choice = input("Seçmek istediğiniz elemanı numara olarak ya da 'take-<numara>' şeklinde yazın (çıkmak için 'exit'): ").strip()
        if choice.lower() == 'exit':
            return None

        if choice.isdigit():
            idx = int(choice)
        elif choice.lower().startswith('take-'):
            num_part = choice[5:]
            if num_part.isdigit():
                idx = int(num_part)
            else:
                print("Numara kısmı geçerli değil, tekrar deneyin.")
                continue
        else:
            print("Geçersiz giriş, lütfen sadece numara veya 'take-<numara>' formatında yazın.")
            continue

        selected = next((el for el in current_elements if el['index'] == idx), None)
        if selected is None:
            print("Geçersiz numara, tekrar deneyin.")
            continue

        children = find_children(elements, selected['path'])
        if children and not choice.lower().startswith('take-'):
            print(f"'{selected['text']}' başlığının altında {len(children)} alt eleman bulundu, seçim yapmaya devam edin.")
            current_elements = children
        else:
            print(f"'{selected['text']}' seçildi, seçim tamamlandı.")
            return selected

def prepare_output(selected, elements):
    descendants = find_all_descendants(elements, selected['path'])
    return [selected] + descendants

def save_data(data, filename="output.json"):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ Data saved to {filename}")
    except Exception as e:
        print(f"Error saving data: {e}")

def get_element_by_path(soup_element, path):
    indices = list(map(int, path.split('.')))
    current = soup_element
    for idx in indices:
        # current objesi Tag değilse None döndür
        if not isinstance(current, Tag):
            return None

        children = [c for c in current.contents if (isinstance(c, Tag) or (isinstance(c, str) and c.strip()))]
        if idx-1 < 0 or idx-1 >= len(children):
            return None
        current = children[idx-1]
    return current

async def main():
    start_url = input("Tarama yapmak istediğiniz web sitesinin URL'sini girin: ").strip()
    html = await fetch_url(start_url)
    if not html:
        print("Sayfa içeriği alınamadı.")
        return

    soup = BeautifulSoup(html, "html.parser")
    body = soup.body
    if not body:
        print("Sayfada body tagı bulunamadı.")
        return

    elements, _ = list_elements_with_types(body)

    print("Sayfadaki öğeler:")
    print_elements(elements)

    selected = select_element(elements)
    if selected is None:
        print("Seçim yapılmadı, program sonlandırıldı.")
        return

    output = []
    items = prepare_output(selected, elements)

    for item in items:
        item_soup = get_element_by_path(body, item['path'])
        if item_soup:
            item_full_html = item_soup.prettify()
            item_full_text = item_soup.get_text(separator='\n', strip=True)
        else:
            item_full_html = None
            item_full_text = None

        new_item = dict(item)
        new_item['full_html'] = item_full_html
        new_item['full_text'] = item_full_text
        output.append(new_item)

    save_data(output)

if __name__ == "__main__":
    asyncio.run(main())
