from bs4 import BeautifulSoup

def extract_headings(html):
    soup = BeautifulSoup(html, "html.parser")
    headings = []
    for tag in ['h1', 'h2', 'h3']:
        for heading in soup.find_all(tag):
            text = heading.get_text(strip=True)
            if text:
                headings.append(text)
    return headings

def extract_links(html):
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a_tag in soup.find_all('a', href=True):
        text = a_tag.get_text(strip=True)
        href = a_tag['href']
        if text and href:
            links.append((text, href))
    return links
