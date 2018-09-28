#!/usr/bin/env python
from time import sleep
import requests
from bs4 import BeautifulSoup


"""
Author: Michael Su
Date: 2018/9/28
"""

"""
In Crawl_ptt_beauty module, it implement 4 functionalities:
    1. Crawl ptt beauty articles in 2017
    2. Find top 10 push articles and top 10 boo articles
    3. Get all image urls in popular article
    4. Use search key to search article and get all image urls in these
        articles.
"""

class Crawl_ptt_beauty():
    """Module for crawl PTT Beauty articles in 2017 and search specific article

    """

    def __init__(self):
        """Class initialization
        Set search url and file name to save all article url and all popular
        article url.
        """
        self.base_url = "https://www.ptt.cc"
        self.start_crawl_url_index = 1992
        self.all_article_file_name = "all_articles.txt"
        self.all_popular_file_name = "all_popular.txt"
        self.exception = [
            "https://www.ptt.cc/bbs/Beauty/M.1490936972.A.60D.html",
            "https://www.ptt.cc/bbs/Beauty/M.1494776135.A.50A.html",
            "https://www.ptt.cc/bbs/Beauty/M.1503194519.A.F4C.html",
            "https://www.ptt.cc/bbs/Beauty/M.1504936945.A.313.html",
            "https://www.ptt.cc/bbs/Beauty/M.1505973115.A.732.html",
            "https://www.ptt.cc/bbs/Beauty/M.1507620395.A.27E.html",
            "https://www.ptt.cc/bbs/Beauty/M.1510829546.A.D83.html",
            "https://www.ptt.cc/bbs/Beauty/M.1512141143.A.D31.html"]


    def crawl(self):
        """Crawl all artitle

        """
        article_file = open(self.all_article_file_name, "w")
        popular_file = open(self.all_popular_file_name, "w")
        year = 2016
        last_date = 10000
        while year < 2018:
            sleep(0.01)
            url = "https://www.ptt.cc/bbs/Beauty/index" + \
                str(self.start_crawl_url_index) + ".html"
            req = requests.get(url)
            content = req.text
            soup = BeautifulSoup(content, 'html.parser')
            articles = soup.findAll('div', {'class': "r-ent"})

            for article in articles:
                if str(article).find("本文已被刪除") > 0:
                    continue
                # if str(article).find("[公告]") > 0:
                #     continue
                title_element = article.find('div', {'class': "title"})
                if len(title_element) < 1:
                    continue
                else:
                    title_element = title_element.find('a')
                if title_element is None:
                    continue
                if title_element.text.find("[公告]") == 0:
                    continue

                date = article.findAll('div', {'class': "date"})[0].text
                date = date.replace(" ", "").replace("/", "")
                title = title_element.text
                link_url = self.base_url + str(title_element.get('href'))
                if link_url in self.exception:
                    continue
                article_info = date + "," + title + "," + link_url
                # print (article_info)
                if last_date > int(date):
                    year = self.get_article_year(link_url)
                    if year >= 2018:
                        break

                """
                Write article description to "all_articles.txt"
                """
                if year == 2017:
                    article_file.write(article_info + "\n")

                """
                Write article description to "all_popular.txt"
                """
                push_element = article.find('div', {'class': "nrec"})\
                    .find('span')
                if push_element != None:
                    # print (push_element.text)
                    if push_element.text == "爆":
                        if year == 2017:
                            popular_file.write(article_info + "\n")

                last_date = int(date)
            self.start_crawl_url_index = self.start_crawl_url_index + 1
            print ("Index: " + str(self.start_crawl_url_index))


    def get_article_year(self, url):
        """Get year when article is published

        Args:
            url: artile url

        Returns:
            The year when article is published
        """
        req = requests.get(url)
        content = req.text
        soup = BeautifulSoup(content, 'html.parser')
        article_titles = soup.findAll('div', {'class': "article-metaline"})
        for article_title in article_titles:
            if str(article_title).find("時間") < 0:
                continue
            date = article_title.find('span', {'class': "article-meta-value"})\
                .text
        year = date.split(" ")[-1]
        print ("Recent year : " + str(year))
        return int(year)


    def get_top10_push(self, start_date, end_date):
        """Get top 10 push articles and top 10 boo articles

        """
        article_file = open(self.all_article_file_name, "r")
        article_descriptions = article_file.readlines()
        push = {}
        push_number = 0
        boo = {}
        boo_number = 0
        for article_description in article_descriptions:

            date = article_description.split(",", 1)[0]
            url = article_description.rsplit(",", 1)[1]
            date = int(date)
            if date >= int(start_date) and date <= int(end_date):
                print (date)
                sleep(0.01)
                r = requests.get(url.split("\n")[0])
                content = r.text
                soup = BeautifulSoup(content, 'html.parser')
                articles = soup.findAll('div', {'class': "push"})
                for article in articles:
                    b_type = article.find('span', {'class': "f1 hl push-tag"})
                    p_type = article.find('span', {'class': "hl push-tag"})
                    if b_type != None:
                        if b_type.text == "噓 ":
                            boo_number = boo_number + 1
                            user_id = article.find(
                                'span',
                                {'class': "f3 hl push-userid"}).text
                            if user_id in boo.keys():
                                boo[user_id] = boo[user_id] + 1
                            else:
                                boo[user_id] = 1
                    if p_type != None:
                        if p_type.text == "推 ":
                            push_number = push_number + 1
                            user_id = article.find(
                                'span',
                                {'class': "f3 hl push-userid"}).text
                            if user_id in push.keys():
                                push[user_id] = push[user_id] + 1
                            else:
                                push[user_id] = 1
        sorted_push = self.sort_list(push)
        sorted_boo = self.sort_list(boo)
        push_file_name = "push[" + start_date + "-" + end_date + "].txt"
        push_file = open(push_file_name, "w")
        self.write_to_push_file(
            push_file,
            push_number,
            sorted_push,
            boo_number,
            sorted_boo)


    def sort_list(self, push_dict):
        """Sort top 10 articles

        Args:
            push_dict: push article dictionary

        Returns:
            sorted article list
        """
        sorted_push = sorted(push_dict.items(), key=lambda x: x[1], reverse=True)
        sorted_push = sorted_push[0:10]
        i = 0
        while i < 10:
            number = sorted_push[i][1]
            j = i + 1
            while j < 10 and sorted_push[j][1] == number:
                j = j + 1
            sorted_push[i:j] = sorted(sorted_push[i:j], key=lambda x: x[0])
            i = j
        return sorted_push


    def write_to_push_file(
            self,
            push_file,
            push_number,
            sorted_push,
            boo_number,
            sorted_boo):
        """write top 10 push articles to file

        Args:
            push_file: The file to write
            push_number: Push number
            sorted_push: sorted push article list
            boo_number: Boo number
            sorted_boo: sorted boo article list
        """
        string = "all like: " + str(push_number) + "\n"
        push_file.write(string)
        string = "all boo: " + str(boo_number) + "\n"
        push_file.write(string)
        for i in range(0, 10):
            string = "like #" + str(i+1) + ": " + sorted_push[i][0] + " "
            string = string + str(sorted_push[i][1]) + "\n"
            push_file.write(string)
        for i in range(0, 10):
            string = "boo #" + str(i+1) + ": " + sorted_boo[i][0] + " "
            string = string + str(sorted_boo[i][1]) + "\n"
            push_file.write(string)


    def get_popular_article(self, start_date, end_date):
        """Write popular article url to file

        Search all popular article and write its url to file

        Args:
            start_date: The starting date to search
            end_date: The ending date to search
        """
        popular_file = open(self.all_popular_file_name, "r")
        popular_sta_file_name = "popular[" + start_date + "-" + end_date + "].txt"
        popular_sta_file = open(popular_sta_file_name, "w")
        popular_descriptions = popular_file.readlines()
        popular_number = 0
        image_url_list = []
        for popular_description in popular_descriptions:
            date = popular_description.split(",", 1)[0]
            url = popular_description.rsplit(",", 1)[1]
            date = int(date)
            if date >= int(start_date) and date <= int(end_date):
                popular_number = popular_number + 1
                print (date)
                sleep(0.01)
                req = requests.get(url.split("\n")[0])
                content = req.text
                soup = BeautifulSoup(content, 'html.parser')
                for link in soup.findAll('a'):
                    link = link.get('href')
                    if link is None:
                        continue
                    if link.endswith(".png"):
                        image_url_list.append(link)
                    elif link.endswith(".jpg"):
                        image_url_list.append(link)
                    elif link.endswith(".jpeg"):
                        image_url_list.append(link)
                    elif link.endswith(".gif"):
                        image_url_list.append(link)
        string = "number of popular articles: " + str(popular_number) +"\n"
        popular_sta_file.write(string)
        for image_url in image_url_list:
            popular_sta_file.write(image_url + "\n")


    def find_article(self, search_key, start_date, end_date):
        """Use search key to search articles

        Use search key to search articles and find image url in in these
        articles. Then write these image urls to file.

        Args:
            search_key: The key string to search
            start_date: The starting date to search
            end_date: The ending date to search
        """
        article_file = open(self.all_article_file_name, "r")
        article_descriptions = article_file.readlines()
        keyword_file_name = "keyword(" + search_key + ")[" + start_date + "-" \
            + end_date + "].txt"
        keyword_file = open(keyword_file_name, "w")
        for article_description in article_descriptions:
            date = article_description.split(",", 1)[0]
            url = article_description.rsplit(",", 1)[1]
            date = int(date)
            keywords = []
            image_url_list = []
            if date >= int(start_date) and date <= int(end_date):
                print (date)
                sleep(0.01)
                req = requests.get(url.split("\n")[0])
                content = req.text
                # print (content)
                soup = BeautifulSoup(content, 'html.parser')
                description = soup.find('div', {'id': "main-content"})
                title_tags = description.findAll('span', {'class':\
                    "article-meta-tag"})
                title_values = description.findAll('span', {'class':\
                    "article-meta-value"})
                for title_tag in title_tags:
                    keywords.append(title_tag.text)
                for title_value in title_values:
                    keywords.append(title_value.text)

                article = description.text.split("※ 發信站: 批踢踢實業坊(ptt.cc)"\
                    )[0]
                keywords.append(article)
                has_search_key = False
                for keyword in keywords:
                    if search_key in keyword:
                        has_search_key = True
                        break
                if has_search_key:
                    for link in soup.findAll('a'):
                        link = link.get('href')
                        if link is None:
                            continue
                        if link.endswith(".png"):
                            image_url_list.append(link)
                        elif link.endswith(".jpg"):
                            image_url_list.append(link)
                        elif link.endswith(".jpeg"):
                            image_url_list.append(link)
                        elif link.endswith(".gif"):
                            image_url_list.append(link)
            for image_url in image_url_list:
                keyword_file.write(image_url + "\n")
