from bs4 import BeautifulSoup


def response_pretty(raw_html):
    soup = BeautifulSoup(raw_html, features="lxml")

    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text


DEFAULT = object()


def make_params(**kwargs):
    return {k: v for k, v in kwargs.items() if v is not DEFAULT}



