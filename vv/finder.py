import random
import bs4
import duckduckgo_search
import requests


def find_links(query: str) -> [str]:
    res = duckduckgo_search.ddg(query)
    hrefs = list(map(lambda x: x['href'], res))
    return hrefs


def find_some_info_in_link(link: str) -> [str]:
    try:
        req = requests.get(link)
        soup = bs4.BeautifulSoup(req.content, 'html.parser')
        ps = soup.find_all('p')
        res = []
        for e in ps:
            res.append(e.text)
        return res
    except:  # TODO: This is very bad move
        return find_some_info_in_link(link)


def find_some_info(query: str) -> [str]:
    hrefs = find_links(query)
    link = random.choice(hrefs)
    return find_some_info_in_link(link)
