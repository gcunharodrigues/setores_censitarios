import requests
import urllib


def get_lat_long(address: str):
    headers = {
        'authority': 'nominatim.openstreetmap.org',
        'method': 'GET',
        'path': '/search.php?q=Shivaji+Nagar%2C+Bangalore%2C+KA+560001&format=jsonv2',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'en-US,en;q=0.9,pt;q=0.8,es;q=0.7,pt-BR;q=0.6,pt-PT;q=0.5',
        'cache-control': 'max-age=0',
        'dnt': '1',
        'priority': 'u=0, i',
        'referer': 'https://nominatim.openstreetmap.org/ui/search.html?q=Shivaji+Nagar%2C+Bangalore%2C+KA+560001',
        'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
    }

    url = 'https://nominatim.openstreetmap.org/search.php?q=' +\
        urllib.parse.quote_plus(address) + \
        '&format=jsonv2'
    response = requests.get(url, headers=headers).json()

    return [float(response[0]["lat"]), float(response[0]["lon"])]
