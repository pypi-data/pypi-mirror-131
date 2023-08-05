import time
import os
from typing import Union, List, Tuple

from .log_setup import logger


def report_free(domain: str, price: Union[int, float], file_path="free.txt"):
    """
    Print free domains on terminal and append domain to file
    The file will have csv format 'domain; price'
    :param domain: Free domain name like example.net
    :param price: Price of domain
    :param file_path: Name of file to report to
    """
    print(f"{domain}, {price}€")
    with open(file_path, "a+") as f:
        f.write(f"{domain}; {price}\n")


# travelersinsurance is the longest upcoming toplevel domain with 18 chars, lol
def main(name, data: List[Tuple[str, float]], price_below=20000, max_len=18, request_delay=0.2, file_path="free.txt"):
    """
    Main routine for checking availability
    Using a subprocess to access the 'nslookup' cli command
    :param name: domain name to check for
    :param data: list with tuples of domains to check for (domain-name, price per month)
    :param price_below: max price for the domain (on do.de)
    :param max_len: max length the domain should have
    :param request_delay: delay between whois-requests
    :param file_path: Name of file to report to
    """

    to_request = data.copy()

    # remove entries that don't match criteria
    for entry in data:
        domain = entry[0]
        price = entry[1]

        if price_below and not price < price_below:
            to_request.remove(entry)
            continue

        if max_len < len(domain):
            to_request.remove(entry)
            continue

    # cycle trough domains that are left and check if available
    for entry in to_request:
        domain = entry[0]
        price = entry[1]

        domain_name = f"{name}.{domain}"

        logger.debug(f"Trying {domain_name}")
        ret: str = os.popen(f"dig {domain_name} SOA").read()

        # check if domain is free, authority section is only given when domain is not registered
        if f"AUTHORITY SECTION" in ret:
            logger.info(f"FOUND FREE: {domain_name} for price: {price}")
            report_free(domain_name, price, file_path=file_path)

        time.sleep(request_delay)

