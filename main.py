import requests
from bs4 import BeautifulSoup
from collections import deque


# def get_links(url: str) -> list:
#     """
#     All Links on the page
#     """
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     links = []
#     for link in soup.find_all('a'):
#         href = link.get('href')
#         if href and href.startswith('/wiki/') and not href.startswith('/wiki/File:'):
#             links.append('https://en.wikipedia.org' + href)
#     return links



def find_path(start_url: str, end_url: str) -> None:
    """
    for found the shortest path
    """
    visited = set()
    queue = deque([(start_url, [])])
    while queue:
        url, path = queue.popleft()
        if url == end_url:
            return path + [url]
        visited.add(url)
        for link in get_links(url):
            if link not in visited:
                queue.append((link, path + [url]))
    return None

start_url = 'https://en.wikipedia.org/wiki/List_of_Xbox_360_retail_configurations#Xbox_360_S'
end_url = 'https://en.wikipedia.org/wiki/Nintendo_3DS'

path = find_path(start_url, end_url)
if path:
    for i in range(len(path) - 1):
        print(f'{i+1}. {path[i]}')
        response = requests.get(path[i])
        soup = BeautifulSoup(response.text, 'html.parser')
        for p in soup.find_all('p'):
            if path[i+1] in str(p):
                link_text = p.text.strip().replace('\n', ' ')
                link_text = ' '.join(link_text.split())
                print(f'   {link_text} ({path[i+1]})')
else:
    print('Path not found')
