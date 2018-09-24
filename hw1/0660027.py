import sys
from crawl_ptt_beauty import Crawl_ptt_beauty

def main():
    crawl = Crawl_ptt_beauty()
    if len(sys.argv) == 2:
        if sys.argv[1] == "crawl":
            crawl.crawl()
        # elif sys.argv[1] == "date":
        #     crawl.get_article_year("https://www.ptt.cc/bbs/Beauty/M.1483157375.A.A1F.html")
        else:
            print ("Wrong command")
    elif len(sys.argv) == 4 :
        if sys.argv[1] == "push":
            crawl.get_top10_push(sys.argv[2], sys.argv[3])
        if sys.argv[1] == "popular":
            crawl.get_popular_article(sys.argv[2], sys.argv[3])

    elif len(sys.argv) == 5 :
        if sys.argv[1] == "keyword":
            crawl.find_article(sys.argv[2], sys.argv[3], sys.argv[4])


    else:
        print ("No command")

if __name__ == "__main__":
    main()
