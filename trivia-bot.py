import requests
from bs4 import BeautifulSoup
import pandas as pd


seed_urls = ['https://www.opinionstage.com/blog/trivia-questions']

for url in seed_urls:
    questions = []
    answers = []
    data = requests.get(url)
    soup = BeautifulSoup(data.content, 'html.parser')
    # print(soup.prettify())
    divTag = soup.find_all("div", {"class": "inner-text-content"})
    for tag in divTag:
        strongTag = tag.find_all("strong")
        for tag in strongTag:
            print(tag.text)
    for tag in divTag:
        pTag = tag.find_all("p")
        for tag in pTag:
            print(tag.text)
