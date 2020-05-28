import urllib.request


def http_get(url):
    request = urllib.request.Request(
        url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(request)
    return response.read()
