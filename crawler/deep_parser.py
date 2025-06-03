from bs4 import BeautifulSoup, Tag

SKIP_TAGS = {'script', 'style', 'noscript', 'meta', 'head', 'link', 'iframe'}

def list_elements_with_types(element, idx_start=1, path=''):
    """
    element: BeautifulSoup Tag objesi
    idx_start: index numarası başlangıcı (1 tabanlı)
    path: hiyerarşik path string, örn: '1.2.3'
    
    Returns:
        elements: list of dict, her dict = {'index', 'type', 'tag', 'text', 'path'}
        next_idx: bir sonraki index numarası
    """

    elements = []
    idx = idx_start

    for child in getattr(element, 'contents', []):
        if isinstance(child, Tag):
            if child.name in SKIP_TAGS:
                continue

            text = child.get_text(separator=' ', strip=True)  # metni satır boşluklarıyla birlikte al
            if not text or len(text) < 5:
                continue

            el_type = 'heading' if child.name in ['h1','h2','h3','h4','h5','h6'] else child.name

            elements.append({
                'index': idx,
                'type': el_type,
                'tag': child.name,
                'text': text,  # tam metin, kesme yok
                'path': f"{path}{idx}"
            })
            idx += 1

            # Her durumda alt elemanlara gir
            sub_path = f"{path}{idx-1}."
            sub_elements, idx = list_elements_with_types(
                child, idx, sub_path
            )
            elements.extend(sub_elements)

        else:
            # NavigableString ya da str
            text = str(child).strip()
            if text and len(text) >= 5:
                elements.append({
                    'index': idx,
                    'type': 'text',
                    'tag': 'text',
                    'text': text,  # tam metin
                    'path': f"{path}{idx}"
                })
                idx += 1

    return elements, idx
