import requests

BASE_URL = "https://www.reddit.com"

REDDIT_URL = "https://www.reddit.com/r/{0}/top.json"


def convert_upvotes_to_num(votes):
    return int(votes.replace("k", "000"))


def get_threads(subreddit):
    """Recupera as threads e suas informações do subreddit

    :param subreddit: subreddit a ser pesquisado
    :return: lista de threads do subreddit
    """

    headers = {
        'User-Agent': 'telegram:pytroxa:v1',
    }

    r = requests.get(REDDIT_URL.format(subreddit), params={'sort': 'new'}, headers=headers)

    response_dict = r.json()

    elements_threads = response_dict['data']['children'] if r.status_code == requests.codes.ok else []

    threads = []

    for element in elements_threads:
        thread = convert_element_to_thread(element)

        threads.append(thread)

    return threads


def convert_element_to_thread(element):

    thread = {}
    dados = element['data']
    thread["subreddit"] = dados['subreddit']
    thread["title"] = dados['title']
    thread["upvotes"] = dados['ups']
    thread["comments"] = BASE_URL + dados['permalink']
    thread["link"] = convert_internal_link_to_absolute(dados['url'])

    # if thread["link"].startswith("/r/"):
    #     thread["external"] = False
    #     thread["link"] = BASE_URL + thread["link"]
    # else:
    #     thread["external"] = True

    return thread


def convert_internal_link_to_absolute(link):
    if link.startswith("/r/"):
        return BASE_URL + link
    else:
        return link


def print_subreddits(threads):
    """Imprime de maneira formatada as threads do subreddit"""

    for thread in threads:
        print(f"r/{thread['subreddit']} - [{thread['upvotes']}] {thread['title']}")
        print(f"\tLink: {thread['link']}")
        print(f"\tComments: {thread['comments']}\n")


def filter_by_votes(threads, min_votes=1):
    return [thread for thread in threads if thread['upvotes'] > min_votes]


def main(subreddits):
    for subreddit in subreddits:
        print_subreddits(filter_by_votes(get_threads(subreddit)))


if __name__ == '__main__':
    entrada = input("Digite os topicos desejados separados por (;): ")
    main(entrada.split(";"))
