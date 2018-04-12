from requests_html import HTMLSession

BASE_URL = "https://www.reddit.com/"
BASE_SUBREDDIT = BASE_URL + "/r/{0}"

session = HTMLSession()

def get_subreddit(subreddit):

    r = session.get(BASE_SUBREDDIT.format(subreddit))

    elements_threads = r.html.find(".thing")

    threads = []

    for element in elements_threads:
        thread = {}

        thread["subreddit"] = element.attrs["data-subreddit"]
        thread["titulo"] = element.find("a.title", first=True).text
        thread["upvotes"] = element.attrs["data-score"]
        thread["comments"] = element.attrs["data-permalink"]
        thread["link"] = element.attrs["data-url"]

        threads.append(thread)

    return threads


def print_subreddits(threads):

    for thread in threads:
        print(f"r/{thread['subreddit']} - [{thread['upvotes']}] {thread['titulo']}")
        print(f"\tLink: {thread['link']}")
        print(f"\tComments: {thread['comments']}\n")

if __name__ == '__main__':
    print_subreddits(get_subreddit("Python"))
