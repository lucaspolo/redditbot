from requests_html import HTMLSession

BASE_URL = "https://www.reddit.com/r/{0}/"

session = HTMLSession()

r = session.get(BASE_URL.format("python"))

elements_threads = r.html.find(".thing")

threads = []

for element in elements_threads:
    thread = {}

    thread["subreddit"] = element.attrs["data-subreddit"]
    thread["titulo"] = element.find("a.title", first=True).text
    thread["upvotes"] = element.attrs["data-score"]
    thread["comments"] = element.attrs["data-permalink"]

    print(thread)

    threads.append(thread)
