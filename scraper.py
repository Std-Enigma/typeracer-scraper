import json

import requests
from bs4 import BeautifulSoup

URL_PREFIX = "https://www.typeracerdata.com/texts"
URL_ARGS = "texts=full&sort=relative_average"
URL = f"{URL_PREFIX}?{URL_ARGS}"


class TypeRacerTextData(dict):  # a dict that represents a type racer text data
    def __init__(self, id: str, text: str, difficulty: float) -> None:
        self["id"] = id
        self["text"] = text
        self["length"] = len(text)
        self["difficulty"] = difficulty


def get_content(url: str) -> bytes:
    return requests.get(url).content


def get_stats_table(soup: BeautifulSoup):
    return soup.find("table", class_="stats")


def parse_table(table) -> list[TypeRacerTextData]:
    data = []

    rows = table.find_all("tr")[1::] # don't include the first row since it's the table header
    for row in rows:
        row_data: list[str] = [data.text for data in row.find_all("td")]
        (id, text, difficulty) = (row_data[1], row_data[2], float(row_data[5]))
        text_data = TypeRacerTextData(id, text, difficulty)
        data.append(text_data)

    return data


if __name__ == "__main__":
    content = get_content(URL)
    soup = BeautifulSoup(content, "html.parser")
    table = get_stats_table(soup)
    json_data = parse_table(table)

    with open("data.json", "w") as file:
        json.dump(json_data, file)
