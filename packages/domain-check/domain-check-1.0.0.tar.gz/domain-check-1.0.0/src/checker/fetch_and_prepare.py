from typing import Tuple, List, Optional

import requests

from .log_setup import logger


def extract_price_per_month(string: str) -> float:
    """ Extract price per month from price per year string """
    f = string.replace(" EUR", "").replace(",", ".")  # "4,20 EUR" to 4.20
    return round(float(f)/12, 2)


def fetch_file(link="https://www.do.de/api/csvpreisliste") -> Optional[List[Tuple[str, float]]]:
    """
    Fetch data from do.de and extract only the needed columns of the gained list
    :param link:
    :return: List of tuples that contain (name, price per month)
    """
    price_file = requests.get(link)

    if price_file.status_code != 200:
        logger.error(f"Can't fetch {link} - response: {price_file.status_code}")
        return None

    # clean text, split full text into lines
    full_lines = price_file.text.replace('"', '').strip().split("\n")
    ready_lines = []
    # split lines, extract first column (domain) and second (price per year)
    for line in full_lines[1:]:
        split = line.split(";")
        price = extract_price_per_month(split[1])

        ready_lines.append((split[0], price))

    return ready_lines




