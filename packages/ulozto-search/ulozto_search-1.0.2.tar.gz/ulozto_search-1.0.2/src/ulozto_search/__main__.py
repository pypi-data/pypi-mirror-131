#!/usr/bin/env python3
from ulozto_search.ulozto_search import search
def cmd():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="String to query uloz.to", type=str)
    parser.add_argument("-t", "--type", help="Filter by file type",
                        type=str, choices=["documents", "videos", "images", "archives", "audios"])
    parser.add_argument("--insecure", help="Don't verify SSL certificates, not recommended",
                        action="store_true")
    parser.add_argument("--show-approximate", help="Show approximate results", action="store_true")
    args = parser.parse_args()
    results = search(args.query, args.type, insecure=args.insecure, includeApproximate=args.show_approximate)
    if len(results) == 0:
        print("Haven't found any results")
        return
    for result in results:
        name, url = result.values()
        print(f'{name:10} | {url:10}')
    return

if __name__ == "__main__":
    cmd()
