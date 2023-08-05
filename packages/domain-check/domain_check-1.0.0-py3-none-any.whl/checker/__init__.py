# extracted from: https://www.checkdomain.net/en/
import argparse

from .main import main as _main
from .fetch_and_prepare import fetch_file


def main():
    """ Entrypoint, parsing all args, dispatching main """
    # setup argparse and register parameters
    parser = argparse.ArgumentParser("Check which TLDs are still free for a given name")
    parser.add_argument("name", help="The domain name to check for")
    parser.add_argument("-p", "--price", help="Max price for domain, default: 20.000",
                        type=float, default=20.000, required=False)
    parser.add_argument("-l", "--maxlen", help="Max length the TLD shall have, default: 18",
                        type=int, default=18, required=False)
    parser.add_argument("-r", "--rate", help="Delay between whois-calls in seconds, default: 0.2s",
                        type=float, default=0.2, required=False)
    parser.add_argument("-f", "--file", help="File the available results are written to, default: ./'free.txt'",
                        type=str, default="./free.txt", required=False)

    args = parser.parse_args()

    data = fetch_file()

    _main(args.name, data,
          price_below=args.price,
          request_delay=args.rate,
          file_path=args.file)


# if __name__ == '__main__':
#     _main("nico")
