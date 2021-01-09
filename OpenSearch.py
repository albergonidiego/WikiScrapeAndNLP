#!/usr/bin/python3

"""
    opensearch.py
    MediaWiki API Demos
    Demo of `Opensearch` module: Search the wiki and obtain
	results in an OpenSearch (http://www.opensearch.org) format
    MIT License
"""

import requests

def wiki_search(searchQuery):
    s = requests.Session()
    url = "https://en.wikipedia.org/w/api.php"

    parameters = {
        "action": "opensearch",
        "namespace": "0",
        "search": searchQuery,
        "limit": "5",
        "format": "json"
    }

    response = s.get(url=url, params=parameters)
    data = response.json()

    return data