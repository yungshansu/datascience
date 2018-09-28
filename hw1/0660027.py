#!/usr/bin/env python
import sys
from crawl_ptt_beauty import Crawl_ptt_beauty

"""
Author: Michael Su
Date: 2018/9/28
"""

"""
Demo Data Science hw1
"""

def main():
    """ Demo function

    There are 4 functionalities for this demo:
        1. Crawl ptt beauty articles in 2017
        2. Find top 10 push articles and top 10 boo articles
        3. Get all image urls in popular article
        4. Use search key to search article and get all image urls in these
            articles.
    """
    crawl = Crawl_ptt_beauty()
    if len(sys.argv) == 2:
        if sys.argv[1] == "crawl":
            crawl.crawl()
        else:
            print ("Wrong command")
    elif len(sys.argv) == 4:
        if sys.argv[1] == "push":
            crawl.get_top10_push(sys.argv[2], sys.argv[3])
        if sys.argv[1] == "popular":
            crawl.get_popular_article(sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 5:
        if sys.argv[1] == "keyword":
            crawl.find_article(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print ("No command")

if __name__ == "__main__":
    main()
