import click

from crawlers.reddit_crawler import print_subreddits, filter_by_votes, get_threads


@click.command()
@click.option('--subreddits', '-s', required=True, help="Threads que deseja buscar separadas por ';'")
@click.option('--min-votes', '-m', default=5000, help="Número mínimo de votos")
def main(subreddits, min_votes):
    for subreddit in subreddits.split(';'):
        print_subreddits(filter_by_votes(get_threads(subreddit), min_votes=min_votes))


if __name__ == '__main__':
    main()
