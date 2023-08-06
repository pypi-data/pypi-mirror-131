import grequests
from urllib.parse import *


def addParams(url, params):
    url_parse = urlparse(url)
    query = url_parse.query
    url_dict = dict(parse_qsl(query))
    url_dict.update(params)
    url_new_query = urlencode(url_dict)
    url_parse = url_parse._replace(query=url_new_query)
    return urlunparse(url_parse)


def addSameParams(urls, params):
    return [addParams(url, params) for url in urls]


def addVaryingParams(urls, paramsList):
    assert len(urls) == len(paramsList), 'must determine exact the same'
    res = []
    for i in range(len(urls)):
        res.append(addParams(urls[i], paramsList[i]))
    return res


class CAGrequests:
    def __init__(self, urls):
        self.urls = urls
        self.async_ = None

    def exception(self, request, exception):
        print(f"Problem: {request.url}: {exception}")

    def Async(self, attrName, **kwargs):
        self.async_ = grequests.map((getattr(grequests, attrName)(url, **kwargs) for url in self.urls),
                                    exception_handler=self.exception, size=3)
        return self.async_
