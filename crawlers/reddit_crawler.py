import sys
from requests_html import HTMLSession

BASE_URL = "https://www.reddit.com"
BASE_SUBREDDIT = BASE_URL + "/r/{0}"

session = HTMLSession()


def convert_upvotes_to_num(votes):
    return int(votes.replace("k", "000"))


def get_threads(subreddit):

    r = session.get(BASE_SUBREDDIT.format(subreddit))

    elements_threads = r.html.find(".thing")

    threads = []

    for element in elements_threads:
        thread = {}

        thread["subreddit"] = element.attrs["data-subreddit"]
        thread["titulo"] = element.find("a.title", first=True).text
        thread["upvotes"] = convert_upvotes_to_num(element.attrs["data-score"])
        thread["comments"] = element.attrs["data-permalink"]
        thread["link"] = element.attrs["data-url"]

        if element.attrs["data-domain"] == f"self.{subreddit}":
            thread["external"] = False
        else
            thread["external"] = True

        threads.append(thread)

    return threads


def print_subreddits(threads):

    for thread in threads:
        print(f"r/{thread['subreddit']} - [{thread['upvotes']}] {thread['titulo']}")
        print(f"\tLink: {thread['link']}")
        print(f"\tComments: {thread['comments']}\n")

def filter_by_votes(threads, min_votes=5000):
    return [thread for thread in threads if thread['upvotes'] > min_votes]

def main(subreddits):
    for subreddit in subreddits:
        print_subreddits(filter_by_votes(get_threads(subreddit)))

if __name__ == '__main__':
    main(sys.argv[1].split(";"))
