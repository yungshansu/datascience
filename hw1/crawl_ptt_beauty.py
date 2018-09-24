import os
import requests
from bs4 import BeautifulSoup
from time import sleep

class Crawl_ptt_beauty():


    def __init__(self):
        self.base_url = "https://www.ptt.cc"
        self.start_crawl_url_index = 1992
        self.all_article_file_name = "all_articles.txt"
        self.all_popular_file_name = "all_popular.txt"
        self.exception = [
            "https://www.ptt.cc/bbs/Beauty/M.1494776135.A.50A.html",
            "https://www.ptt.cc/bbs/Beauty/M.1503194519.A.F4C.html",
            "https://www.ptt.cc/bbs/Beauty/M.1504936945.A.313.html",
            "https://www.ptt.cc/bbs/Beauty/M.1505973115.A.732.html",
            "https://www.ptt.cc/bbs/Beauty/M.1507620395.A.27E.html",
            "https://www.ptt.cc/bbs/Beauty/M.1510829546.A.D83.html",
            "https://www.ptt.cc/bbs/Beauty/M.1512141143.A.D31.html"]

    def crawl(self):
        article_file = open(self.all_article_file_name, "w")
        popular_file = open(self.all_popular_file_name, "w")
        year = 2016
        last_date = 10000
        while year < 2018:
            sleep(0.5)
            url = "https://www.ptt.cc/bbs/Beauty/index" + \
                str(self.start_crawl_url_index) + ".html"
            r = requests.get(url)
            content = r.text
            soup = BeautifulSoup(content, 'html.parser')
            articles = soup.findAll('div', {'class': "r-ent"})

            for article in articles:
                if str(article).find("本文已被刪除") > 0:
                    continue
                if str(article).find("[公告]") > 0:
                    continue
                title_element = article.find('div', {'class': "title"})
                if len(title_element) < 1:
                    continue
                else:
                    title_element = title_element.find('a')
                if title_element == None:
                    continue


                date = article.findAll('div', {'class': "date"})[0].text
                date = date.replace(" ","").replace("/","")
                title = title_element.text
                link_url =  (self.base_url + str(title_element.get('href')))
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
            print (self.start_crawl_url_index)


    def get_article_year(self, url):
        r = requests.get(url)
        content = r.text
        soup = BeautifulSoup(content, 'html.parser')
        article_titles = soup.findAll('div',{'class': "article-metaline"})
        for article_title in article_titles:
            if str(article_title).find("時間") < 0:
                continue
            date = article_title.find('span', {'class': "article-meta-value"})\
                .text
        date = date.split(" ")[-1]
        print ("Recent year : " + str(date))
        return int(date)


    def get_top10_push(self, start_date, end_date):
        article_file = open(self.all_article_file_name, "r")
        article_descriptions = article_file.readlines()
        push = {}
        push_number = 0
        boo = {}
        boo_number = 0
        for article_description in article_descriptions:
            sleep(0.5)
            date = article_description.split(",", 1)[0]
            url = article_description.rsplit(",", 1)[1]
            date = int(date)
            if date >= int(start_date) and date <= int(end_date):
                print (date)
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
        sorted_push = sorted(push_dict.items(), key=lambda x: x[1], reverse=True)
        sorted_push = sorted_push[0:10]
        i = 0
        while i < 10:
            number = sorted_push[i][1]
            j = i + 1
            while (j < 10 and sorted_push[j][1] == number):
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
        string = "all like: " + str(push_number) + "\n"
        push_file.write(string)
        string = "all boo: " + str(boo_number) + "\n"
        push_file.write(string)
        for i in range(0,10):
            string = "like #" + str(i+1) + ": " + sorted_push[i][0] + " "
            string = string + str(sorted_push[i][1]) + "\n"
            push_file.write(string)
        for i in range(0,10):
            string = "boo #" + str(i+1) + ": " + sorted_boo[i][0] + " "
            string = string + str(sorted_boo[i][1]) + "\n"
            push_file.write(string)


    def get_popular_article(self, start_date, end_date):
        popular_file = open(self.all_popular_file_name, "r")
        popular_sta_file_name = "popular[" + start_date + "-" + end_date + "].txt"
        popular_sta_file = open(popular_sta_file_name, "w")
        popular_descriptions = popular_file.readlines()
        popular_number = 0
        image_url_list = []
        for popular_description in popular_descriptions:
            sleep(0.5)
            date = popular_description.split(",", 1)[0]
            url = popular_description.rsplit(",", 1)[1]
            date = int(date)
            if date >= int(start_date) and date <= int(end_date):
                popular_number = popular_number + 1
                print (date)
                r = requests.get(url.split("\n")[0])
                content = r.text
                soup = BeautifulSoup(content, 'html.parser')
                for link in soup.findAll('a'):
                    link = link.get('href')
                    if link == None:
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
        article_file = open(self.all_article_file_name, "r")
        article_descriptions = article_file.readlines()
        for article_description in article_descriptions:
            sleep(0.5)
            date = article_description.split(",", 1)[0]
            url = article_description.rsplit(",", 1)[1]
            date = int(date)
            if date >= int(start_date) and date <= int(end_date):
                print (date)
                r = requests.get(url.split("\n")[0])
                content = r.text
                soup = BeautifulSoup(content, 'html.parser')
                description = soup.find('div', {'id': "main-container"})
                print (description)
                break
