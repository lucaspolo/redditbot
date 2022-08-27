import asyncio

import click

from redditbot.crawlers.reddit_crawler import print_subreddits, filter_by_votes, get_subreddits


@click.command()
@click.option('--subreddits', '-s', required=True, help="Threads que deseja buscar separadas por ';'")
@click.option('--min-votes', '-m', default=5000, help='Número mínimo de votos')
def main(subreddits, min_votes):
    subreddits = subreddits.split(';')
    threads = asyncio.run(get_subreddits(subreddits))
    filtred_threads = filter_by_votes(threads, min_votes=min_votes)
    print_subreddits(filtred_threads)


if __name__ == '__main__':
    main()
