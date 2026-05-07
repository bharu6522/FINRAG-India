import re 


def clean_text(raw_text: str) -> str: 

    text = re.sub(r'\n{3}','\n\n', raw_text)
    text = re.sub(r'-\n(\w)',r'\1', text)
    text = re.sub(r'(?<![.!?])\n(?=[a-z])', ' ', text)
    text = re.sub(r' +',' ', text)

    ## Unicode 
    text = text.replace('\u2013', '-').replace('\u2014', '--')
    text = text.replace('\u201c', '"').replace('\u201d', '"')
    text = text.replace('\u2018', "'").replace('\u2019', "'")

    # Remove non-printable characters
    text = re.sub(r'[^\x20-\x7E\n\t₹%]', '', text)


    return text 

def clean_document(doc: dict) -> dict :
    cleaned_pages = []
    for page in doc["pages"]:
        cleaned = clean_text(page["text"])
        if len(cleaned) > 50:
            cleaned_pages.append({
                "page": page["page"],
                "text": cleaned
            })


    doc['pages'] = cleaned_pages

    return doc 