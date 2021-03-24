from bs4 import BeautifulSoup

def remove_html(doc):
    soup = BeautifulSoup(doc, 'lxml')
    for s in soup(['script', 'style', 'head', 'meta', 'noscript']):
        s.decompose()
    
    doc = ' '.join(soup.stripped_strings)

    return doc

def clean_message(doc):
    if not doc:
        return ""

    return remove_html(doc)

