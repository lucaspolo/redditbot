from crawlers.reddit_crawler import convert_upvotes_to_num


def test_convert_upvotes_to_num():
    assert convert_upvotes_to_num("10k") == 10000
