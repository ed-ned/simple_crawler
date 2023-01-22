from bs4 import BeautifulSoup
import requests
from urllib.parse import urlsplit
from collections import deque


class SpiderException(Exception):
    """Spider base exception"""
    pass


class SpiderUrlDoesNotExists(SpiderException):
    """Spider was called with empty or broken URL"""
    pass


class Spider:
    """
    Spider class designed to collect links from an incoming URL. The search
    is not limited to the passed URL, it continues through the nested ones.
    The class accepts two parameters:
      url - address of the start page
      max_level - how many levels of nesting the search is lowered to
    """

    def __init__(self, url: str, max_level=1):
        self.url = url
        self.max_level = max_level

    def _is_valide_link(self, url: str) -> bool:
        if not url:
            return False
        if url.startswith('#'):
            return False
        return True

    def _get_base_url(self, url: str) -> str:
        parts = urlsplit(url)
        return "{0.scheme}://{0.netloc}".format(parts)

    def _fix_link(self, url: str, base_url: str) -> str:
        return base_url + url if url.startswith('/') else url

    def process(self, max_level=1):

        if not self.url:
            raise SpiderUrlDoesNotExists('An empty url was passed')

        level_number = 0
        current_level_urls = deque([self.url])
        new_level_urls = deque()
        visited_urls = set()

        # BFS like link searching method
        while len(current_level_urls):

            current_url = current_level_urls.popleft()
            visited_urls.add(current_url)

            # We throw an exception unless we could get the initializing url,
            # otherwise we skip it
            # We need base_link to fix local link like /page.html...
            try:
                response = requests.get(current_url)
                base_link = self._get_base_url(current_url)
            except (requests.exceptions.RequestException, ValueError):
                if current_url == self.url:
                    raise SpiderUrlDoesNotExists(
                        'Initial url does not exists or broken',
                    )
                continue

            soup = BeautifulSoup(response.text, features='lxml')
            for link in soup.find_all('a'):

                new_link = link.get('href')

                # Skip URL like #something
                if not self._is_valide_link(new_link):
                    continue

                new_link = self._fix_link(new_link, base_link)

                # We skip visited in previous and current levels links
                if (new_link not in visited_urls and
                        new_link not in new_level_urls):
                    new_level_urls.append(new_link)

            # We do not add new levels link if we get max_level
            if not current_level_urls and level_number < self.max_level:
                current_level_urls.extend(new_level_urls)
                new_level_urls.clear()
                level_number += 1

        return list(visited_urls)