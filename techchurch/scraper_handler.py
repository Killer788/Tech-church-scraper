from .models import Author, Tag, Article, ArticleSearchByKeywordItem, ArticleTag, ArticleAuthor

import json

import requests
from bs4 import BeautifulSoup


class ScraperHandler:
    def __init__(self, base_url, search_url):
        self.base_url = base_url
        self.search_url = search_url

    def search_by_keyword(self, search_by_keyword_instance):
        print('search_by_keyword => Started')
        search_items = list()

        for i in range(search_by_keyword_instance.page_count):
            response = self.request_to_target_url(self.search_url.format(
                keyword=search_by_keyword_instance.keyword,
                page_count=i,
            ))
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                search_items += self.extract_from_soup(search_by_keyword_instance=search_by_keyword_instance, soup=soup)

            for search_item in search_items:
                article, authors, tags = self.parse_article_detail(item=search_item)
                search_item.article = article
                search_item.is_scraped = True
                search_item.save()
                data = {
                    'title': article.title,
                    'description': article.description,
                    'thumbnail': article.thumbnail,
                    'authors': authors,
                    'tags': tags,
                }
                print(data)
                print('text:', article.text)

        print('search_by_keyword => Finished')
        return len(search_items)

    def parse_article_detail(self, item):
        print('parse_article_detail => Started')
        response = self.request_to_target_url(url=item.url)
        article_soup = BeautifulSoup(response.text, "html.parser")

        try:
            page_title = article_soup.find('title').text
        except Exception:
            page_title = 'Found'

        print(page_title)
        if page_title != 'Page not found | TechCrunch':
            title = article_soup.find('h1', attrs={'class': 'article__title'}).text

            h2_tag = article_soup.find('h2', attrs={'class': 'article__subtitle'})
            if h2_tag:
                description = h2_tag.text
            else:
                description = item.description

            script_tag_txt = article_soup.find('script', attrs={'class': 'yoast-schema-graph'}).text
            json_txt = json.loads(script_tag_txt)
            thumbnail = json_txt['@graph'][0]['image']['url']

            text = ''
            div_tag = article_soup.find('div', attrs={'class': 'article-content'})
            text_tags = div_tag.findAll()
            consumed_tags = list()
            for text_tag in text_tags:
                try:
                    consumed_tags += text_tag.findChildren()
                    if text_tag.name == 'img':
                        text += '\n' + text_tag['src']
                    elif 'embed--techcrunch' not in text_tag['class']:
                        if text_tag not in consumed_tags:
                            text += '\n' + text_tag.text
                            consumed_tags.append(text_tag.findChildren())

                except KeyError:
                    if text_tag not in consumed_tags:
                        text += text_tag.text.strip()
                        consumed_tags.append(text_tag.findChildren())

            article, _ = Article.objects.get_or_create(
                title=title,
                description=description,
                thumbnail=thumbnail,
                text=text,
            )

            authors = self.parse_author(soup=article_soup)
            for author in authors:
                ArticleAuthor.objects.get_or_create(article=article, author=author)

            tags = self.parse_tags(soup=article_soup)
            for tag in tags:
                ArticleTag.objects.get_or_create(article=article, tag=tag)
        else:
            title = 'Not Found!'
            description = 'Not Found!'
            thumbnail = 'Not Found!'
            text = 'Not Found!'
            article, _ = Article.objects.get_or_create(
                title=title,
                description=description,
                thumbnail=thumbnail,
                text=text,
            )

            authors = list()
            new_author, _ = Author.objects.get_or_create(full_name='Not Found!')
            authors.append(new_author)
            for author in authors:
                ArticleAuthor.objects.get_or_create(article=article, author=author)

            tags = list()
            new_tag, _ = Tag.objects.get_or_create(title='Not Found!')
            tags.append(new_tag)
            for tag in tags:
                ArticleTag.objects.get_or_create(article=article, tag=tag)

        print('parse_article_detail => Finished')
        return article, authors, tags

    def parse_tags(self, soup):
        print('parse_tags => Started')
        tags = list()

        script_tag_txt = soup.find('script', attrs={'class': 'yoast-schema-graph'}).text
        json_txt = json.loads(script_tag_txt)
        try:
            article_tags = json_txt['@graph'][0]['keywords']
            for tag in article_tags:
                new_tag, _ = Tag.objects.get_or_create(title=tag)
                tags.append(new_tag)
        except Exception as e:
            print(e)
            print("There were no tags")
            new_tag, _ = Tag.objects.get_or_create(title='None')
            tags.append(new_tag)

        print('parse_tags => Finished')
        return tags

    def parse_author(self, soup):
        print('parse_author => Started')
        authors = list()

        article_author_div_tag = soup.find('div', attrs={'class': 'article__byline'})
        article_authors = article_author_div_tag.findAll('a')
        for article_author in article_authors:
            if '@' not in article_author.text.strip():
                new_author, _ = Author.objects.get_or_create(full_name=article_author.text.strip())
                authors.append(new_author)

        print('parse_author => Finished')
        return authors

    def extract_from_soup(self, search_by_keyword_instance, soup):
        print('extract_from_soup => Started')
        search_items = list()
        search_divs_siblings = list()

        search_divs = soup.findAll('div', attrs={'class': 'd-tc va-top'})
        for search_div in search_divs:
            search_divs_siblings.append(search_div.findNextSibling())

        for div in search_divs_siblings:
            search_items.append(self.parse_search_item(search_by_keyword_instance=search_by_keyword_instance, soup=div))

        print('extract_from_soup => Finished')
        return search_items

    def parse_search_item(self, search_by_keyword_instance, soup):
        print('parse_search_item => Started')
        a_tag = soup.find('a', attrs={'class': 'fz-20 lh-22 fw-b'})
        p_tag = soup.find('p', attrs={'class': 'fz-14 lh-20 c-777'})

        print('parse_search_item => Finished')
        return ArticleSearchByKeywordItem.objects.create(
            search_by_keyword=search_by_keyword_instance,
            title=a_tag.text.strip(),
            description=p_tag.text.strip(),
            url=a_tag['href'],
        )

    def request_to_target_url(self, url):
        print('Request sent to URL:', url)
        return requests.get(url)
